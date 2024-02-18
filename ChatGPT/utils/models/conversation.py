from ChatGPT.models import Conversation
import uuid
import datetime



class SaveConversation:
    """
    对当前对话ID数据库写入以及对初始化内容写入操作
    
    `initialize` => 对当前对话进行初始化
    `userMapping` => 对用户提问进行数据库写入操作
    `assistantMapping` => 对回复内容进行数据库写入操作

    self.mapping_user: 用户提问数据结构
    self.mapping_assistant: 回复内容数据结构
    """
    def __init__(self, data):
        self.data = data
        self.messages_list = data["messages"]
        self.messages_id = data["messages"][0]["id"]
        self.parent_message_id = data["parent_message_id"]
        self.children = data["children"]
        self.mapping_user = {
            "id": self.messages_id,
            "message": {
                "id": self.messages_id,
                "author": {"role": "user", "metadata": {}},
                "create_time": int(datetime.datetime.now().timestamp()),
                "content": self.messages_list[0]["content"],
                "status": "finished_successfully",
                "weight": 1,
                "metadata": {"timestamp_": "absolute"},
                "recipient": "all",
            },
            "parent": self.parent_message_id,
            "children": [self.children],
        }
        
        
        # self.mapping_assistant["message"][content]["parts"].
        self.mapping_assistant = {
            "id": self.children,
            "message": {
                "id": self.children,
                "author": {"role": "assistant", "metadata": {}},
                "create_time": int(datetime.datetime.now().timestamp()),
                "content": {
                    "content_type": "text",
                    "parts": [],
                },
                "status": "finished_successfully",
                "end_turn": True,
                "weight": 1,
                "metadata": {
                    "finish_details": {"type": "stop", "stop_tokens": [100260]},
                    "is_complete": True,
                    "model_slug": "gpt-3.5-turbo-1106",
                    "parent_id": self.messages_id,
                    "timestamp_": "absolute",
                },
                "recipient": "all",
            },
            "parent": self.messages_id,
            "children": [],
        }

    def initialize(self, conversation_id):
        # 初始化数据结构
        random_uuid = uuid.uuid4()
        mapping = {  
            self.parent_message_id: {
                "id": self.parent_message_id,
                "message": {
                    "id": self.parent_message_id,
                    "author": {"role": "system", "metadata": {}},
                    "content": {"content_type": "text", "parts": [""]},
                    "status": "finished_successfully",
                    "end_turn": True,
                    "weight": 0,
                    "metadata": {},
                    "recipient": "all",
                },
                "parent": str(random_uuid),
                "children": [self.messages_id],
            },
            str(random_uuid): {
                "id": str(random_uuid),
                "children": [self.parent_message_id],
            },
            self.messages_id: self.mapping_user,
        }

        conversationData = { 
            "title": "用户请求帮助",
            "moderation_results": [],
            "mapping": mapping,
            "current_node": self.messages_id,
            "conversation_id": conversation_id,
            "system_id": self.parent_message_id,
            "messages": [
                {'role': 'system', 'content': '你是一个有用的助手'},
                {'role': 'user', 'content': self.messages_list[0]["content"]["parts"][0]},
                ],
        }
        Conversation.objects.create(**conversationData)

    def userMapping(self, conversation_id):
        # 追加内容
        conv_obj = Conversation.objects.get(conversation_id=conversation_id)
        
        conv_obj.mapping[self.messages_id] = self.mapping_user
        p = conv_obj.mapping[self.parent_message_id]["children"]
        p.append(self.messages_id)
        
        self.Messages(
            conv_obj=conv_obj,
            role="user",
            parts=self.messages_list[0]["content"]["parts"][0]
            )

        conv_obj.save()
        


    def assistantMapping(self, conversation_id,dialog):
        # 追加内容
        conv_obj = Conversation.objects.get(conversation_id=conversation_id)
        
        # 将节点设置为assistant id 
        conv_obj.current_node = self.children
        self.mapping_assistant["message"]["content"]["parts"].append(dialog)
        conv_obj.mapping[self.children] = self.mapping_assistant


        self.Messages(
            conv_obj=conv_obj,
            role="assistant",
            parts=dialog
            )
        conv_obj.save()
        
        
    def Messages(self,conv_obj,role,parts):
        """Messages
        将对话内容添加到与GPT Messages里面
            conv_obj (_type_): 传递django对象
            role (_type_):角色
            parts (_type_): 内容
        """
        author ={"role":role,"content":parts}
        messages = conv_obj.messages
        messages.append(author)
        
