from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from awward.models import Users
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from awward.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    current_user = request.user
    post = Site.objects.all()
    profile_info = Profile.objects.filter(user=current_user).first()
    context = {'profile':profile_info, 'posts':post}
    return render(request, 'awwards/home.html', context)

def register(request):
    if request.method == 'POST':
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        confirm_password= request.POST['confirm_password']
        if password == confirm_password:
            user = Users(username=username, email=email, password=make_password(password))
            user.save()
            messages.add_message(request, messages.SUCCESS, "Account created successfully!")
            return redirect('signIn')
    else:
        return render(request, 'auth/register.html')

def signIn(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Successfully logged in!")
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "invalid infomation!") 
            return redirect("signIn") 
    else:
        return render(request, 'auth/signIn.html')

def signOut(request):
    logout(request)
    return redirect('signIn')

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        image = request.FILES['image']
        bio = request.POST['bio']
        profile = Profile(user=current_user, image=image, bio=bio)
        profile.save()
        return redirect('profile')
    profile_info = Profile.objects.filter(user=current_user).first()
    context= {'profile':profile_info}   
    return render(request, 'awwards/profile.html', context)

@login_required
def post(request):
    current_user = request.user
    if request.method == 'POST':
        title = request.POST['title']
        screen = request.FILES['screen']
        description = request.POST['description']
        link = request.POST['link']
        location = request.POST['location']
        post = Site(title=title, screen=screen, location=location, description=description, link=link, user=current_user)
        post.save()
        messages.add_message(request, messages.SUCCESS, "post created successfully")
        return redirect('home')
    post = Site.objects.all()
    context = {'posts': post}
    return render(request, 'awwards/post.html', context)

@login_required
def viewpost(request, pk):
    posts = Site.objects.get(id=pk)
    if request.method == 'POST':
       posts.delete()
       return redirect('home')
    context = {'post': posts}
    return render(request, 'awwards/view-post.html', context)

@login_required
def search_posts(request):
    if request.method=='GET':
            query = request.GET.get('q')
            if query:
                searched = Site.objects.filter(title__icontains=query)     
    context = {'searched':searched}
    return redirect('home', context)
    