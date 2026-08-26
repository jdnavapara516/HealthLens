from django.urls import path

from .views import conversation_view

urlpatterns = [
    path('chat/<int:conversation_id>/', conversation_view, name='conversation'),
]