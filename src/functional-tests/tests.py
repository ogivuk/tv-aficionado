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
        self.browser.get(self.live_server_url+'/tv-show/')
        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('TV Aficionado',self.browser.title)
        self.assertIn('TV Shows', header_text)

# class AddNewTVShowTest(LiveServerTestCase):

#     def setUp(self):
#         self.browser_firefox = webdriver.Firefox()
#         self.browser_chrome = webdriver.Chrome()

#     def tearDown(self):
#         self.browser_firefox.quit()
#         self.browser_chrome.quit()

#     def can_add_tvshow_and_retrieve_it_later(self):
#         # User opens the default page


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
