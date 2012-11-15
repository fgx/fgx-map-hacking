from fgx.tests import *

class TestAjaxNavController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_nav', action='index'))
        # Test response...
