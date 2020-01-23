from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, it's pepper.");


def signUp(request):
    return HttpResponse("Sign up")


def signIn(request):
    return HttpResponse("Sign in")