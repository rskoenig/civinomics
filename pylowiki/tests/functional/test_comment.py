from pylowiki.tests import *

class TestCommentController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='comment', action='index'))
        # Test response...
