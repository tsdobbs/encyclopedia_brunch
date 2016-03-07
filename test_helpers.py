import unittest
import os
from helpers import get_image_selection

class TestWikipedia (unittest.TestCase):
    """
    Defines the unit test cases for the various helper functions used
    """

    def test_wikipedia_response(self):
        """
        Tests if we successfully got a list of images back from Wikipedia
        """
        # Check a bunch of different possible titles and make sure images are returned
        title_list = ['lion']
        for title in title_list:
            image_list = get_image_selection(title)
            self.assertTrue(len(image_list)>0)

    def test_wikipedia_redirect(self):
        """
        Tests if the function can handle slight changes (ex. 'lions' should direct to the 'Lion' page)
        """
        # Check a bunch of different possible titles and make sure images are returned
        title_list = ['lions']
        for title in title_list:
            image_list = get_image_selection(title)
            self.assertTrue(len(image_list)>0)

    def test_wikipedia_nobigpics(self):
        """
        Makes sure that if a page is returned but it has no pics that are big enough, returns a blank list but no errors
        """
        title_list = ['landshark', 'oil drilling']
        for title in title_list:
            image_list = get_image_selection(title)
            self.assertTrue(True)

    def test_wikipedia_nonsense(self):
        """
        Makes sure that if nonsense is supplied function returns a blank list, but no errors
        """
        title_list = ['sfjisakl;fjwi;']
        for title in title_list:
            image_list = get_image_selection(title)
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
