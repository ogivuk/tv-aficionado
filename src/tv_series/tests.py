from django.test import TestCase

from tv_series.models import TVSeries

class HomePageVisitorTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/tv-series/')
        
        self.assertTemplateUsed(response, 'tv-series/home.html')
    
    def test_displays_tv_series(self):
        TVSeries.objects.create(name = "The First TV Series", release_year = 2001, tvdb_id = 123456)
        TVSeries.objects.create(name = "The Second TV Series", release_year = 2002, tvdb_id = 123457)

        response = self.client.get("/tv-series/")

        self.assertContains(response, "The First TV Series")
        self.assertContains(response, "The Second TV Series")

    def test_update_all_tv_series(self):
        TVSeries.objects.create(name = "The First TV Series", release_year = 2001, tvdb_id = 123456)
        TVSeries.objects.create(name = "The Second TV Series", release_year = 2002, tvdb_id = 123457)

        self.fail("Finish the test")
    
    def test_redirect_after_post(self):
        response = self.client.post('/tv-series/all/update')

        self.assertRedirects(response, '/tv-series/')

class TVSeriesModelTest(TestCase):

    def test_saving_and_retrieving_tvseries(self):
        first_tvseries = TVSeries()
        first_tvseries.name = "The First TV Series"
        first_tvseries.release_year = 2001
        first_tvseries.tvdb_id = 123456
        first_tvseries.save()

        second_tvseries = TVSeries()
        second_tvseries.name = "The Second TV Series"
        second_tvseries.release_year = 2002
        second_tvseries.tvdb_id = 123457
        second_tvseries.save()

        saved_tvseries = TVSeries.objects.all()

        self.assertEqual(saved_tvseries.count(), 2)

        first_saved_tvseries = saved_tvseries[0]
        second_saved_tvseries = saved_tvseries[1]

        self.assertEqual(first_saved_tvseries.name, "The First TV Series")
        self.assertEqual(first_saved_tvseries.release_year, 2001)
        self.assertEqual(first_saved_tvseries.tvdb_id, 123456)
        self.assertEqual(second_saved_tvseries.name, "The Second TV Series")
        self.assertEqual(second_saved_tvseries.release_year, 2002)
        self.assertEqual(second_saved_tvseries.tvdb_id, 123457)

class AddNewTVSeriesTest(TestCase):

    def test_tv_series_add_uses_correct_template(self):
        response = self.client.get('/tv-series/add/')
        
        self.assertTemplateUsed(response, 'tv-series/add.html')

    def test_tv_series_add_can_save_a_POST_request(self):
        self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': 2018, 'tvdb_id': 123456})

        self.assertEqual(TVSeries.objects.count(), 1)
        new_tvseries = TVSeries.objects.first()
        self.assertEqual(new_tvseries.name, 'TV Series 1')
        self.assertEqual(new_tvseries.release_year, 2018)
        self.assertEqual(new_tvseries.tvdb_id, 123456)

    def test_redirect_after_post(self):
        response = self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': 2018, 'tvdb_id': 123456})

        self.assertRedirects(response, '/tv-series/add/?name=TV-Series-1&release_year=2018&tvdb_id=123456&status=add-success')

    def test_tv_series_add_can_display_status_message(self):
        response = self.client.get('/tv-series/add/?name=TV-Series-1&release_year=2018&tvdb_id=123456&status=add-success')
        
        self.assertContains(response, "TV Series 1 (2018) has been successfully added.")

    def test_tv_series_add_does_not_display_parameters_when_successful(self):
        response = self.client.get('/tv-series/add/?name=TV-Series-1&release_year=2018&tvdb_id=123456&status=add-success')
        
        self.assertNotContains(response, "123456")

