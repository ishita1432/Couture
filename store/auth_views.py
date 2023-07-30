from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib import messages


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered Successfully!!")
            username = request.POST['username']
            pass1 = request.POST['password1']
            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
                return redirect('home')
            
    context = {'form':form}
    return render(request, "signup.html",context)


def signin(request):
    if request.user.is_authenticated:
       messages.warning(request,'You are already logged in!!')
       return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!!")
            return redirect('login')
    
    return render(request, "signin.html")

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully!!")
        return redirect('home')