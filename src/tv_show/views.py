from django.shortcuts import render

def home_page(request):
    return render(request, 'tv-show/home.html')