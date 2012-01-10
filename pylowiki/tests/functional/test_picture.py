from pylowiki.tests import *

class TestPictureController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='picture', action='index'))
        # Test response...
