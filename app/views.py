from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from app.forms import LoginForm, OfferForm
from datetime import date
# Create your views here.

def index(request):
    return redirect('/app/home')


def register(request):
    if not request.user.is_authenticated:
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
        if not request.user.is_authenticated:
            return redirect('/app/home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/app/home')
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
        return render(request, self.template_name, {'form': form})

def logout(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    auth_logout(request)
    return redirect('/app/home')

class CustomHomeView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        return render(request, self.template_name, {'nbar': 'home'})

class CustomTabNewsView(TemplateView):
    template_name = 'news.html'
    def get(self, request):
        return render(request, self.template_name, {'nbar': 'news'})


class CustomAllOfferView(TemplateView):
    template_name = 'all.html'
    def get(self, request):
        return render(request, self.template_name, {'nbar': 'all'})

class CustomAddOffer(TemplateView):
    template_name = 'addOffer.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/app/home')
        form = OfferForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/app/home')
        form = OfferForm(request.POST)

        if form.is_valid():
            addOffer = form.save(commit=False)
            addOffer.user = request.user

            
            today = date.today()
            d1 = today.strftime("%Y-%m-%d")
            addOffer.date_published = d1

            addOffer.save()
            return redirect('/app/home')
        else:
            messages.error(request, form.errors)
            messages.error(request, "Offer is invalid")
        form = OfferForm()
        return render(request, self.template_name, {'form': form})