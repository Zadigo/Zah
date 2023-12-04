import unittest
from unittest import TestCase

from werkzeug.wrappers.response import Response

from zah.urls.base import render_page


class TestUrls(TestCase):
    def test_can_render_template(self):
        view = render_page('index.html')
        response = view()
        print(view, response)
        self.assertIsInstance(response, Response)


if __name__ == '__main__':
    unittest.main()
