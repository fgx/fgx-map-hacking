from fgx.tests import *

class TestWwwController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='www', action='index'))
        # Test response...
