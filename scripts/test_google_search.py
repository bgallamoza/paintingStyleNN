'''
@File   :   test_google_search.py
@Author :   Brennan Gallamoza
@Desc   :   Unit tests for testing the google_search.py module
'''

import unittest
from google_search import *

class Test_GoogleSearch(unittest.TestCase):

    def test_generate_urls(self):
        search_params = {"q":"dog","tbm":"isch"}
        err_msg = "ERROR: Wrong URL"
        url = generate_url(search_params)
        self.assertEqual(url, "https://www.google.com/search?q=dog&tbm=isch", err_msg)

    # Tests if method correctly gets the first url for a "dog" search
    def test_get_image_urls_1(self):
        PATH = ".\\scripts\\drivers\\chromedriver.exe"
        wd = webdriver.Chrome(PATH)
        search_params = {"q":"dog","tbm":"isch"}
        delay = 1
        max_images = 1
        err_msg_1 = "ERROR: Incorrect url_list size"
        err_msg_2 = "ERROR: Incorrect URLS"
        correct_list = [
            'https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e'
        ]

        url_list = get_image_urls(wd, delay, max_images, search_params)
        print(url_list)

        self.assertEqual(1, len(url_list), err_msg_1)
        self.assertEqual(url_list, correct_list, err_msg_2)

        wd.quit()

    # Tests if method correctly gets the multiple urls for a "dog" search
    def test_get_image_urls_2(self):
        PATH = ".\\scripts\\drivers\\chromedriver.exe"
        wd = webdriver.Chrome(PATH)
        search_params = {"q":"dog","tbm":"isch"}
        delay = 1
        max_images = 3
        err_msg_1 = "ERROR: Incorrect url_list size"
        err_msg_2 = "ERROR: Incorrect URLS"
        correct_list = [
            'https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e',
            'https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/02/322868_1100-800x825.jpg',
            'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=1200:*'
        ]

        url_list = get_image_urls(wd, delay, max_images, search_params)
        print(url_list)

        self.assertEqual(3, len(url_list), err_msg_1)
        self.assertEqual(url_list, correct_list, err_msg_2)

        wd.quit()

    def test_url_to_img(self):
        url = 'https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e'
        img_1 = url_to_img(url)
        img_1.show()

    def img_to_array(self):
        url = 'https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=67773a9d419786091c958b2ad08eae5e'
        arr = img_to_array(url_to_img(url))
        self.assertEqual(arr.shape, (1200, 1200, 3))

if __name__ == '__main__':
    unittest.main()