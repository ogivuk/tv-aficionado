from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class HomePageVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_tvshow_home_page(self):
        # User opens the landing page for TV Shows
        self.browser.get(self.live_server_url+'/tv-show/')
        header_text = self.browser.find_element_by_tag_name('h1').text

        # User notices TV Aficionado in the page title, and TV Shows in the page.
        self.assertIn('TV Aficionado',self.browser.title)
        self.assertIn('TV Shows', header_text)

class AddNewTVShowTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_home_page_and_go_to_add_new_tvshow_page(self):
        # User opens the landing page for TV Shows
        self.browser.get(self.live_server_url+'/tv-show/')

        # User notices a link for adding a new TV Show
        link = self.browser.find_element_by_id('id_add_tv_show')
        
        # The link displays "Add new TV Show"
        self.assertEqual(link.text,"Add new TV Show")
        # and it points to ".../tv-show/add/"
        self.assertRegex(link.get_attribute("href"), r'/tv-show/add/$')
        
        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-show/add/$')

    def test_can_open_tvshow_home_page_from_add_tvshow_page(self):
        # User opens the page for adding TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # User notices a link for going to the TV Show Home Page
        link = self.browser.find_element_by_id('id_link_to_home_page')

        # The link points to ".../tv-show/"
        self.assertRegex(link.get_attribute("href"), r'/tv-show/$')

        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-show/$')
    
    def test_can_add_tvshow_and_retrieve_it_later(self):
        # helper variables holding TV show data
        test_tvshow_name = 'Game of Thrones'
        test_tvshow_year = '2011'
        test_tvshow_thetvdb_id = '121361'
        test_tvshow_display_name = 'Game of Thrones (2011)'
        test_tvshow_url_name = 'Game-of-Thrones-2011'
        test_tvshow_url_id = '1' # Internal IDs always start from 1
        
        # User opens the page for adding new TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user is invited to enter the name of a new TV show
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the name of a new TV show"
        )
        # The user enters the name of the TV show
        inputbox.send_keys(test_tvshow_name)

        # The user is invited to enter the release year of a new TV show
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the release year of the new TV show"
        )
        # The user enters the release year
        inputbox.send_keys(test_tvshow_year)

        # The user is invited to enter the theTVDB unique TV show ID
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the unique theTVDB ID of the new TV show"
        )
        # The user enters the id
        inputbox.send_keys(test_tvshow_thetvdb_id)

        # The user notices the a button named "Add"
        button = self.browser.find_element_by_id('id_submit')
        self.assertEqual(
            button.get_attribute('type'),
            "submit"
        )
        self.assertEqual(
            button.get_attribute('value'),
            "Add"
        )
        # Finally, the user clicks on the button to add the show
        button.click()

        # The browser returns to page with adding new TV shows carrying over the data
        test_tvshow_urlarg_name = test_tvshow_name.replace(' ','-')
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + '/tv-show/add/' 
                + f'?name={test_tvshow_urlarg_name}'
                + f'&release_year={test_tvshow_year}'
                + f'&tvdb_id={test_tvshow_thetvdb_id}'
                + '&status=add-success'
        )

        # The user observes that the entered values have not been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), '')

        # The user observes the message that the TV show has been successfully added
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvshow_display_name + " has been successfully added.")

        # The user opens the page with all TV shows
        self.browser.get(self.live_server_url+'/tv-show/')

        # The user sees the name of the TV show in the list
        table = self.browser.find_element_by_id('id_tvshows_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(test_tvshow_name + ' (' + test_tvshow_year + ')',[row.text for row in rows])

        # The user can access the page for TV show by name, where spaces are replaced with hyphens,
        # appended with release year.
        self.browser.get(self.live_server_url+f'/tv-show/{test_tvshow_url_name}/')

        # The user notices the name of TV show appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(test_tvshow_display_name,self.browser.title)
        self.assertIn(test_tvshow_display_name, header_text)
        self.assertIn(test_tvshow_name, page_text)
        self.assertIn(test_tvshow_year, page_text)
        self.assertIn(test_tvshow_thetvdb_id, page_text)

        # The user can access the page for TV show by its id
        self.browser.get(self.live_server_url+f'/tv-show/{test_tvshow_url_id}/')

        # The user notices the name of TV show appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(test_tvshow_display_name,self.browser.title)
        self.assertIn(test_tvshow_display_name, header_text)
        self.assertIn(test_tvshow_name, page_text)
        self.assertIn(test_tvshow_year, page_text)
        self.assertIn(test_tvshow_thetvdb_id, page_text)

    def test_user_cannot_enter_duplicate_tv_show(self):
        # helper variables holding TV show data
        test_tvshow_name = 'Game of Thrones'
        test_tvshow_year = '2011'
        test_tvshow_thetvdb_id = '121361'
        test_tvshow_display_name = 'Game of Thrones (2011)'
        test_tvshow_url_name = 'Game-of-Thrones-2011'
        test_tvshow_url_id = '1'
        
        # User opens the page with all TV shows
        self.browser.get(self.live_server_url+'/tv-show/')

        # User does not see the new TV show in the list yet
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(test_tvshow_name, page_text)

        # User opens the page for adding new TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user enters the new TV show for the first time
        self.browser.find_element_by_id('id_name').send_keys(test_tvshow_name)
        self.browser.find_element_by_id('id_year').send_keys(test_tvshow_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message that the TV show has been successfully added
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvshow_display_name + " has been successfully added.")
        
        # The user goes back to the starting page for TV shows
        self.browser.get(self.live_server_url+'/tv-show/')

        # The user sees the new TV show in the list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(test_tvshow_name, page_text)

        # The user opens the page for adding new TV Shows for 2nd time
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user tries to enter the new TV show for the second time
        self.browser.find_element_by_id('id_name').send_keys(test_tvshow_name)
        self.browser.find_element_by_id('id_year').send_keys(test_tvshow_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message that the TV show already exists
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvshow_display_name + " already exists.")

        # The user observes that the values have not been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), '')

class AddNewTVShowValidateInputTest(LiveServerTestCase):

    # helper variables holding TV show data
    test_tvshow_name = 'TV Show 1'
    test_tvshow_year = '2018'
    test_tvshow_thetvdb_id = '123456'
    test_tvshow_display_name = 'TV Show 1 (2018)'
    test_tvshow_url_name = 'TV-Show-1-2018'
    test_tvshow_url_id = '1'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_input_validation_user_cannot_save_TVshow_without_name(self):
        # User opens the page with all TV shows, and it does not see the new TV show
        self.browser.get(self.live_server_url+'/tv-show/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)

        # User opens the page for adding new TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user enters the new TV show, but without its name
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvshow_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the name of the TV show
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the name of the TV show.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_year)
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_thetvdb_id)

        # User opens the page with all TV shows, and it still does not see the new TV show
        self.browser.get(self.live_server_url+'/tv-show/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)

    def test_input_validation_user_cannot_save_TVshow_without_release_year(self):
        # User opens the page with all TV shows, and it does not see the new TV show
        self.browser.get(self.live_server_url+'/tv-show/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)

        # User opens the page for adding new TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user enters the new TV show, but without its release year
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvshow_name)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the release year of the TV show
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the release year of the TV show.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_name)
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_thetvdb_id)

        # User opens the page with all TV shows, and it still does not see the new TV show
        self.browser.get(self.live_server_url+'/tv-show/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)
    
    def test_input_validation_user_cannot_save_TVshow_without_tvdb_id(self):
        # User opens the page with all TV shows
        self.browser.get(self.live_server_url+'/tv-show/')

        # User does not see the new TV show in the list yet
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)

        # User opens the page for adding new TV Shows
        self.browser.get(self.live_server_url+'/tv-show/add/')

        # The user enters the new TV show for the first time, but without its tvdb id
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvshow_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvshow_year)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the TVDB id of the TV show
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the TVDB id of the TV show.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_name)
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvshow_year)

        # User opens the page with all TV shows, and it still does not see the new TV show
        self.browser.get(self.live_server_url+'/tv-show/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvshow_name, page_text)

class ViewTVShowTest(LiveServerTestCase):

    # helper variables holding TV show data
    test_tvshow_name = 'TV Show 1'
    test_tvshow_year = '2018'
    test_tvshow_thetvdb_id = '123456'
    test_tvshow_display_name = 'TV Show 1 (2018)'
    test_tvshow_url_name = 'TV-Show-1-2018'
    test_tvshow_url_id = '1'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_tvshow_view_displays_all_parameters(self):
        # First, user adds a TV show
        self.browser.get(self.live_server_url+'/tv-show/add/')
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvshow_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvshow_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user can access the page for TV show by name, 
        # where spaces are replaced with hyphens, appended with release year.
        self.browser.get(self.live_server_url+f'/tv-show/{self.test_tvshow_url_name}/')

        # The user notices the name of TV show appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(self.test_tvshow_display_name,self.browser.title)
        self.assertIn(self.test_tvshow_display_name, header_text)

        # The user notices the TV show parameters
        self.assertIn(self.test_tvshow_name, page_text)
        self.assertIn(self.test_tvshow_year, page_text)
        self.assertIn(self.test_tvshow_thetvdb_id, page_text)

        # The user notices the internal ID of the TV Show, and the id is a number larger than 0
        tvshow_id = self.browser.find_element_by_id('id_tvshow_id').text

        self.assertTrue(int(tvshow_id) > 0)

        # The user can access the page for TV show by its internal ID
        self.browser.get(self.live_server_url+f'/tv-show/{tvshow_id}/')

        # The user notices the name of TV show appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(self.test_tvshow_display_name,self.browser.title)
        self.assertIn(self.test_tvshow_display_name, header_text)
        
        # The user notices the TV show parameters
        self.assertIn(self.test_tvshow_name, page_text)
        self.assertIn(self.test_tvshow_year, page_text)
        self.assertIn(self.test_tvshow_thetvdb_id, page_text)
        self.assertIn(tvshow_id, page_text)
        
    def test_can_open_tvshow_home_page_from_tvshow_page(self):
        # First, user adds a TV show
        self.browser.get(self.live_server_url+'/tv-show/add/')
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvshow_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvshow_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvshow_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # User opens the page with the TV show information based on its name and year
        self.browser.get(self.live_server_url+f'/tv-show/{self.test_tvshow_url_name}/')

        # User notices a link for going to the TV Show Home Page
        link = self.browser.find_element_by_id('id_link_to_home_page')

        # The link points to ".../tv-show/"
        self.assertRegex(link.get_attribute("href"), r'/tv-show/$')

        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-show/$')