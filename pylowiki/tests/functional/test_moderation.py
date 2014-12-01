from pylowiki.tests import *

class TestModerationController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='moderation', action='index'))
        # Test response...
