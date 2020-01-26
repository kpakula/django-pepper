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
    return redirect('/app/home')


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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

class CustomHomeView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        return render(request, template_name=self.template_name)
