import unittest
from zah.core.shortcuts import render
from bs4 import BeautifulSoup

class TestRouter(unittest.TestCase):
    def test_render(self):
        # Should return callable
        self.assertTrue(callable(render({}, 'base.htm')))
        # ...that callable should be view(**kwargs)
        self.assertEqual(render({}, 'base.htm').__name__, 'view')

    def test_render_output(self):
        # The output should be the HTML
        # file passed by the user
        output = render({}, 'base.htm')()
        self.assertTrue(isinstance(output, str))

    def test_variable_expansion(self):
        context = {
            'title': 'Sports',
        }
        # Passing context through render
        output = render({}, 'base.htm', context)
        # And, test passing context to view
        soup = BeautifulSoup(output(section_title='Tennis'), 'html.parser')
                
        self.assertEqual(soup.find('title').text, 'Sports')
        self.assertEqual(soup.find('h2', attrs={'class': 'section_title'}).text, 'Tennis')

if __name__ == "__main__":
    unittest.main()
