# -*- coding: utf-8 -*-
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller = 'home', action = 'index' ) # load the homepage.
    map.connect('/activate/*id', controller = 'activate', action = 'index') # Account Activation
    map.connect('/issue/{id}/background', controller = 'issue', action = 'background', id = '{id}')
    map.connect('/issue/readThis', controller = 'issue', action = 'readThis')
    map.connect('/issue/{id}/edit', controller = 'issue', action = 'edit', id = '{id}')
    map.connect('/issue/edit_handler', controller = 'issue', action = 'edit_handler')
    map.connect('/issue/edit_slideshow', controller = 'issue', action = 'edit_slideshow')
    map.connect('/issue/{id}', controller = 'issue', action = 'home', id = '{id}')
    map.connect('/issue/{id}/leaderboard', controller = 'issue', action = 'leaderboard', id = '{id}')
    map.connect('/issue/{id1}/news/{id2}', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/issue/{id1}/suggestion/{id2}/rate/{id3}', controller = 'suggestion', action = 'rate', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/issue/{id1}/suggestion/{id2}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    #map.connect('/issue/{id1}/news/{id2}', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id}', controller = 'home', action = 'mainPage', id = '{id}')
    #map.connect('/php/{id}', '/php/{id}')
    #map.connect('/commentModeration', controller = 'commentModeration', action = 'index')
    map.connect('/moderation', controller = 'moderation', action = 'index')
    map.connect('/moderation/handler/{id}', controller = 'moderation', action = 'handler', id = '{id}')
    map.connect('/moderation/{id1}/{id2}', controller = 'moderation', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addIssue', controller = 'addIssue', action = 'index')
    map.connect('/addSuggestion/{id}', controller = 'addSuggestion', action = 'handler', id = '{id}')
    map.connect('/rating', controller = 'rating', action = 'index')
    map.connect('/admin', controller = 'admin', action = 'index')
    map.connect('/corp/', controller = 'corp', action = 'index', id = 'None')
    map.connect('/corp/{id}', controller = 'corp', action = 'index', id = '{id}')
    map.connect('/suggestion/rate', controller = 'suggestion', action = 'rate')
    ################
    # Action Lists #
    ################
    
    map.connect('/edit', controller='actionlist', action='index', id='edit')    
    map.connect('/edit/', controller='actionlist', action='index', id='edit')
    
    map.connect('/revision', controller='actionlist', action='index', id='revision')    
    map.connect('/revision/', controller='actionlist', action='index', id='revision')  
    
    map.connect('/delete', controller='actionlist', action='index', id='delete')    
    map.connect('/delete/', controller='actionlist', action='index', id='delete')    

    map.connect('/restore', controller='actionlist', action='index', id='restore')    
    map.connect('/restore/', controller='actionlist', action='index', id='restore')
    
    map.connect('/sitemap', controller='actionlist', action='index', id='sitemap')
    map.connect('/issues', controller='actionlist', action='index', id='sitemapIssues')
    map.connect('/solutions', controller = 'actionlist', action = 'index', id = 'sitemapSolutions')

    map.connect('/account/edit', controller = 'account', action = 'edit')
    map.connect('/account/editSubmit', controller = 'account', action = 'editSubmit')
    #map.connect('/account/{id}', controller='account', action='user', id='{id}')
    map.connect('/account/{id}', controller = 'home', action = 'mainPage', id = '{id}')

    ################
    #  AreYouSure  #
    ################

    map.connect('/revert/*id', controller = 'AreYouSure', action = 'revert', id = '{id}' ) # revert AreYouSure route
    map.connect('/delete/*id', controller = 'AreYouSure', action = 'delete', id = '{id}' ) # delete AreYouSure route  
    map.connect('/restore/*id', controller = 'AreYouSure', action = 'restore', id = '{id}' ) # restore AreYouSure route  
    map.connect('/AreYouSure/handler/*id', controller = 'AreYouSure', action = 'handler' ) # revert handler
    
    ################
    # Application  #
    ################

    map.connect('/edit/handler/*id', controller = 'edit', action = 'handler' ) # edit handler
    map.connect('/edit/*id', controller='edit', action='edit') # edit route
  

    map.connect('/revision/number/{id}', controller='revision', action='number') # revision view number
    map.connect('/revision/*id', controller='revision', action='revisions') # all revisions for page

    map.connect('/create', controller='create', action='index') # create route
    map.connect('/create/assist/*id', controller='create', action='assist') # create route

    map.connect('/search', controller = 'search', action = 'index' ) # search root route
    map.connect('/search/handler', controller = 'search', action = 'handler' ) # search handler route

    map.connect('/contact', controller = 'contact', action = 'index' ) # contact route
    map.connect('/contact/handler', controller = 'contact', action = 'handler' ) # contact handler route

    map.connect('/comment/index/*id', controller='comment', action='index') # comment handler route
    map.connect('/comment/disable/{id}', controller='comment', action='disable') # set comment to disabled
    
    map.connect('/{controller}', controller='{controller}', action='index') # Maps url to controller index
    map.connect('/{controller}/{action}', controller='{controller}', action='{action}')
    map.connect('/{controller}/{action}/{id}')

    map.connect('/random', controller='wiki', action='random') # selects a random page

    map.connect('/wiki/handler/*id', controller='wiki', action='handler') # wiki handler route
    #map.connect('/wiki/*id', controller = 'wiki', action = 'index')
    #map.connect('/*id', controller='wiki', action='index') # view or wiki route

    return map
