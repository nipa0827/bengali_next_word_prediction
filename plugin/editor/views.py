from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'index.html')


def open(request):
    return render(request, 'open.html')


def new(request):
    return render(request, 'new.html')


def download(request):
    return render(request, 'download.html')


def about(request):
    return render(request, 'about.html')
