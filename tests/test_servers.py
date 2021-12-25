import unittest

from zah.core.servers import BaseServer


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = BaseServer()
        
        
if __name__ == '__main__':
    unittest.main()
