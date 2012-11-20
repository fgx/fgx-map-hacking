from fgx.tests import *

class TestAjaxUsersController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ajax_users', action='index'))
        # Test response...
