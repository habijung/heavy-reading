from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile

# Blank page
def index(request):
    msg = "accounts page."
    return render(request, 'accounts/index.html', {'message': msg})

# Sign Up
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            cardname = request.POST['cardname'] + '@narasarang.or.kr'
            affiliation = request.POST['affiliation']

            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=cardname
            )
            
            profile = Profile(user=user, affiliation=affiliation)
            profile.save()
            
            auth.login(request, user)
            return redirect('/')
    
    return render(request, 'accounts/signup.html')



# Log-in
def login(request):
    # If POST request, run log-in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check username / password
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            return render(request, 'accounts/login.html', {'error' : 'username or password is incorrect.'})
        
    # Else GET request, show log-in page
    else:
        return render(request, 'accounts/login.html')

# Log-out
def logout(request):
    # If POST request, run log-out
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # If GET request, show log-out page
    return render(request, 'accounts/login.html')