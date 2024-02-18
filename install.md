# **高仿 ChatGPT 官网 UI**

## 项目介绍



项目基于 python django 框架开发

前端 react



体验地址：



[点击体验](https://react.orglen.com/)



源码下载：



[下载链接](https://liushuiyin.com/wp-content/uploads/2023/12/chatgpt_python_django_v0.1.1.zip)



## PC 端展示：



亮色主题：





![img](https://liushuiyin.com/wp-content/uploads/2023/12/20231221115738.png)





暗色主题：





![img](https://raw.githubusercontent.com/hhhaiai/Picture/main/img/202402181241732.png)





流式内容输出：





![img](https://raw.githubusercontent.com/hhhaiai/Picture/main/img/202402181241416.png)





dom 差异化更新提升性能：





![img](https://raw.githubusercontent.com/hhhaiai/Picture/main/img/202402181241724.png)





后端提示词 自动为当前内容起标题归纳总结：





![img](https://raw.githubusercontent.com/hhhaiai/Picture/main/img/202402181241175.png)





## 本地部署



```
python 版本 >= 3.6
```



下载压缩包解压进入项目根目录



```
pip install -r requirements.txt
```



编辑目录 `config > .env`



```
# 填入 OPENAI_API_KEY
OPENAI_API_KEY = "sk-rhTQqTiiEefRZEZH3f0d63B69d8b4eAdBcFa69Bc8dB1Fe50"
 
#模型
MODEL = "gpt-3.5-turbo-1106"
 
# 代理url
ENDPOINT = "https://api.openai.com"
```



启动项目：



```
python manage.py runserver
```



## 服务器部署



```
python 版本 >= 3.6
```



下载压缩包解压进入项目根目录



```
pip install -r requirements.txt
```



编辑目录 `config > .env`



```
# 填入 OPENAI_API_KEY
OPENAI_API_KEY = "sk-rhTQqTiiEefRZEZH3f0d63B69d8b4eAdBcFa69Bc8dB1Fe50"
 
#模型
MODEL = "gpt-3.5-turbo-1106"
 
# 代理url
ENDPOINT = "https://api.openai.com"
```



安装 uwsgi



```
pip install uwsgi
```



配置 uwsgi



在项目根目录创建 `uwsgi.ini `并写入



```
[uwsgi]  
#使用nginx连接时使用  
socket=127.0.0.1:8000  #正式上线后使用此模式，速度稍有优势
#直接做web服务器使用  
; http=0.0.0.0:8000  #联调阶段优先使用http模式，方便定点测试
#项目目录  
chdir=/www/wwwroot/react.orglen.com/beta/ 
#项目中wsgi.py文件的目录，相对于项目目录  
wsgi-file=/www/wwwroot/react.orglen.com/beta/chatgpt_python_django/wsgi.py 
 
#http-timeout=60
 
socket-timeout=60
#服务器响应时间
harakiri=60
# 指定启动的工作进程数  
processes=4  
# 指定工作进程中的线程数  
threads=20 
master=True  
# 保存启动之后主进程的pid  
pidfile=uwsgi.pid  
# 设置uwsgi后台运行，用uwsgi.log保存日志信息  
daemonize=uwsgi.log  
 
 
static-map = /static=/www/wwwroot/react.orglen.com/beta/collectstatic/static
# static-map = /media=/www/wwwroot/chat.orglen.com/media
 
buffer-size     = 65535
post-buffering  = 32768
 
 
# 设置虚拟环境的路径  
#virtualenv=/home/shuan/.virtualenvs/bj18_py3# conda 环境路径  
```



配置 nginx socket 模式



```
location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:8000;
       uwsgi_read_timeout 100;
       uwsgi_buffering off;
       chunked_transfer_encoding on;  # 开启分块传输编码
        tcp_nopush on;  # 开启TCP NOPUSH选项，禁止Nagle算法
        tcp_nodelay on;  # 开启TCP NODELAY选项，禁止延迟ACK算法
        keepalive_timeout 300;  # 设定keep-alive超时时间为65秒
       }
 
   location /static {	#这里就是静态文件的配置
        expires 30d;
        autoindex on;
        add_header Cache-Control private;
        alias /www/wwwroot/react.orglen.com/beta/collectstatic/static/;	
    }
```



配置 nginx http 模式



```
location / {
        proxy_pass http://127.0.0.1:8000/;
        # 不缓存，支持流式输出
        proxy_cache off;  # 关闭缓存
        proxy_buffering off;  # 关闭代理缓冲
        chunked_transfer_encoding on;  # 开启分块传输编码
        tcp_nopush on;  # 开启TCP NOPUSH选项，禁止Nagle算法
        tcp_nodelay on;  # 开启TCP NODELAY选项，禁止延迟ACK算法
        keepalive_timeout 300;  # 设定keep-alive超时时间为65秒
    }
 
location /static {	#这里就是静态文件的配置
        expires 30d;
        autoindex on;
        add_header Cache-Control private;
        alias /www/wwwroot/react.orglen.com/beta/collectstatic/static/;	
    }
```



## 启动 uwsgi



用 uwsgi 启动 django 项目



到项目根目录



执行



```
uwsgi --ini uwsgi.ini
```



uwsgi 相关命令



```
uwsgi --ini uwsgi.ini    #启动命令
uwsgi --stop uwsgi.pid    #停止命令 
uwsgi --reload uwsgi.pid    #重启命令
```



## 数据库



django 默认数据库为 sqlite



可以更改为 mysql



在项目中 `chatgpt_python_django/settings.py` 中注释以下代码



```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```



并添加以下代码 请修改为自己的数据库地址



```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
 
        'NAME': '',        #mysql数据库名称
 
        'USER': '',        #mysql数据库用户
 
        'PASSWORD': '',    #mysql数据库密码
 
        'HOST': '',        #mysql数据库连接地址
 
        'PORT': '3306',    #mysql数据库连接端口
    }
}
```



安装 mysql 依赖



```
pip install pymysql
```



在项目中 找到 `chatgpt_python_django/__init__.py` 并填入



```
import pymysql
pymysql.version_info = (1,4,13,"final",0)
pymysql.install_as_MySQLdb()
```



完成数据库的修改操作需要执行以下命令重启 uwsgi



```
uwsgi --reload uwsgi.pid
```



## 遇到的问题



1、安装 uwsgi 报错



缺少 `python-devel`, `python-dev`



如果你的 python 版本在 3.6 请直接用 yum 安装 `python-devel`



在终端执行 `yum -y install python36-devel` 即可