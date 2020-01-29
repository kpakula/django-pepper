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
    path('offers/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('offers/<int:pk>/update/', views.OfferUpdateView, name='update'),
    path('offers/<int:pk>/delete/', views.OfferDeleteView, name='delete'),
    path('offers/upvote/<int:pk>', views.upvote, name="upvote"),
    path('offers/downvote/<int:pk>', views.downvote, name="downvote"),
    path('offers/my/', views.CustomMyOfferView.as_view(), name="myview"),
]
