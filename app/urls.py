from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('home/', views.CustomHomeView.as_view(), name="home"),
    path('logout/', views.logout, name='logout'),
    path('offers/news/', views.CustomTabNewsView.as_view(), name='news'),
    path('offers/all/', views.CustomAllOfferView.as_view(), name='all'),
    path('offers/add/', views.CustomAddOffer.as_view(), name='addoffer'),
    # ex /app/offers/1
    path('offers/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('offers/upvote/<int:pk>', views.upvote, name="upvote"),
    path('offers/downvote/<int:pk>', views.downvote, name="downvote"),
]
