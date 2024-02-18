from django.http import HttpResponse, StreamingHttpResponse,JsonResponse
from ChatGPT.models import Conversation
from django.core.serializers import serialize  # noqa: F401
import json

from ChatGPT.utils.models import conversation as Conv
from ChatGPT.utils.openai.resources.chat.chat import ChatCompletion
from ChatGPT.utils.http.response import ChatStreaming
def index(request):
    return HttpResponse("ok")

def prompt(request, conversation_id):
    if request.method == "POST":
        body = request.body.decode()
        json_obj = json.loads(body)
        # print(json_obj)
        # 实例化对象
        conv = Conv.SaveConversation(json_obj)
        
        # 判断是否存在 conversation_id 的数据
        exists = Conversation.objects.filter(conversation_id=conversation_id).exists()
        
        if exists:
            conv.userMapping(conversation_id)
            # conv.assistantMapping(conversation_id)
        else:
            # 执行初始化内容
            conv.initialize(conversation_id)
            
        conv_obj = Conversation.objects.get(conversation_id=conversation_id)
        response = StreamingHttpResponse(
            ChatStreaming(json_obj,conversation_id,conv_obj.messages), 
            content_type='text/event-stream'
            )
        response['Content-Type'] = 'text/event-stream; charset=utf-8'
        return response
    
    conv_obj = Conversation.objects.get(conversation_id=conversation_id)
    conversation_json = serialize('json', [conv_obj])
    data = json.loads(conversation_json)[0]['fields']
    if 'messages' in data:
        del data['messages']
    json_data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json')


# def gen_title(request, conversation_id):
#     conv_obj = Conversation.objects.get(conversation_id=conversation_id)
#     conversation_json = serialize('json', [conv_obj])
#     return JsonResponse(json.loads(conversation_json)[0]['fields'], safe=False,)



def gen_title(request, conversation_id): 
    conv_obj = Conversation.objects.get(conversation_id=conversation_id)
    title = ChatCompletion.ChatTitle(conv_obj.messages[1:3])
    conv_obj.title = title
    conv_obj.save()
    return JsonResponse({"title":title})