from django.shortcuts import render, redirect

from tv_show.models import TVShow

def home_page(request):
    tv_shows = TVShow.objects.all()
    #return render(request,'tournament.html', {'tournament': tournament})
    return render(request, 'tv-show/home.html', {'tv_shows': tv_shows})

def add_tv_show(request):
    return render(request, 'tv-show/add.html')

def new_tv_show(request):
    TVShow.objects.create(name=request.POST['name'], release_year=request.POST['release_year'], tvdb_id=request.POST['tvdb_id'])
    return redirect(f'/tv-show/')