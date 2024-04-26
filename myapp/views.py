from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post
from .forms import PostForm


def logoutUser(request):
    logout(request)
    return redirect('index')


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
    else:
        messages.error(request, "An error occured during the registration")
    context = {'form': form}
    return render(request, 'login-register.html', context)


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    context = {'page': page}
    return render(request, 'login-register.html',context)


def index(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    posts = Post.objects.filter(title__icontains=q)
    return render(request, 'index.html', {'posts': posts})


def post(request, pk):
    posts = Post.objects.get(id=pk)
    context = {'post': posts}
    return render(request, 'post.html', context)


@login_required(login_url='/login')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('index')

    context = {'form': form}
    return render(request, 'create-post.html', context)


def delete_post(request, pk):
    posts = Post.objects.get(id=pk)

    if request.method == 'POST':
        posts.delete()
        return redirect('index')
    return render(request, 'delete-post.html')


def UserPosts(request):
    user_posts = Post.objects.filter(author=request.user)
    context = {'user_posts': user_posts}
    return render(request, 'display-posts.html', context)
