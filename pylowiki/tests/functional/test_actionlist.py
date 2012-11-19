# -*- coding: utf-8 -*-
from pylowiki.tests import *

class TestActionlistController(TestController):

	# what is this function about?
    def __before__(self):
        if c.conf['public.sitemap'] != "true": 
            h.check_if_login_required()

    # 
    def test_index( self, id ): # id is the action
        """Create a list of pages with the given action/option """
        """Valid actions: edit, revision, delete, restore, sitemap """
        # c.action = id
        # if id == 'sitemapIssues' expect list_workshops.bootstrap to render
        # otherwise
        #   sitemap == lib/db/ -> get_all_pages()
        #	'surveys': == lib/db/ -> getActiveSurveys()
        #	restore == lib/db/ -> get_all_pages(1)
        # AND if 'user' in session:
        #	if not c.authuser:
        #        session.delete()
        #        return redirect('/')
        #
        # otherwise If the user is in session, list the surveys
        # return render('/derived/list_surveys.bootstrap')

    def test_help( self ):

        # return render('/derived/help.bootstrap')

    def test_searchWorkshops( self, id1, id2  ):
        # confirm render('/derived/list_workshops.bootstrap')

    def test_searchName( self, id1, id2 ):
        # if searchType workshops make workshop and confirm name in render('/derived/list_workshops.bootstrap')
        # else: render('/derived/list_users.bootstrap')

    def test_searchGeoUsers( self, id1 ):
        # make user and confirm result in render('/derived/list_users.bootstrap')

    def test_searchGeoWorkshops( self ):
        # make workshop, test scope searches in render('/derived/list_workshops.bootstrap')
        # if no match return redirect('/')

    def test_searchTags( self, id1 ):
        # create workshop with tag, search for found tag workshop in render('/derived/list_workshops.bootstrap')

    def searchUsers( self, id1, id2  ):
        # create user, search for user and see if result in render('/derived/list_users.bootstrap')

