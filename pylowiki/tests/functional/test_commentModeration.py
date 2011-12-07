from pylowiki.tests import *

class TestCommentmoderationController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='commentModeration', action='index'))
        # Test response...
