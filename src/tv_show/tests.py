from django.test import TestCase

# Create your tests here.

class HomePageVisitorTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/tv-show/')
        
        self.assertTemplateUsed(response,'tv-show/home.html')