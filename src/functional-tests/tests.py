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

    def test_can_open_tvseries_home_page(self):
        # User opens the landing page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        header_text = self.browser.find_element_by_tag_name('h1').text

        # User notices TV Aficionado in the page title, and TV Series in the page.
        self.assertIn('TV Aficionado',self.browser.title)
        self.assertIn('TV Series', header_text)

    def test_home_page_displays_tv_series_as_links_to_their_individual_pages(self):
        # Preparation: User first adds two TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys("The First TV Series")
        self.browser.find_element_by_id('id_year').send_keys("2018")
        self.browser.find_element_by_id('id_tvdb').send_keys("123456")
        self.browser.find_element_by_id('id_submit').click()
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys("The Second TV Series")
        self.browser.find_element_by_id('id_year').send_keys("2018")
        self.browser.find_element_by_id('id_tvdb').send_keys("123457")
        self.browser.find_element_by_id('id_submit').click()

        # User opens the landing page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # User sees the list of TV Series
        table = self.browser.find_element_by_id('id_tvseries_table')
        rows = table.find_elements_by_tag_name('tr')

        # User sees the first TV Series displayed as a Hyperlink
        ## rows[1] contains the first TV Series entry, rows[0] has the table header
        link = rows[1].find_element_by_tag_name('a')
        self.assertRegex(link.get_attribute("href"), r'/tv-series/')
        self.assertIn(link.text, "The First TV Series (2018)")
        # User clicks on the link and gets taken to the individual page
        link.click()
        self.assertIn("The First TV Series (2018)", self.browser.title)

        # User opens again the landing page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        table = self.browser.find_element_by_id('id_tvseries_table')
        rows = table.find_elements_by_tag_name('tr')

        # User sees the second TV Series displayed as a Hyperlink
        link = rows[2].find_element_by_tag_name('a')
        self.assertRegex(link.get_attribute("href"), r'/tv-series/')
        self.assertIn(link.text, "The Second TV Series (2018)")
        # User clicks on the link and gets taken to the individual page
        link.click()
        self.assertIn("The Second TV Series (2018)", self.browser.title)

    def test_home_page_can_update_episode_information_for_all_tv_series(self):
        # Preparation: User first adds two TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys("The First TV Series")
        self.browser.find_element_by_id('id_year').send_keys("2018")
        self.browser.find_element_by_id('id_tvdb').send_keys("123456")
        self.browser.find_element_by_id('id_submit').click()
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys("The Second TV Series")
        self.browser.find_element_by_id('id_year').send_keys("2018")
        self.browser.find_element_by_id('id_tvdb').send_keys("123457")
        self.browser.find_element_by_id('id_submit').click()
        
        # User opens the landing page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # User sees the TV Series, but with no information about the episodes
        table = self.browser.find_element_by_id('id_tvseries_table')
        rows = table.find_elements_by_tag_name('tr')
        tv_series_1_attributes = rows[1].find_elements_by_tag_name('td')
        tv_series_2_attributes = rows[2].find_elements_by_tag_name('td')

        self.assertEqual(tv_series_1_attributes[0].text, "The First TV Series (2018)")
        self.assertEqual(tv_series_1_attributes[1].text, "")
        self.assertEqual(tv_series_1_attributes[2].text, "")
        self.assertEqual(tv_series_1_attributes[3].text, "")
        self.assertEqual(tv_series_1_attributes[4].text, "")

        self.assertEqual(tv_series_2_attributes[0].text, "The Second TV Series (2018)")
        self.assertEqual(tv_series_2_attributes[1].text, "")
        self.assertEqual(tv_series_2_attributes[2].text, "")
        self.assertEqual(tv_series_2_attributes[3].text, "")
        self.assertEqual(tv_series_2_attributes[4].text, "")
        #self.assertIn(link.text, "The First TV Series (2018)")

        # User notices the a button named "Update All"
        button = self.browser.find_element_by_id('id_update_all')
        self.assertEqual(
            button.get_attribute('type'),
            "submit"
        )
        self.assertEqual(
            button.get_attribute('value'),
            "Update All"
        )
        # Finally, the user clicks on the button to add the TV series
        button.click()

        # The browser returns to the home page
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + '/tv-series/'
        )

        # User sees the TV Series with updated information
        table = self.browser.find_element_by_id('id_tvseries_table')
        rows = table.find_elements_by_tag_name('tr')
        tv_series_1_attributes = rows[1].find_elements_by_tag_name('td')
        tv_series_2_attributes = rows[2].find_elements_by_tag_name('td')

        self.assertEqual(tv_series_1_attributes[0].text, "The First TV Series (2018)")
        self.assertNotEqual(tv_series_1_attributes[1].text, "")
        self.assertNotEqual(tv_series_1_attributes[2].text, "")
        self.assertNotEqual(tv_series_1_attributes[3].text, "")
        self.assertNotEqual(tv_series_1_attributes[4].text, "")

        self.assertEqual(tv_series_2_attributes[0].text, "The Second TV Series (2018)")
        self.assertNotEqual(tv_series_2_attributes[1].text, "")
        self.assertNotEqual(tv_series_2_attributes[2].text, "")
        self.assertNotEqual(tv_series_2_attributes[3].text, "")
        self.assertNotEqual(tv_series_2_attributes[4].text, "")

class AddNewTVSeriesTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_home_page_and_go_to_add_new_tvseries_page(self):
        # User opens the landing page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # User notices a link for adding a new TV Series
        link = self.browser.find_element_by_id('id_add_tv_series')
        
        # The link displays "Add new TV Series"
        self.assertEqual(link.text,"Add new TV Series")
        # and it points to ".../tv-series/add/"
        self.assertRegex(link.get_attribute("href"), r'/tv-series/add/$')
        
        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-series/add/$')

    def test_can_open_tvseries_home_page_from_add_tvseries_page(self):
        # User opens the page for adding TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # User notices a link for going to the TV Series Home Page
        link = self.browser.find_element_by_id('id_link_to_home_page')

        # The link points to ".../tv-series/"
        self.assertRegex(link.get_attribute("href"), r'/tv-series/$')

        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-series/$')
    
    def test_can_add_tvseries_and_retrieve_it_later(self):
        # helper variables holding TV Series data
        test_tvseries_name = 'Game of Thrones'
        test_tvseries_year = '2011'
        test_tvseries_thetvdb_id = '121361'
        test_tvseries_display_name = 'Game of Thrones (2011)'
        test_tvseries_url_name = 'Game-of-Thrones-2011'
        test_tvseries_url_id = '1' # Internal IDs always start from 1
        
        # User opens the page for adding new TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user is invited to enter the name of a new TV Series
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the name of a new TV Series"
        )
        # The user enters the name of the TV Series
        inputbox.send_keys(test_tvseries_name)

        # The user is invited to enter the release year of a new TV Series
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the release year of the new TV Series"
        )
        # The user enters the release year
        inputbox.send_keys(test_tvseries_year)

        # The user is invited to enter the theTVDB unique TV Series ID
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter the unique theTVDB ID of the new TV Series"
        )
        # The user enters the id
        inputbox.send_keys(test_tvseries_thetvdb_id)

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
        # Finally, the user clicks on the button to add the TV series
        button.click()

        # The browser returns to page with adding new TV Series carrying over the data
        test_tvseries_urlarg_name = test_tvseries_name.replace(' ','-')
        self.assertEqual(
            self.browser.current_url, 
            self.live_server_url + '/tv-series/add/' 
                + f'?name={test_tvseries_urlarg_name}'
                + f'&release_year={test_tvseries_year}'
                + f'&tvdb_id={test_tvseries_thetvdb_id}'
                + '&status=add-success'
        )

        # The user observes that the entered values have not been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), '')

        # The user observes the message that the TV Series has been successfully added
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvseries_display_name + " has been successfully added.")

        # The user opens the page with all TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # The user sees the name of the TV Series in the list
        table = self.browser.find_element_by_id('id_tvseries_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(test_tvseries_name + ' (' + test_tvseries_year + ')',[row.text for row in rows])

        # The user can access the page for TV Series by name, where spaces are replaced with hyphens,
        # appended with release year.
        self.browser.get(self.live_server_url+f'/tv-series/{test_tvseries_url_name}/')

        # The user notices the name of TV Series appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(test_tvseries_display_name,self.browser.title)
        self.assertIn(test_tvseries_display_name, header_text)
        self.assertIn(test_tvseries_name, page_text)
        self.assertIn(test_tvseries_year, page_text)
        self.assertIn(test_tvseries_thetvdb_id, page_text)

        # The user can access the page for TV Series by its id
        self.browser.get(self.live_server_url+f'/tv-series/{test_tvseries_url_id}/')

        # The user notices the name of TV Series appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(test_tvseries_display_name,self.browser.title)
        self.assertIn(test_tvseries_display_name, header_text)
        self.assertIn(test_tvseries_name, page_text)
        self.assertIn(test_tvseries_year, page_text)
        self.assertIn(test_tvseries_thetvdb_id, page_text)

    def test_user_cannot_enter_duplicate_tv_series(self):
        # helper variables holding TV Series data
        test_tvseries_name = 'Game of Thrones'
        test_tvseries_year = '2011'
        test_tvseries_thetvdb_id = '121361'
        test_tvseries_display_name = 'Game of Thrones (2011)'
        
        # User opens the page with all TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # User does not see the new TV Series in the list yet
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(test_tvseries_name, page_text)

        # User opens the page for adding new TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user enters the new TV Series for the first time
        self.browser.find_element_by_id('id_name').send_keys(test_tvseries_name)
        self.browser.find_element_by_id('id_year').send_keys(test_tvseries_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message that the TV Series has been successfully added
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvseries_display_name + " has been successfully added.")
        
        # The user goes back to the starting page for TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # The user sees the new TV Series in the list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(test_tvseries_name, page_text)

        # The user opens the page for adding new TV Series for 2nd time
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user tries to enter the new TV Series for the second time
        self.browser.find_element_by_id('id_name').send_keys(test_tvseries_name)
        self.browser.find_element_by_id('id_year').send_keys(test_tvseries_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message that the TV Series already exists
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, test_tvseries_display_name + " already exists.")

        # The user observes that the values have not been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), '')
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), '')

