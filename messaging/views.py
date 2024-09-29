from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from .forms import MessageForm


@login_required
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all().order_by('created_at')
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation_view', conversation_id=conversation.id)

    return render(request, 'messaging/conversation.html', {'conversation': conversation, 'messages': messages, 'form': form})


@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})