class AddTVSeriesInputValidationTest(TestCase):

    def test_post_does_not_save_new_tv_series_without_name_filled_in(self):
        self.client.post('/tv-series/new', data={'name': '', 'release_year': '2018', 'tvdb_id': '123456'})

        self.assertEqual(TVSeries.objects.count(), 0)

    def test_post_does_not_save_new_tv_series_without_release_year_filled_in(self):
        self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': '', 'tvdb_id': '123456'})
        
        self.assertEqual(TVSeries.objects.count(), 0)

    def test_post_does_not_save_new_tv_series_without_tvdb_id_filled_in(self):
        self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': '2018', 'tvdb_id': ''})

        self.assertEqual(TVSeries.objects.count(), 0)

    def test_post_does_not_save_new_tv_series_with_already_existing_name_and_release_year(self):
        self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': '2018', 'tvdb_id': '123456'})
        self.assertEqual(TVSeries.objects.count(), 1)
        
        self.client.post('/tv-series/new', data={'name': 'TV Series 1', 'release_year': '2018', 'tvdb_id': '123456'})
        self.assertEqual(TVSeries.objects.count(), 1)

    def test_tv_series_add_does_not_display_parameters_when_duplicate(self):
        response = self.client.get('/tv-series/add/?name=TV-Series-1&release_year=2018&tvdb_id=123456&status=add-fail-tv-series-exists')
        
        self.assertNotContains(response, "123456")

    def test_tv_series_add_displays_parameters_when_missing_name(self):
        response = self.client.get('/tv-series/add/?name=&release_year=2018&tvdb_id=123456&status=add-fail-missing-name')
        
        self.assertContains(response, "2018")
        self.assertContains(response, "123456")

    def test_tv_series_add_displays_parameters_when_missing_release_year(self):
        response = self.client.get('/tv-series/add/?name=TV-Series-1&release_year=&tvdb_id=123456&status=add-fail-missing-year')
        
        self.assertContains(response, "TV Series 1")
        self.assertContains(response, "123456")

    def test_tv_series_add_displays_parameters_when_missing_tvdb_id(self):
        response = self.client.get('/tv-series/add/?name=TV-Series-1&release_year=2018&tvdb_id=&status=add-fail-missing-tvdb-id')
        
        self.assertContains(response, "TV Series 1")
        self.assertContains(response, "2018")

class ViewTVSeriesInfoTest(TestCase):
    # Helper variables containing TV series info for tests
    test_tv_series_name = "The First TV Series"
    test_tv_series_year = 2001
    test_tv_series_tvdb_id = 123456
    test_tv_series_display_url = "The-First-TV-Series-2001"

    def are_all_tv_series_info_displayed(self, response, new_tv_series):
        self.assertContains(response, new_tv_series.id)
        self.assertContains(response, new_tv_series.name)
        self.assertContains(response, new_tv_series.release_year)
        self.assertContains(response, new_tv_series.tvdb_id)

    def test_tv_series_view_uses_correct_template(self):
        new_tv_series = TVSeries.objects.create(name = "The First TV Series", release_year = 2001, tvdb_id = 123456)

        response = self.client.get(f'/tv-series/{new_tv_series.id}/')
        
        self.assertTemplateUsed(response,'tv-series/view.html')

    def test_tv_series_info_on_separate_page_based_on_name_and_release_year(self):
        new_tv_series = TVSeries.objects.create(name = self.test_tv_series_name, release_year = self.test_tv_series_year, tvdb_id = self.test_tv_series_tvdb_id)

        response = self.client.get(f'/tv-series/{self.test_tv_series_display_url}/')

        self.are_all_tv_series_info_displayed(response, new_tv_series)

    def test_tv_series_info_on_separate_page_based_on_id(self):
        new_tv_series = TVSeries.objects.create(name = self.test_tv_series_name, release_year = self.test_tv_series_year, tvdb_id = self.test_tv_series_tvdb_id)

        response = self.client.get(f'/tv-series/{new_tv_series.id}/')
        
        self.are_all_tv_series_info_displayed(response, new_tv_series)
