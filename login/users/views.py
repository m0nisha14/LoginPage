
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from login import settings
from django.core.mail import send_mail


def home(request):
    return render(request,"users/index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already registered")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request,"Password did not match")
        
        if not username.isalnum():
            messages.error(request,"Username must be Alpha numeric")
            return redirect('home')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False
        myuser.save()

        messages.success(request,"Your account has been created successfully")


        subject="Welcome to the login page"
        message="Hello " + myuser.first_name + "!! \n" +"Welcome!! \n Thank you for visting our website"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        

        return redirect('signin')



    return render(request,"users/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "users/index.html",{'fname':fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request,"users/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Your account has been logged out successfully")
    return redirect('home')



