from fgx.tests import *

class TestAjaxAptController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_apt', action='index'))
        # Test response...
