import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChatMessageForm
from .models import Conversation, Message


@login_required
def chat_index(request):
    conversation = (
        Conversation.objects
        .filter(user=request.user)
        .order_by('-updated_at', '-created_at')
        .first()
    )

    if conversation is None:
        return redirect('home')

    return redirect(
        'conversation',
        conversation_id=conversation.id,
    )


@login_required
def conversation_view(request, conversation_id):

    conversation = get_object_or_404(
        Conversation.objects.select_related('report'),
        id=conversation_id,
        user=request.user,
    )

    form = ChatMessageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        user_message = form.cleaned_data['content']

        previous_messages = (
            Message.objects
            .filter(conversation=conversation)
            .order_by('-created_at')[:20]
        )

        history = [
            {
                'role': message.role,
                'content': message.content,
            }
            for message in reversed(previous_messages)
        ]

        payload = {
            'user_id': request.user.id,
            'report_id': conversation.report.id,
            'message': user_message,
            'history': history,
        }

        try:

            response = requests.post(
                f'{settings.FASTAPI_URL}/api/v1/chat',
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            assistant_answer = data['answer']

        except (requests.RequestException, KeyError, ValueError, TypeError):
            assistant_answer = (
                'Sorry, the AI service is currently unavailable. Please try again.'
            )

        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            content=user_message,
        )
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=assistant_answer,
        )

        return redirect(
            'conversation',
            conversation_id=conversation.id,
        )

    conversations = (
        Conversation.objects
        .filter(user=request.user)
        .select_related('report')
    )

    return render(
        request,
        'chat/chat.html',
        {
            'conversation': conversation,
            'conversations': conversations,
            'form': form,
        },
    )