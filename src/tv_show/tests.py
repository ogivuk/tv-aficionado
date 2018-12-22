from django.test import TestCase

from tv_show.models import TVShow

# Create your tests here.

class HomePageVisitorTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/tv-show/')
        
        self.assertTemplateUsed(response,'tv-show/home.html')
    
    def test_displays_tv_shows(self):
        TVShow.objects.create(name = "The First TV Show", release_year = 2001, tvdb_id = 123456)
        TVShow.objects.create(name = "The Second TV Show", release_year = 2002, tvdb_id = 123457)

        response = self.client.get("/tv-show/")

        self.assertContains(response, "The First TV Show")
        self.assertContains(response, "The Second TV Show")

class TVShowModelTest(TestCase):

    def test_saving_and_retrieving_tvshows(self):
        first_tvshow = TVShow()
        first_tvshow.name = "The First TV Show"
        first_tvshow.release_year = 2001
        first_tvshow.tvdb_id = 123456
        first_tvshow.save()

        second_tvshow = TVShow()
        second_tvshow.name = "The Second TV Show"
        second_tvshow.release_year = 2002
        second_tvshow.tvdb_id = 123457
        second_tvshow.save()

        saved_tvshows = TVShow.objects.all()

        self.assertEqual(saved_tvshows.count(), 2)

        first_saved_tvshow = saved_tvshows[0]
        second_saved_tvshow = saved_tvshows[1]

        self.assertEqual(first_saved_tvshow.name, "The First TV Show")
        self.assertEqual(first_saved_tvshow.release_year, 2001)
        self.assertEqual(first_saved_tvshow.tvdb_id, 123456)
        self.assertEqual(second_saved_tvshow.name, "The Second TV Show")
        self.assertEqual(second_saved_tvshow.release_year, 2002)
        self.assertEqual(second_saved_tvshow.tvdb_id, 123457)

class AddNewTVShowTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get('/tv-show/add/')
        
        self.assertTemplateUsed(response,'tv-show/add.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': 2018, 'tvdb_id': 123456})

        self.assertEqual(TVShow.objects.count(), 1)
        new_tvshow = TVShow.objects.first()
        self.assertEqual(new_tvshow.name, 'TV Show 1')
        self.assertEqual(new_tvshow.release_year, 2018)
        self.assertEqual(new_tvshow.tvdb_id, 123456)

    def test_redirect_after_post(self):
        response = self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': 2018, 'tvdb_id': 123456})

        new_tvshow = TVShow.objects.first()
        self.assertRedirects(response, '/tv-show/')

class AddTVShowInputValidationTest(TestCase):

    def test_must_have_all_fields_filled_in(self):
        pass