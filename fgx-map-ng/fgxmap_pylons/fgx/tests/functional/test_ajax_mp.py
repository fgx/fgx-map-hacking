from fgx.tests import *

class TestAjaxMpController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_mp', action='index'))
        # Test response...
