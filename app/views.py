from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
# Create your views here.

def index(request):
    return HttpResponse("Hello, it's pepper.");


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/app/')
            else:
                print('invalid')
                # messages.error(request, "Invalid username or password.")
        else:
            print('invalid')
            # messages.error(request, "Invalid username or password. ")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})