import unittest
from datetime import datetime
from tornado_analysis.tornado_class import tornado_class

class TestTornadoClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up method to initiate the tornado class with a dataset before tests are run. """
        cls.tornado = tornado_class('data/tornado_data.csv')

    def test_clean_data(self):
        """ Test if the data cleaning method works correctly. """
        #check if the clean_data method formatted the datetime correctly
        date_format = "%Y-%m-%d %H:%M:%S"
        self.assertTrue(isinstance(datetime.strptime(str(self.tornado.df['datetime'].iloc[0]), date_format), datetime))

    def test_date_filter(self):
        """ Test the date filtering functionality. """
        filtered_data = self.tornado.date_filter('2020-01-01', '2020-12-31')
        #check the filtered data is not empty
        self.assertTrue(not filtered_data.empty)

    def test_worst_tornadoes(self):
        """ Test finding the worst tornadoes. """
        worst_data = self.tornado.worst_tornadoes('2020-01-01', '2020-12-31')
        #returns data and potentially check the maximum Fujita scale found
        self.assertTrue(not worst_data.empty)
        self.assertEqual(worst_data['fujita_scale'].max(), worst_data['fujita_scale'].iloc[0])

    def test_multiple_grid_count(self):
        """ Test counting tornadoes moving through multiple grids. """
        count = self.tornado.multiple_grid_count('2020-01-01', '2020-12-31')
        #check if the count is a non-negative integer
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_grid_severity_probability(self):
        """ Test the grid severity probability calculation. """
        probability = self.tornado.grid_severity_probability(101, 2, '2020-01-01', '2020-12-31')
        #check if probability is a float and correctly calculated
        self.assertIsInstance(probability, float)
        self.assertGreaterEqual(probability, 0)

if __name__ == '__main__':
    unittest.main()
