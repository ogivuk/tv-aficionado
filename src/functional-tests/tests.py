from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class VisitorTest(LiveServerTestCase):
    
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

    def test_can_add_tvshow_and_retrieve_it_later(self):
        # helper variables holding TV show data
        test_tvshow_name = 'Game of Thrones'
        test_tvshow_year = '2011'
        test_tvshow_thetvdb_id = '121361'
        test_tvshow_display_name = 'Game of Thrones (2011)'
        test_tvshow_url_name = 'Game-of-Thrones-2011'
        test_tvshow_url_id = test_tvshow_thetvdb_id
        
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

        # The browser returns to the starting page for TV shows
        self.assertEqual(self.browser.current_url, self.live_server_url+'/tv-show/')

        # The user sees the name of the TV show in the list
        table = self.browser.find_element_by_id('id_tvshows_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(test_tvshow_name + ' (' + test_tvshow_year + ')',[row.text for row in rows])

        # The user can access the page for TV show by name
        self.browser.get(self.live_server_url+f'/tv-show/{test_tvshow_url_name}/')

        # The user notices the name of TV show in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(test_tvshow_display_name,self.browser.title)
        self.assertIn(test_tvshow_display_name, header_text)

        # The user can access the page for TV show by name, where spaces are replaced with hyphens,
        # appended with release year.
        self.browser.get(self.live_server_url+f'/tv-show/{test_tvshow_url_name}/')

        # The user notices the name of TV show appended with release year in brackets in the page title and in the first <h1> tag
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(test_tvshow_display_name,self.browser.title)
        self.assertIn(test_tvshow_display_name, header_text)

        self.assertIn(test_tvshow_name, self.browser.toString())
        self.assertIn(test_tvshow_year, self.browser.toString())
        self.assertIn(test_tvshow_thetvdb_id, self.browser.toString())

        # The user can access the page for TV show by its id

        self.fail("Finish the test")

    # def test_user_cannot_enter_duplicate_tv_show(self):


#     def wait_for_row_in_list_table(self, row_text):
#         start_time = time.time()
#         while True:
#             try:
#                 table = self.browser.find_element_by_id('id_list_table')
#                 rows = table.find_elements_by_tag_name('tr')
#                 self.assertIn(row_text,[row.text for row in rows])
#                 return
#             except (AssertionError, WebDriverException) as e:
#                 if time.time() - start_time > MAX_WAIT:
#                     raise e
#                 time.sleep(0.5)      

#     def test_can_add_players_and_retrieve_them_later(self):
#         # Foosball local admin opens the web app
#         self.browser.get(self.live_server_url)

#         # (S)he notices the name T.G.I.Foosball in the title and the first header
#         self.assertIn('T.G.I.Foosball', self.browser.title)
#         header_text = self.browser.find_element_by_tag_name('h1').text
#         self.assertIn('Tournament', header_text)

#         # The admin is invited to enter a new player
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         self.assertEqual(
#             inputbox.get_attribute('placeholder'),
#             "Enter a new player name"
#         )

#         # The admin types "John Doe" into a text box
#         inputbox.send_keys('John Doe')

#         # When the admin hits enter, the page updates, and now the page lists
#         # "1: John Doe" as a player in the list of players:
#         inputbox.send_keys(Keys.ENTER)
#         self.wait_for_row_in_list_table('1: John Doe')

#         # There is still a text box inviting the admin to add another player.
#         # The admin enters "Jenny Doe":
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         inputbox.send_keys('Jenny Doe')
#         inputbox.send_keys(Keys.ENTER)

#         # The page updates again, and now shows both players in the list:
#         self.wait_for_row_in_list_table('1: John Doe')
#         self.wait_for_row_in_list_table('2: Jenny Doe')

#     def test_multiple_tournaments_have_user_lists_at_different_urls(self):
#         # Thomas creates a new tournament
#         self.browser.get(self.live_server_url)
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         inputbox.send_keys("John Doe")
#         inputbox.send_keys(Keys.ENTER)
#         self.wait_for_row_in_list_table("1: John Doe")

#         # He notices that the tournament has a unique URL
#         thomas_tournament_url = self.browser.current_url
#         self.assertRegex(thomas_tournament_url, '/tournament/.+')

#         # Now, another admin, Ognjen, wants to create another tournament

#         ## We use a new browser session to make sure that no information
#         ## of Thomas is coming through from cookies, etc.
#         self.browser.quit()
#         self.browser = webdriver.Firefox()

#         # Ognjen visits the main page. There is no sign of Thomas' tournament
#         self.browser.get(self.live_server_url)
#         page_text = self.browser.find_element_by_tag_name('body').text
#         self.assertNotIn('John Doe', page_text)
#         self.assertNotIn('Jenny Doe', page_text)

#         # Ognjen creates a new tournament
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         inputbox.send_keys('Jenny Doe')
#         inputbox.send_keys(Keys.ENTER)
#         self.wait_for_row_in_list_table("1: Jenny Doe")

#         # Ognjen gets his own URL for the tournament
#         ognjen_tournament_url = self.browser.current_url
#         self.assertRegex(ognjen_tournament_url, "/tournament/.+")
#         self.assertNotEqual(thomas_tournament_url, ognjen_tournament_url)

#         # Again, there is no trace of Thomas' tournament
#         page_text = self.browser.find_element_by_tag_name('body').text
#         self.assertNotIn("John Doe", page_text)
#         self.assertIn("Jenny Doe", page_text)
