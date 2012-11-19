from pylowiki.tests import *

class TestActivateController(TestController):

    def test_activation_works(self):
        # make user
        # visit this page with email and hash
        # confirm user is not activated, and becomes activated
        # assert this: '%s, you are now registered!  Please login below.' % email

    def test_activation_wrong_hash(self):
    	# make user
        # visit this page with email and wrong hash
        # assert Incorrect activation string

    def test_second_activation_fails(self):
    	# make user, visit this page with email and hash
    	# confirm success message '%s, you are now registered!  Please login below.' % email
    	# now, visit this page again with the email and hash and assert:
    	# '%s is already marked as active!' % email

    def test_wrong_email(self):
        # make user then provide slightly wrong email name
        # assert we see this 'Specified user not found!'
        