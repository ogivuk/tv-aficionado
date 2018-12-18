from django.shortcuts import render

def home_page(request):
    return render(request, 'tv-show/home.html')

def add_tv_show(request):
    return render(request, 'tv-show/add.html')