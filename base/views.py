from django.shortcuts import render, redirect, get_object_or_404
from .forms import MyUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Conversation, Message
from django.db.models import Q



def user_registration(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = MyUserCreationForm()
        if request.method == "POST":
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.email = user.email.lower()
                user.save()
                return redirect("login")
            else:
                messages.error(request,"An error ocurred during registration")

        return render(request, "base/registration_page.html",{"form":form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            email = request.POST.get("email").lower()
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "email or password is incorrect...")
        
        return render(request, "base/login_page.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    conversations = Conversation.objects.filter(
        Q(user1= request.user) | Q(user2=request.user)
    )
    
    return render(request, "base/home.html", {"conversations": conversations})


@login_required(login_url="login")
def chat_details(request, pk):
    conversation = get_object_or_404(Conversation, id=pk)

    if request.user != conversation.user1 and request.user != conversation.user2:
        return redirect("home")
    
    messages = conversation.messages.all()

    conversation.messages.filter(is_read=False, sender__in=[conversation.user1, conversation.user2]).update(is_read=True)

    if request.method == "POST":
        content = request.POST.get("content")
        if content is not None:
            Message.objects.create(
                conversation = conversation,
                sender = request.user,
                content = content
            )
            conversation.save()
        # else:
        #     messages.error(request, "something went wrong with message form try again...")

    return render(request, "base/chat.html", {"conversation": conversation, "messages": messages})


@login_required(login_url="login")
def user_list(request):
    users = User.objects.exclude(id=request.user.id)

    # Get existing conversation partners
    existing_conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )

    conversation_lookup = {}

    for conv in existing_conversations:
        if request.user == conv.user1:
            conversation_lookup[conv.user2.id] = conv.id
        else:
            conversation_lookup[conv.user1.id] = conv.id
    
    return render(request, "base/user_list.html", {"users":users, "conversation_lookup": conversation_lookup})


@login_required(login_url="login")
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect("chat")
    
    # checking if conversation already exist between these users
    conversation = Conversation.objects.filter(
        (Q(user1=request.user) & Q(user2=other_user)) | 
        (Q(user1=other_user) & Q(user2=request.user))
    ).first()

    # if conversation is not exist, create a new one
    if not conversation:
        conversation = Conversation.objects.create(
            user1 = request.user,
            user2 = other_user
        )

    return redirect("chat", conversation_id=conversation)



def new_chat(request):
    return render(request, "base/new_chat.html", {})