from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, "amazoff/home.html", {"name":request.user.username.capitalize()})
    else:
        return render(request, "amazoff/login.html", {"message":"To use this website, please login."})

def _logout(request):
    if request.user.is_authenticated:
        logout(request)
        message = "You have been logged out successfully!."
    else:
        message = "ERROR: You are already logged out."
    return render(request, "amazoff/login.html", {"message":message})

def _login(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "amazoff/home.html", {"name":username.capitalize()})
        else:
            return render(request, "amazoff/login.html", {"message":"Invalid username or password."})
    else:    
        return HttpResponseRedirect(reverse("home"))

def register_view(request, message = "Amazoff, Not so prime!"):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            message = "Passwords do not match."
            return HttpResponseRedirect(reverse("register"), args=(message))

        if User.objects.filter(username=username).exists():
            messages = "Username already taken."
            return HttpResponseRedirect(reverse("register"), args=(message))

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return HttpResponseRedirect(reverse("register"), args=(message))

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return render(request, "amazoff/home.html", {"name":username.capitalize()})
        else:
            return render(request, "amazoff/login.html", {"message":"Something went wrong from out side."})
    return render(request, "amazoff/register.html", {"message":message})
