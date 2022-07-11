from django.shortcuts import render , redirect
from .forms import PostForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout , authenticate
from . models import Post

# Create your views here.
@login_required(login_url='/login')
def home(requests):
    posts = Post.objects.all()

    if requests.method == "DELETE":
        post_id = requests.DELETE.get("post-id")
        print(post_id)
    return render(requests, 'main/home.html', {"posts":posts})


def sign_up(requests):
    if requests.method == 'POST':
        form = RegisterForm(requests.POST)
        if form.is_valid():
            user = form.save()
            login(requests, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    
    return render(requests, 'registration/sign_up.html' , {'form':form})


@login_required(login_url='/login')
def create_post(requests):
    if requests.method == "POST":
        form = PostForm(requests.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = requests.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
    return render(requests, 'main/create_post.html', {"form":form})