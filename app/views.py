from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView, UpdateView, DeleteView
from app.forms import LoginForm, OfferForm
from datetime import date
from .models import Offer
# Create your views here.
from django.views import generic
from django.shortcuts import get_object_or_404

HOME_PAGE = '/app/home/'


def index(request):
    return redirect(HOME_PAGE)


def upvote(request, pk):
    if not request.user.is_authenticated:
        return redirect(HOME_PAGE)
    # return render(request, 'offer', {})
    obj = Offer.objects.get(id=pk)
    obj.votes += 1
    obj.save()
    return redirect('/app/offers/'+str(pk))


def downvote(request, pk):
    obj = Offer.objects.get(id=pk)
    obj.votes -= 1
    obj.save()
    return redirect('/app/offers/'+str(pk))


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

def OfferDeleteView(request, pk):
    instance = Offer.objects.get(id=pk)
    instance.delete()
        
    return redirect('/app/offers/my')




def OfferUpdateView(request, pk):

    # post = get_object_or_404(Offer, 6)\
    if request.method == "POST":
        oD = Offer.objects.all()
        offer = oD.filter(id=pk)[0]
        form = OfferForm(request.POST)

        if form.is_valid():
            form = OfferForm(instance=offer)
            post = form.save(commit=False)
            
            post.user = request.user
            post.votes = offer.votes

            post.description = request.POST.get("description")
            post.date_start = request.POST.get("date_start")
            post.date_end = request.POST.get("date_end")
            post.title = request.POST.get("title")
            post.old_price = request.POST.get("old_price")
            post.price = request.POST.get("price")
            post.link = request.POST.get("link")
            post.link_to_image = request.POST.get("link_to_image")
            
            today = date.today()
            d1 = today.strftime("%Y-%m-%d")
            post.date_published = d1
            
            print(request.POST.get('title'))
            post.save()
            return redirect('/app/offers/'+ str(pk))
    else:
        oD = Offer.objects.all()
        offer = oD.filter(id=pk)[0]
        form = OfferForm(instance=offer)
    template = "update_view.html"
    context= {'form': form }
    return render(request, template, context)
    
    
    




class CustomHomeView(TemplateView):
    template_name = 'home.html'
    # Hot offers
    def get_all_by_votes(self):
        all_objects = Offer.objects.all()
        all_entries = all_objects.filter(votes__gte=150)[:10]
        return all_entries

    def get(self, request):
        all_entries = self.get_all_by_votes()

        return render(request, self.template_name, {'nbar': 'home', 'all_entries': all_entries})
    
    
class CustomMyOfferView(TemplateView):
    template_name = 'myoffers.html'
    # My offers
    def get_my_offers(self, request):
        all_objects = Offer.objects.all()
        all_entries = all_objects.filter(user=request.user)
        return all_entries

    def get(self, request):
        all_entries = self.get_my_offers(request)

        return render(request, self.template_name, {'all_entries': all_entries})


class CustomTabNewsView(TemplateView):
    template_name = 'news.html'
    
    def get_all_by_date(self):
        all_entries = Offer.objects.all().order_by('date_published')[:20]
        return all_entries
    
    def get(self, request):
        all_entries = self.get_all_by_date()
        return render(request, self.template_name, {'nbar': 'news', 'all_entries': all_entries})


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
    
    
# class CustomNewsOfferView(TemplateView):
#     template_name = 'news.html'
    
#     def get_all_by_date(self):
#         all_entries = Offer.objects.all().order_by('date_published')
    
    
#     def get(self, request):
#         all_entries = self.get_all_by_date()
#         return render(request, self.template_name, {})


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
