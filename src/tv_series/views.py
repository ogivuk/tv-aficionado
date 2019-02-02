from django.shortcuts import render, redirect

from tv_show.models import TVShow

def home_page(request):
    tv_shows = TVShow.objects.all()
    return render(request, 'tv-show/home.html', {'tv_shows': tv_shows})

def add_tv_show(request):
    # Get the TV show parameters from the GET request, if any are passed.
    name = request.GET.get('name', '').replace('-',' ')
    release_year = request.GET.get('release_year', '')
    tvdb_id = request.GET.get('tvdb_id', '')
    status_code = request.GET.get('status', '')
    
    # Form the response based on the status_code
    if status_code == "add-success":
        # The TV show has been successfully added.
        # Pass a notification and do not pass the other arguments.
        status_message = name + ' (' + release_year + ') has been successfully added.'
        return render(request, 'tv-show/add.html', {'status_message': status_message})
    if status_code == "add-fail-missing-name":
        # User did not enter the name.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the name of the TV show.'
        return render(request, 'tv-show/add.html', {'release_year': release_year, 'tvdb_id': tvdb_id, 'status_message': status_message})
    if status_code == "add-fail-missing-year":
        # User did not enter the release year.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the release year of the TV show.'
        return render(request, 'tv-show/add.html', {'name': name, 'tvdb_id': tvdb_id, 'status_message': status_message})
    if status_code == "add-fail-missing-tvdb-id":
        # User did not enter the TVDB id.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the TVDB id of the TV show.'
        return render(request, 'tv-show/add.html', {'name': name, 'release_year': release_year, 'status_message': status_message})
    if status_code == "add-fail-tv-show-exists":
        # User entered a TV show that already exists.
        # Pass a notification and do not pass the other arguments.
        status_message = name + ' (' + release_year + ') already exists.'
        return render(request, 'tv-show/add.html', {'status_message': status_message})

    # Default exist in case the status_code is not covered.
    status_message = ''
    return render(request, 'tv-show/add.html', {'name': name, 'release_year': release_year, 'tvdb_id': tvdb_id, 'status_message': status_message})

def new_tv_show(request):
    # Get the values passed with the POST request
    tv_show_name = request.POST['name']
    tv_show_redirect_name = tv_show_name.replace(' ','-')
    tv_show_release_year = request.POST['release_year']
    tv_show_tvdb_id = request.POST['tvdb_id']

    # Validate the values, all are required and cannot be empty.
    if tv_show_name == "":
        return redirect(f'/tv-show/add/?name={tv_show_redirect_name}&release_year={tv_show_release_year}&tvdb_id={tv_show_tvdb_id}&status=add-fail-missing-name')
    if tv_show_release_year == "":
        return redirect(f'/tv-show/add/?name={tv_show_redirect_name}&release_year={tv_show_release_year}&tvdb_id={tv_show_tvdb_id}&status=add-fail-missing-year')
    if tv_show_tvdb_id == "":
        return redirect(f'/tv-show/add/?name={tv_show_redirect_name}&release_year={tv_show_release_year}&tvdb_id={tv_show_tvdb_id}&status=add-fail-missing-tvdb-id')

    # Check if the entry already exists, the combination of name and release year must be unique. Of course, the tvdb id also must be unique
    if (TVShow.objects.filter(name__iexact=tv_show_name, release_year__exact=tv_show_release_year).count() != 0 or 
        TVShow.objects.filter(tvdb_id__exact=tv_show_tvdb_id).count() != 0):
        return redirect(f'/tv-show/add/?name={tv_show_redirect_name}&release_year={tv_show_release_year}&tvdb_id={tv_show_tvdb_id}&status=add-fail-tv-show-exists')

    # Validations passed, data are fine and unique. Create an object.
    TVShow.objects.create(name=tv_show_name, release_year=tv_show_release_year, tvdb_id=tv_show_tvdb_id)

    # Redirect back to the page passing all the data with the success status message   
    return redirect(f'/tv-show/add/?name={tv_show_redirect_name}&release_year={tv_show_release_year}&tvdb_id={tv_show_tvdb_id}&status=add-success')

def view_tv_show(request, tv_show_id):
    tv_show = TVShow.objects.get(pk=tv_show_id)
    return render(request, 'tv-show/view.html', {'tv_show': tv_show})

def view_tv_show(request, tv_show_id):
    tv_show = TVShow.objects.get(pk=tv_show_id)
    return render(request, 'tv-show/view.html', {'tv_show': tv_show})

def view_tv_show_name_year(request, tv_show_name_year):
    # Split the string into words by '-' as the separator
    name_in_words_and_year = tv_show_name_year.split('-')
    
    # Get the release year as the last word after the split
    release_year = name_in_words_and_year[-1]
    
    # Concatinate the name based on the remaining words
    name = name_in_words_and_year[0]
    for cnt in range(1, len(name_in_words_and_year)-1):
        name += " " + name_in_words_and_year[cnt]

    # Find the TV show with the given name and release year
    tv_show = TVShow.objects.get(name=name, release_year=release_year)

    return view_tv_show(request, tv_show.id)
    
def update_all_tv_shows(request):
    return redirect('/tv-show/')