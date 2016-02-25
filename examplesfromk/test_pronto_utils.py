import unittest
import os
from pronto_utils import remove_file
from pronto_utils import download_if_needed
from pronto_utils import plot_daily_totals


class TestProntoUtils (unittest.TestCase):
    """
    Defines the unit test cases for pronto utils
    """

    def test_remove_unneeded(self):
        """
        Tests remove file function returns false when file doesn't exist
        """
        # This is obviously not a file, so let's make sure that it
        # returns that fact
        result = remove_file('notafile.nonext')
        self.assertFalse(result[0])

    def test_remove_needed(self):
        """
        Tests remove file function returns true when file does exist
        """
        # Let's make a file to try deleting, and make sure the function
        # does it
        os.system('touch a.py')
        result = remove_file('a.py')
        self.assertTrue(result[0])

    def test_download_needed(self):
        """
        Tests the download if needed function downloads new files
        """
        # Remove data works, so let's make sure test.zip isn't
        # around so we can download it for the test and verify that
        # it will download
        remove_file('test.zip')
        result = download_if_needed(
            'https://github.com/UWSEDS/Cogert/blob/master/analysis/test.zip',
            'test.zip')
        self.assertFalse(result[0])

    def test_download_unneeded(self):
        """
        Ensures download if needed function won't double download_if_needed
        """
        # We just downloaded the test.zip so let's make sure it doesn't
        # download again if it's queried
        result = download_if_needed(
            'https://github.com/UWSEDS/Cogert/blob/master/analysis/test.zip',
            'test.zip')
        self.assertTrue(result[0])

    def test_plot_daily_totals(self):
        try:
            plot_daily_totals()
        except:
            self.fail('plot_daily_totals raised an exception!')
if __name__ == '__main__':
    unittest.main()
