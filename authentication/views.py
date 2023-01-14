from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        typeOfUser = request.POST['typeOfUser']
        fname = request.POST['fname']
        lname = request.POST['lname']
        profilePicture = request.POST['profilePicture']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        address = request.POST['address']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists. Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered.")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords did not match.")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.type_of_user = typeOfUser
        myuser.profile_picture = profilePicture
        myuser.add_ress = address

        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name
            username = user.username
            return render(request, "authentication/index.html", {'fname': fname, 'lname': lname, 'username':username})
        
        else:
            messages.error(request, "Wrong credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    # return render(request, "authentication/signout.html")
    # pass
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('home')