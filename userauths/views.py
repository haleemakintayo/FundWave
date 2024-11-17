from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages

# Create your views here.
def signin(request):
    if request.method == "POST": 
      username = request.POST['email']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)
      if user is not None: 
        login(request, user)
        return redirect('home')
      else: 
        return render(request, 'signin.html', {'error': 'Invalid credentials.'})
    else: 
      return render(request, 'signin.html', {})


def logout_user(request): 
  logout(request)
  return redirect('home')


def signup(request):
    if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
        user = form.save()
        if user is not None:  
          login(request, user)
          messages.success(request, 'Account created successfully!')
          return redirect('home')
        else: 
           messages.error(request, 'Error creating account')
    else:
      form = SignUpForm()
    return render(request, 'signup.html', {'form': form})