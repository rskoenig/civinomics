from pylowiki.tests import *

class TestSlideshowController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='slideshow', action='index'))
        # Test response...
