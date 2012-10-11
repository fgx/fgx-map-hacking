from fgxmap.tests import *

class TestAppinfoController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='appinfo', action='index'))
        # Test response...
