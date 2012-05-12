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
    map.connect('/issue/{id}/edit_handler', controller = 'issue', action = 'edit_handler', id = '{id}')
    map.connect('/issue/{id}/editSlideshow', controller = 'issue', action = 'editSlideshow', id = '{id}')
    map.connect('/issue/{id}', controller = 'issue', action = 'home', id = '{id}')
    map.connect('/issue/{id}/leaderboard', controller = 'leaderboard', action = 'index', id = '{id}')
    map.connect('/issue/{id}/discussion', controller = 'discussion', action = 'index', id = '{id}')
    map.connect('/issue/{id1}/news/{id2}', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/issue/{id1}/suggestion/{id2}/rate/{id3}', controller = 'suggestion', action = 'rate', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/comment/{id}', controller = 'comment', action = 'index', id = '{id}')
    map.connect('/moderation', controller = 'moderation', action = 'index')
    map.connect('/moderation/handler/{id}', controller = 'moderation', action = 'handler', id = '{id}')
    map.connect('/moderation/{id1}/{id2}', controller = 'moderation', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addWorkshop', controller = 'workshop', action = 'addWorkshop')
    map.connect('/rating', controller = 'rating', action = 'index')
    map.connect('/admin', controller = 'admin', action = 'index')
    map.connect('/corp/', controller = 'corp', action = 'index', id = 'None')
    map.connect('/corp/{id}', controller = 'corp', action = 'index', id = '{id}')
    map.connect('/suggestion/rate', controller = 'suggestion', action = 'rate')

    map.connect('/slideshow/edit', controller = 'slideshow', action = 'edit')
    
    map.connect('/ipadListener/sendSurveyData', controller = 'ipadListener', action = 'sendSurveyData')
    map.connect('/ipadListener/sendSurveyData/', controller = 'ipadListener', action = 'sendSurveyData')

    # Workshop home page
    map.connect('/workshops/{id1}/{id2}', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')

    # Workshop follow/unfollow
    map.connect('/workshop/{id1}/{id2}/follow', controller = 'workshop', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/follow/', controller = 'workshop', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/unfollow', controller = 'workshop', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/unfollow/', controller = 'workshop', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    
    
    # Add image(s) to workshop slideshow
    map.connect('/workshop/{id1}/{id2}/addImages', controller = 'slideshow', action = 'addImageDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/addImages/', controller = 'slideshow', action = 'addImageDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addImages', controller = 'slideshow', action = 'addImageDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addImages/', controller = 'slideshow', action = 'addImageDisplay', id1 = '{id1}', id2 = '{id2}')
    
    # Handler for adding images
    map.connect('/workshop/{id1}/{id2}/addImages/handler', controller = 'slideshow', action = 'addImageHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/addImages/handler', controller = 'slideshow', action = 'addImageHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addImages/handler', controller = 'slideshow', action = 'addImageHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addImages/handler/', controller = 'slideshow', action = 'addImageHandler', id1 = '{id1}', id2 = '{id2}')
    
    # Edit slideshow
    map.connect('/workshop/{id1}/{id2}/editSlideshow', controller = 'slideshow', action = 'editSlideshowDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/editSlideshow/', controller = 'slideshow', action = 'editSlideshowDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editSlideshow', controller = 'slideshow', action = 'editSlideshowDisplay', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editSlideshow/', controller = 'slideshow', action = 'editSlideshowDisplay', id1 = '{id1}', id2 = '{id2}')
    
    # Workshop background page
    map.connect('/workshop/{id1}/{id2}/background', controller = 'workshop', action = 'background', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/background/', controller = 'workshop', action = 'background', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/background', controller = 'workshop', action = 'background', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/background/', controller = 'workshop', action = 'background', id1 = '{id1}', id2 = '{id2}')

    # Workshop settings
    map.connect('/workshop/{id1}/{id2}/editSettings', controller = 'workshop', action = 'editSettings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/editSettings/', controller = 'workshop', action = 'editSettings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editSettings', controller = 'workshop', action = 'editSettings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editSettings/', controller = 'workshop', action = 'editSettings', id1 = '{id1}', id2 = '{id2}')

    # Workshop feedback
    map.connect('/workshop/{id1}/{id2}/feedback', controller = 'workshop', action = 'feedback', id1 = '{id1}', id2 = '{id2}')

    # Workshop settings submit handler
    map.connect('/workshop/{id1}/{id2}/editWorkshopHandler', controller = 'workshop', action = 'editWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/editWorkshopHandler/', controller = 'workshop', action = 'editWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editWorkshopHandler', controller = 'workshop', action = 'editWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/editWorkshopHandler/', controller = 'workshop', action = 'editWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    
    # Workshop admin
    map.connect('/workshop/{id1}/{id2}/admin', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/admin/', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')

    # Workshop admin submit handler
    map.connect('/workshop/{id1}/{id2}/adminWorkshopHandler', controller = 'workshop', action = 'adminWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/adminWorkshopHandler/', controller = 'workshop', action = 'adminWorkshopHandler', id1 = '{id1}', id2 = '{id2}')

    # Workshop feedback
    map.connect('/workshop/{id1}/{id2}/feedback', controller = 'workshop', action = 'feedback', id1 = '{id1}', id2 = '{id2}')

    # System Administration
    map.connect('/systemAdmin', controller = 'systemAdmin', action = 'index')
    map.connect('/systemAdmin/', controller = 'systemAdmin', action = 'index')

    # System admin submit handler
    map.connect('/systemAdmin/handler', controller = 'systemAdmin', action = 'handler')
    map.connect('/systemAdmin/handler/', controller = 'systemAdmin', action = 'handler')



    # Resources
    map.connect('/resource/handler/{id1}/{id2}', controller = 'news', action = 'handler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/resource/handler/{id1}/{id2}/', controller = 'news', action = 'handler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/resource/{id3}/{id4}', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/resource/{id3}/{id4}/', controller = 'news', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    # Resource flagging
    map.connect('/flagResource/{id1}', controller = 'news', action = 'flagResource', id1 = '{id1}')

    # Resource modding
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modResource', controller = 'news', action = 'modResource', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modResource/', controller = 'news', action = 'modResource', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    
    
    # Suggestions
    map.connect('/addSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'addSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'addSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/suggestion/{id3}/{id4}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/suggestion/{id3}/{id4}/', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')

    # Suggestion flagging
    map.connect('/flagSuggestion/{id1}', controller = 'suggestion', action = 'flagSuggestion', id1 = '{id1}')

    # Suggestion modding
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modSuggestion', controller = 'suggestion', action = 'modSuggestion', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modSuggestion/', controller = 'suggestion', action = 'modSuggestion', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    
    # User profile
    map.connect('/profile/{id1}/{id2}', controller = 'account', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/', controller = 'account', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}')
    
    # User profile follow/unfollow
    map.connect('/profile/{id1}/{id2}/follow', controller = 'account', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/follow/', controller = 'account', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/unfollow', controller = 'account', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/unfollow/', controller = 'account', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    
    # User profile enable/disable
    map.connect('/profile/{id1}/{id2}/enable', controller = 'account', action = 'enableHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/enable/', controller = 'account', action = 'enableHandler', id1 = '{id1}', id2 = '{id2}')

    # User accessLevel
    map.connect('/profile/{id1}/{id2}/privs', controller = 'account', action = 'privsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/privs/', controller = 'account', action = 'privsHandler', id1 = '{id1}', id2 = '{id2}')

    # Comments
    map.connect('/addComment', controller = 'comment', action = 'addComment')
    map.connect('/addComment/', controller = 'comment', action = 'addComment')
    
    # Comment flagging
    map.connect('/flagComment/{id1}', controller = 'comment', action = 'flagComment', id1 = '{id1}')

    # Comment modding
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modComment/{id5}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'suggestion')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modComment/{id5}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'suggestion')

    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modComment/{id5}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'resource')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modComment/{id5}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'resource')

    map.connect('/workshop/{id1}/{id2}/background/modComment/{id3}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = 'background', id4 = 'background', id5 = '{id3}', id6 = 'background')
    map.connect('/workshop/{id1}/{id2}/background/modComment/{id3}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = 'background', id4 = 'background', id5 = '{id3}', id6 = 'background')


    map.connect('/workshop/{id1}/{id2}/feedback/modComment/{id3}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = 'feedback', id4 = 'feedback', id5 = '{id3}', id6 = 'feedback')
    map.connect('/workshop/{id1}/{id2}/feedback/modComment/{id3}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = 'feedback', id4 = 'feedback', id5 = '{id3}', id6 = 'feedback')

    # Ratings
    map.connect('/rateSuggestion/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateSuggestion', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/rateFacilitation/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateFacilitation', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')

    map.connect('/geo/postal/{id1}/{id2}', controller = 'geo', action = 'showPostalInfo', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/city/{id1}/{id2}/{id3}', controller = 'geo', action = 'showCityInfo', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/geo/county/{id1}/{id2}/{id3}', controller = 'geo', action = 'showCountyInfo', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/geo/state/{id1}/{id2}', controller = 'geo', action = 'showStateInfo', id1 = '{id1}', id2 = '{id2}')

    # Temporary
    map.connect('/workshops/{id1}/{id2}/discussion', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    
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
    map.connect('/workshops', controller='actionlist', action='index', id='sitemapIssues')
    map.connect('/searchWorkshops/{id1}/{id2}', controller='actionlist', action='searchWorkshops', id='searchWorkshops', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchWorkshops/{id1}/{id2}/', controller='actionlist', action='searchWorkshops', id='searchWorkshops', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchUsers/{id1}/{id2}', controller='actionlist', action='searchUsers', id='searchUsers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchUsers/{id1}/{id2}/', controller='actionlist', action='searchUsers', id='searchUsers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchTags/{id1}', controller='actionlist', action='searchTags', id='searchTags', id1 = '{id1}')
    map.connect('/searchTags/{id1}/', controller='actionlist', action='searchTags', id='searchTags', id1 = '{id1}')
    map.connect('/searchName/', controller='actionlist', action='searchName', id='searchName')
    map.connect('/searchName', controller='actionlist', action='searchName', id='searchName')

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
    map.connect('/{controller}/', controller = '{controller}', action = 'index')
    map.connect('/{controller}/{action}', controller='{controller}', action='{action}')
    map.connect('/{controller}/{action}/', controller='{controller}', action='{action}')
    map.connect('/{controller}/{action}/{id}')

    map.connect('/random', controller='wiki', action='random') # selects a random page

    #map.connect('/wiki/handler/*id', controller='wiki', action='handler') # wiki handler route
    map.connect('/wiki/handler/{id1}/{id2}', controller = 'wiki', action = 'handler', id1 = '{id1}', id2 = '{id2}')
    #map.connect('/wiki/*id', controller = 'wiki', action = 'index')
    #map.connect('/*id', controller='wiki', action='index') # view or wiki route

    return map
