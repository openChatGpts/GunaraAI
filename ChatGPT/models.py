from django.db import models
import json

# Create your models here.
class Conversation(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间",auto_now=True)
    mapping = models.JSONField(default=dict) 
    moderation_results = models.JSONField(default=list)
    current_node = models.CharField(verbose_name="当前节点", max_length=100)
    conversation_id = models.CharField(verbose_name="对话ID", max_length=100)
    system_id = models.CharField(verbose_name="首次对话ID", max_length=100)
    messages = models.JSONField(verbose_name="对话列表",default=list)
    def set_mapping(self, mapping_dict):
        self.mapping = json.dumps(mapping_dict)
    def get_mapping(self):
        return json.loads(self.mapping)
     
    def set_messages(self, messages_dict):
        self.messages = json.dumps(messages_dict)
    def get_messages(self):
        return json.loads(self.messages)
    
    class Meta:
        verbose_name = "对话"
        verbose_name_plural = "对话" 
        
    def __str__(self):
        return self.conversation_id
    


    