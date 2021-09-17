from django.test import TestCase,Client

# Create your tests here.
class formTest(TestCase):
    def test_form(self):
        client = Client()
        response = client.post('/', {'date_from':'2021-09-07','date_to':'2021-09-16'}) #test form creation response
        self.assertEqual(response.status_code, 200)
