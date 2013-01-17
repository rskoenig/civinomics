from pylowiki.tests import *

class TestIdeaController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='idea', action='index'))
        # Test response...
