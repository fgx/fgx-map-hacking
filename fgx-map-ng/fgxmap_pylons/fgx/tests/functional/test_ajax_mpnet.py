from fgx.tests import *

class TestAjaxMpnetController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_mpnet', action='index'))
        # Test response...
