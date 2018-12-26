from django.test import TestCase

from tv_show.models import TVShow

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

    def test_tv_show_add_uses_correct_template(self):
        response = self.client.get('/tv-show/add/')
        
        self.assertTemplateUsed(response,'tv-show/add.html')

    def test_tv_show_add_can_save_a_POST_request(self):
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': 2018, 'tvdb_id': 123456})

        self.assertEqual(TVShow.objects.count(), 1)
        new_tvshow = TVShow.objects.first()
        self.assertEqual(new_tvshow.name, 'TV Show 1')
        self.assertEqual(new_tvshow.release_year, 2018)
        self.assertEqual(new_tvshow.tvdb_id, 123456)

    def test_redirect_after_post(self):
        response = self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': 2018, 'tvdb_id': 123456})

        self.assertRedirects(response, '/tv-show/add/?name=TV-Show-1&release_year=2018&tvdb_id=123456&status=add-success')

    def test_tv_show_add_can_display_status_message(self):
        response = self.client.get('/tv-show/add/?name=TV-Show-1&release_year=2018&tvdb_id=123456&status=add-success')
        
        self.assertContains(response, "TV Show 1 (2018) has been successfully added.")

    def test_tv_show_add_does_not_display_parameters_when_successful(self):
        response = self.client.get('/tv-show/add/?name=TV-Show-1&release_year=2018&tvdb_id=123456&status=add-success')
        
        self.assertNotContains(response, "123456")

class AddTVShowInputValidationTest(TestCase):

    def test_post_does_not_save_new_tv_show_without_name_filled_in(self):
        self.client.post('/tv-show/new', data={'name': '', 'release_year': '2018', 'tvdb_id': '123456'})

        self.assertEqual(TVShow.objects.count(), 0)

    def test_post_does_not_save_new_tv_show_without_release_year_filled_in(self):
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': '', 'tvdb_id': '123456'})
        
        self.assertEqual(TVShow.objects.count(), 0)

    def test_post_does_not_save_new_tv_show_without_tvdb_id_filled_in(self):
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': '2018', 'tvdb_id': ''})

        self.assertEqual(TVShow.objects.count(), 0)

    def test_post_does_not_save_new_tv_show_with_already_existing_name_and_release_year(self):
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': '2018', 'tvdb_id': '123456'})
        self.assertEqual(TVShow.objects.count(), 1)
        
        self.client.post('/tv-show/new', data={'name': 'TV Show 1', 'release_year': '2018', 'tvdb_id': '123456'})
        self.assertEqual(TVShow.objects.count(), 1)

    def test_tv_show_add_does_not_display_parameters_when_duplicate(self):
        response = self.client.get('/tv-show/add/?name=TV-Show-1&release_year=2018&tvdb_id=123456&status=add-fail-tv-show-exists')
        
        self.assertNotContains(response, "123456")

    def test_tv_show_add_displays_parameters_when_missing_name(self):
        response = self.client.get('/tv-show/add/?name=&release_year=2018&tvdb_id=123456&status=add-fail-missing-name')
        
        self.assertContains(response, "2018")
        self.assertContains(response, "123456")

    def test_tv_show_add_displays_parameters_when_missing_release_year(self):
        response = self.client.get('/tv-show/add/?name=TV-Show-1&release_year=&tvdb_id=123456&status=add-fail-missing-year')
        
        self.assertContains(response, "TV Show 1")
        self.assertContains(response, "123456")

    def test_tv_show_add_displays_parameters_when_missing_tvdb_id(self):
        response = self.client.get('/tv-show/add/?name=TV-Show-1&release_year=2018&tvdb_id=&status=add-fail-missing-tvdb-id')
        
        self.assertContains(response, "TV Show 1")
        self.assertContains(response, "2018")

class ViewTVShowInfoTest(TestCase):
    # Helper variables containing TV show info for tests
    test_tv_show_name = "The First TV Show"
    test_tv_show_year = 2001
    test_tv_show_tvdb_id = 123456
    test_tv_show_display_url = "The-First-TV-Show-2001"

    def are_all_tv_show_info_displayed(self, response, new_tv_show):
        self.assertContains(response, new_tv_show.id)
        self.assertContains(response, new_tv_show.name)
        self.assertContains(response, new_tv_show.release_year)
        self.assertContains(response, new_tv_show.tvdb_id)

    def test_tv_show_view_uses_correct_template(self):
        new_tv_show = TVShow.objects.create(name = "The First TV Show", release_year = 2001, tvdb_id = 123456)

        response = self.client.get(f'/tv-show/{new_tv_show.id}/')
        
        self.assertTemplateUsed(response,'tv-show/view.html')

    def test_tv_show_info_on_separate_page_based_on_name_and_release_year(self):
        new_tv_show = TVShow.objects.create(name = self.test_tv_show_name, release_year = self.test_tv_show_year, tvdb_id = self.test_tv_show_tvdb_id)

        response = self.client.get(f'/tv-show/{self.test_tv_show_display_url}/')

        self.are_all_tv_show_info_displayed(response, new_tv_show)

    def test_tv_show_info_on_separate_page_based_on_id(self):
        new_tv_show = TVShow.objects.create(name = self.test_tv_show_name, release_year = self.test_tv_show_year, tvdb_id = self.test_tv_show_tvdb_id)

        response = self.client.get(f'/tv-show/{new_tv_show.id}/')
        
        self.are_all_tv_show_info_displayed(response, new_tv_show)
