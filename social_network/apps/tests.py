from django.test import TestCase
from django.shortcuts import reverse
import time 
# Create your tests here.
class AppsTest(TestCase):
    def test_init_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code , 200)

    def test_init_name(self):
        response = self.client.get(reverse("Home page"))
        self.assertEqual(response.status_code , 200)

    def test_time_load(self):
        start_load = time.time()
        response = self.client.get(reverse("Home page"))
        end_load = time.time()
        time_load = end_load - start_load
        self.assertLess(time_load , 1)