class AddNewTVSeriesValidateInputTest(LiveServerTestCase):

    # helper variables holding TV Series data
    test_tvseries_name = 'TV Series 1'
    test_tvseries_year = '2018'
    test_tvseries_thetvdb_id = '123456'
    test_tvseries_display_name = 'TV Series 1 (2018)'
    test_tvseries_url_name = 'TV-Series-1-2018'
    test_tvseries_url_id = '1'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_input_validation_user_cannot_save_TVSeries_without_name(self):
        # User opens the page with all TV Series, and it does not see the new TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)

        # User opens the page for adding new TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user enters the new TV Series, but without its name
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvseries_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the name of the TV Series
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the name of the TV Series.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_year)
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_thetvdb_id)

        # User opens the page with all TV Series, and it still does not see the new TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)

    def test_input_validation_user_cannot_save_TVseries_without_release_year(self):
        # User opens the page with all TV Series, and it does not see the new TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)

        # User opens the page for adding new TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user enters the new TV Series, but without its release year
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvseries_name)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the release year of the TV Series
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the release year of the TV Series.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_name)
        inputbox = self.browser.find_element_by_id('id_tvdb')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_thetvdb_id)

        # User opens the page with all TV Series, and it still does not see the new TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)
    
    def test_input_validation_user_cannot_save_TVseries_without_tvdb_id(self):
        # User opens the page with all TV Series
        self.browser.get(self.live_server_url+'/tv-series/')

        # User does not see the new TV Series in the list yet
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)

        # User opens the page for adding new TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')

        # The user enters the new TV Series for the first time, but without its tvdb id
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvseries_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvseries_year)
        self.browser.find_element_by_id('id_submit').click()

        # The user observes the message to enter the TVDB id of the TV Series
        messagebox = self.browser.find_element_by_id('id_status_message')
        self.assertEqual(messagebox.text, "Please enter the TVDB id of the TV Series.")

        # The user observes that the other values have been kept
        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_name)
        inputbox = self.browser.find_element_by_id('id_year')
        self.assertEqual(inputbox.get_attribute('value'), self.test_tvseries_year)

        # User opens the page with all TV Series, and it still does not see the new TV Series
        self.browser.get(self.live_server_url+'/tv-series/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.test_tvseries_name, page_text)

class ViewTVseriesTest(LiveServerTestCase):

    # helper variables holding TV Series data
    test_tvseries_name = 'TV Series 1'
    test_tvseries_year = '2018'
    test_tvseries_thetvdb_id = '123456'
    test_tvseries_display_name = 'TV Series 1 (2018)'
    test_tvseries_url_name = 'TV-Series-1-2018'
    test_tvseries_url_id = '1'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_tvseries_view_displays_all_parameters(self):
        # First, user adds a TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvseries_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvseries_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # The user can access the page for TV Series by name, 
        # where spaces are replaced with hyphens, appended with release year.
        self.browser.get(self.live_server_url+f'/tv-series/{self.test_tvseries_url_name}/')

        # The user notices the name of TV Series appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(self.test_tvseries_display_name,self.browser.title)
        self.assertIn(self.test_tvseries_display_name, header_text)

        # The user notices the TV Series parameters
        self.assertIn(self.test_tvseries_name, page_text)
        self.assertIn(self.test_tvseries_year, page_text)
        self.assertIn(self.test_tvseries_thetvdb_id, page_text)

        # The user notices the internal ID of the TV Series, and the id is a number larger than 0
        tvseries_id = self.browser.find_element_by_id('id_tvseries_id').text

        self.assertTrue(int(tvseries_id) > 0)

        # The user can access the page for TV Series by its internal ID
        self.browser.get(self.live_server_url+f'/tv-series/{tvseries_id}/')

        # The user notices the name of TV Series appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertIn(self.test_tvseries_display_name,self.browser.title)
        self.assertIn(self.test_tvseries_display_name, header_text)
        
        # The user notices the TV Series parameters
        self.assertIn(self.test_tvseries_name, page_text)
        self.assertIn(self.test_tvseries_year, page_text)
        self.assertIn(self.test_tvseries_thetvdb_id, page_text)
        self.assertIn(tvseries_id, page_text)
        
    def test_can_open_tvseries_home_page_from_tvseries_page(self):
        # First, user adds a TV Series
        self.browser.get(self.live_server_url+'/tv-series/add/')
        self.browser.find_element_by_id('id_name').send_keys(self.test_tvseries_name)
        self.browser.find_element_by_id('id_year').send_keys(self.test_tvseries_year)
        self.browser.find_element_by_id('id_tvdb').send_keys(self.test_tvseries_thetvdb_id)
        self.browser.find_element_by_id('id_submit').click()

        # User opens the page with the TV Series information based on its name and year
        self.browser.get(self.live_server_url+f'/tv-series/{self.test_tvseries_url_name}/')

        # User notices a link for going to the TV Series Home Page
        link = self.browser.find_element_by_id('id_link_to_home_page')

        # The link points to ".../tv-series/"
        self.assertRegex(link.get_attribute("href"), r'/tv-series/$')

        # The user clicks on the link to open the page
        link.click()

        # The browser opens the page
        self.assertRegex(self.browser.current_url, r'/tv-series/$')