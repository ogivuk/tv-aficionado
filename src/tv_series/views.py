from django.shortcuts import render, redirect

from tv_series.models import TVSeries

def home_page(request):
    tv_series = TVSeries.objects.all()
    return render(request, 'tv-series/home.html', {'tv_series': tv_series})

def add_tv_series(request):
    # Get the TV series parameters from the GET request, if any are passed.
    name = request.GET.get('name', '').replace('-',' ')
    release_year = request.GET.get('release_year', '')
    tvdb_id = request.GET.get('tvdb_id', '')
    status_code = request.GET.get('status', '')
    
    # Form the response based on the status_code
    if status_code == "add-success":
        # The TV series has been successfully added.
        # Pass a notification and do not pass the other arguments.
        status_message = name + ' (' + release_year + ') has been successfully added.'
        return render(request, 'tv-series/add.html', {'status_message': status_message})
    if status_code == "add-fail-missing-name":
        # User did not enter the name.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the name of the TV series.'
        return render(request, 'tv-series/add.html', {'release_year': release_year, 'tvdb_id': tvdb_id, 'status_message': status_message})
    if status_code == "add-fail-missing-year":
        # User did not enter the release year.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the release year of the TV series.'
        return render(request, 'tv-series/add.html', {'name': name, 'tvdb_id': tvdb_id, 'status_message': status_message})
    if status_code == "add-fail-missing-tvdb-id":
        # User did not enter the TVDB id.
        # Pass a notification together with the other arguments.
        status_message = 'Please enter the TVDB id of the TV series.'
        return render(request, 'tv-series/add.html', {'name': name, 'release_year': release_year, 'status_message': status_message})
    if status_code == "add-fail-tv-series-exists":
        # User entered a TV series that already exists.
        # Pass a notification and do not pass the other arguments.
        status_message = name + ' (' + release_year + ') already exists.'
        return render(request, 'tv-series/add.html', {'status_message': status_message})

    # Default exist in case the status_code is not covered.
    status_message = ''
    return render(request, 'tv-series/add.html', {'name': name, 'release_year': release_year, 'tvdb_id': tvdb_id, 'status_message': status_message})

def new_tv_series(request):
    # Get the values passed with the POST request
    tv_series_name = request.POST['name']
    tv_series_redirect_name = tv_series_name.replace(' ','-')
    tv_series_release_year = request.POST['release_year']
    tv_series_tvdb_id = request.POST['tvdb_id']

    # Validate the values, all are required and cannot be empty.
    if tv_series_name == "":
        return redirect(f'/tv-series/add/?name={tv_series_redirect_name}&release_year={tv_series_release_year}&tvdb_id={tv_series_tvdb_id}&status=add-fail-missing-name')
    if tv_series_release_year == "":
        return redirect(f'/tv-series/add/?name={tv_series_redirect_name}&release_year={tv_series_release_year}&tvdb_id={tv_series_tvdb_id}&status=add-fail-missing-year')
    if tv_series_tvdb_id == "":
        return redirect(f'/tv-series/add/?name={tv_series_redirect_name}&release_year={tv_series_release_year}&tvdb_id={tv_series_tvdb_id}&status=add-fail-missing-tvdb-id')

    # Check if the entry already exists, the combination of name and release year must be unique. Of course, the tvdb id also must be unique
    if (TVSeries.objects.filter(name__iexact=tv_series_name, release_year__exact=tv_series_release_year).count() != 0 or 
        TVSeries.objects.filter(tvdb_id__exact=tv_series_tvdb_id).count() != 0):
        return redirect(f'/tv-series/add/?name={tv_series_redirect_name}&release_year={tv_series_release_year}&tvdb_id={tv_series_tvdb_id}&status=add-fail-tv-series-exists')

    # Validations passed, data are fine and unique. Create an object.
    TVSeries.objects.create(name=tv_series_name, release_year=tv_series_release_year, tvdb_id=tv_series_tvdb_id)

    # Redirect back to the page passing all the data with the success status message   
    return redirect(f'/tv-series/add/?name={tv_series_redirect_name}&release_year={tv_series_release_year}&tvdb_id={tv_series_tvdb_id}&status=add-success')

def view_tv_series(request, tv_series_id):
    tv_series = TVSeries.objects.get(pk=tv_series_id)
    return render(request, 'tv-series/view.html', {'tv_series': tv_series})

#def view_tv_series(request, tv_series_id):
#    tv_series = TVSeries.objects.get(pk=tv_series_id)
#    return render(request, 'tv-series/view.html', {'tv_series': tv_series})

def view_tv_series_name_year(request, tv_series_name_year):
    # Split the string into words by '-' as the separator
    name_in_words_and_year = tv_series_name_year.split('-')
    
    # Get the release year as the last word after the split
    release_year = name_in_words_and_year[-1]
    
    # Concatinate the name based on the remaining words
    name = name_in_words_and_year[0]
    for cnt in range(1, len(name_in_words_and_year)-1):
        name += " " + name_in_words_and_year[cnt]

    # Find the TV series with the given name and release year
    tv_series = TVSeries.objects.get(name=name, release_year=release_year)

    return view_tv_series(request, tv_series.id)
    
def update_all_tv_series(request):
    return redirect('/tv-series/')