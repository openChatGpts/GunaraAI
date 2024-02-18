import json
import time
from ChatGPT.utils.models import conversation as Conv
from ChatGPT.utils.openai.resources.chat.chat import ChatCompletion



def ChatStreaming(conv_data,conversation_id,messages):
    dialog=""
    conv = Conv.SaveConversation(conv_data)
    response = ChatCompletion.chat(messages)
    for line in response.iter_lines():  
        if line:
            data = line.decode('utf-8').replace('data: ', '')
            if data =="[DONE]":
                conv.assistantMapping(conversation_id,dialog)
                response.close()  # 关闭响应链接
                break  # 退出循环
            else:
                content = json.loads(data)["choices"][0]["delta"]["content"]
                dialog += content
                time.sleep(0.03)
                yield content
                


    