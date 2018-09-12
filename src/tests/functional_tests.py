from selenium import webdriver
import unittest

class SmokeTest(unittest.TestCase):

    def setUp(self):
        self.browser_Firefox = webdriver.Firefox()
        self.browser_Chrome = webdriver.Chrome()
    
    def test_webpage_opens_in_Firefox(self):
        # Alice has heard about a new cool website about TV shows.
        # Alice tries to open the homepage of TV-Aficio in Firefox.
        self.browser_Firefox.get('http://localhost:8000')

        # Alice sees that the webpage opens by noticing 'TV-Aficio' in the page title.
        self.assertIn('TV-Aficio', self.browser_Firefox.title)

    def test_webpage_opens_in_Chrome(self):
        # Alice has heard about a new cool website about TV shows.
        # Alice tries to open the homepage of TV-Aficio in Chrome.
        self.browser_Chrome.get('http://localhost:8000')

        # Alice sees that the webpage opens by noticing 'TV-Aficio' in the page title.
        self.assertIn('TV-Aficio', self.browser_Chrome.title)

    def tearDown(self):
        self.browser_Firefox.quit()
        self.browser_Chrome.quit()

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice has heard about a new cool website about TV shows.
        # Alice opens the homepage of TV-Aficio.
        self.browser.get('http://localhost:8000')

        # Alice notices 'TV-Aficio' in the page title and in the header
        self.assertIn('TV-Aficio', self.browser.title)
        self.fail('Finish the test')

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(verbosity=2)
