from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChatMessageForm
from .models import Conversation, Message


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
    return render(request, 'chat/chat.html', {'conversation': conversation, 'form': form})