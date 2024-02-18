
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('conversation/gen_title/<uuid:conversation_id>', views.gen_title,name='gen_title'),
    path('conversation/<uuid:conversation_id>', views.prompt,name='conversation_id'),
    
    
]
   