from fgx.tests import *

class TestAjaxDbController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_db', action='index'))
        # Test response...
