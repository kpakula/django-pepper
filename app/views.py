from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.views.generic import TemplateView
from app.forms import LoginForm
# Create your views here.

def index(request):
    return HttpResponse("Hello, it's pepper.");


def register(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/app/profile')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})


class CustomLoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
                
            post = form.cleaned_data['post']
            post2 = form.cleaned_data['post2']
            user = authenticate(username=post, password=post)

            if user is not None:
                auth_login(request, user)
                return redirect('/app/home')
            else:
                messages.error(request, "Invalid login or password")
        else:
            messages.error(request, "Invalid login or password")
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        form = LoginForm()

        if form.is_valid():
            # form.save()
            post = form.cleaned_data['post']
            post2 = form.cleaned_data['post2']

            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            # print(username)            
            
            user = authenticate(username=username, password=password)
 
            if user is not None:
                auth_login(request, user)
                return redirect('/app/home')
            else:
                messages.error(request, "Invalid login or password")
        else:
            messages.error(request, "Invalid login or password")

    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/app/home')

def home(request):
    return render(request, 'home.html')