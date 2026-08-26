from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChatMessageForm
from .models import Conversation, Message


@login_required
def chat_index(request):
    conversation = Conversation.objects.filter(user=request.user).order_by('-updated_at', '-created_at').first()
    if conversation is None:
        return redirect('home')
    return redirect('conversation', conversation_id=conversation.id)


@login_required
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.select_related('report'),
        id=conversation_id,
        user=request.user,
    )
    form = ChatMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            content=form.cleaned_data['content'],
        )
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content='AI processing will be connected soon.',
        )
        return redirect('conversation', conversation_id=conversation.id)
    conversations = Conversation.objects.filter(user=request.user).select_related('report')
    return render(request, 'chat/chat.html', {
        'conversation': conversation,
        'conversations': conversations,
        'form': form,
    })