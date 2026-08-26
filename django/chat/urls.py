from django.urls import path

from .views import chat_index, conversation_view

urlpatterns = [
    path('chat/', chat_index, name='chat_index'),
    path('chat/<int:conversation_id>/', conversation_view, name='conversation'),
]