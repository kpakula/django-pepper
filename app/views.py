from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from app.forms import LoginForm, OfferForm
from datetime import date
from .models import Offer
# Create your views here.
from django.views import generic

HOME_PAGE = '/app/home/'


def index(request):
    return redirect(HOME_PAGE)


# def detail(request):
#     return render(request, 'offer', {})

class DetailView(generic.DetailView):
    model = Offer
    template_name = 'detail.html'


def register(request):
    if request.user.is_authenticated:
        return redirect(HOME_PAGE)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect(HOME_PAGE)
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


class CustomLoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(HOME_PAGE)
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(HOME_PAGE)
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect(HOME_PAGE)
            else:
                messages.error(request, "Invalid login or password")
        else:
            messages.error(request, "Invalid login or password")
        form = LoginForm()
        return render(request, self.template_name, {'form': form})


def logout(request):
    if not request.user.is_authenticated:
        return redirect(HOME_PAGE)
    auth_logout(request)
    return redirect(HOME_PAGE)


class CustomHomeView(TemplateView):
    template_name = 'home.html'
    # Hot offers

    def get(self, request):
        return render(request, self.template_name, {'nbar': 'home'})


class CustomTabNewsView(TemplateView):
    template_name = 'news.html'
    # New offers

    def get(self, request):
        return render(request, self.template_name, {'nbar': 'news'})


class CustomAllOfferView(TemplateView):
    template_name = 'all.html'

    def get_all(self):
        # idk
        all_entries = Offer.objects.all()

        # for offer in all_entries.iterator():
        #     print(offer.title)

        return all_entries

    # All offers
    def get(self, request):
        all_entries = self.get_all()
        return render(request, self.template_name, {'nbar': 'all', 'all_entries': all_entries})


class CustomAddOffer(TemplateView):
    template_name = 'addOffer.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(HOME_PAGE)
        form = OfferForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(HOME_PAGE)
        form = OfferForm(request.POST)

        if form.is_valid():
            addOffer = form.save(commit=False)
            addOffer.user = request.user

            today = date.today()
            d1 = today.strftime("%Y-%m-%d")
            addOffer.date_published = d1
            addOffer.votes = 0

            addOffer.save()
            return redirect(HOME_PAGE)
        else:
            messages.error(request, form.errors)
            messages.error(request, "Offer is invalid")
        form = OfferForm()
        return render(request, self.template_name, {'form': form})
