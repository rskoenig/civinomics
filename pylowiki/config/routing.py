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

    ########################################################################################################
    # 
    # Administrative routes
    # 
    ########################################################################################################
    
    # System Administration
    map.connect('/systemAdmin', controller = 'systemAdmin', action = 'index')
    map.connect('/systemAdmin/', controller = 'systemAdmin', action = 'index')

    # System admin submit handler
    map.connect('/systemAdmin/handler', controller = 'systemAdmin', action = 'handler')
    map.connect('/systemAdmin/handler/', controller = 'systemAdmin', action = 'handler')
    
    ########################################################################################################
    # 
    # Corporate routes
    # 
    ########################################################################################################
    map.connect('/corp/', controller = 'corp', action = 'index', id = 'None')
    map.connect('/corp/{id}', controller = 'corp', action = 'index', id = '{id}')

    ########################################################################################################
    # 
    # Platform-specific routes
    # 
    ########################################################################################################

    
    map.connect('/comment/{id}', controller = 'comment', action = 'index', id = '{id}')
    map.connect('/moderation', controller = 'moderation', action = 'index')
    map.connect('/moderation/handler/{id}', controller = 'moderation', action = 'handler', id = '{id}')
    map.connect('/moderation/{id1}/{id2}', controller = 'moderation', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addWorkshop', controller = 'workshop', action = 'addWorkshop')
    map.connect('/rating', controller = 'rating', action = 'index')
    map.connect('/admin', controller = 'admin', action = 'index')
    map.connect('/suggestion/rate', controller = 'suggestion', action = 'rate')

    map.connect('/slideshow/edit', controller = 'slideshow', action = 'edit')
    
    map.connect('/ipadListener/sendSurveyData', controller = 'ipadListener', action = 'sendSurveyData')
    map.connect('/ipadListener/sendSurveyData/', controller = 'ipadListener', action = 'sendSurveyData')

    # Workshop home page
    map.connect('/workshops/{id1}/{id2}', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/', controller = 'workshop', action = 'display', id1 = '{id1}', id2 = '{id2}')
    # suggestions
    map.connect('/workshop/{id1}/{id2}/suggestions', controller = 'workshop', action = 'displayAllSuggestions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/suggestions/', controller = 'workshop', action = 'displayAllSuggestions', id1 = '{id1}', id2 = '{id2}')
    # resources
    map.connect('/workshop/{id1}/{id2}/resources', controller = 'workshop', action = 'displayAllResources', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/resources/', controller = 'workshop', action = 'displayAllResources', id1 = '{id1}', id2 = '{id2}')

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

    # Workshop leaderboard page
    map.connect('/workshop/{id1}/{id2}/leaderboard', controller = 'leaderboard', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/leaderboard/', controller = 'leaderboard', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard', controller = 'leaderboard', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard/', controller = 'leaderboard', action = 'index', id1 = '{id1}', id2 = '{id2}')
    # Workshop leaderboard explanation page
    map.connect('/workshop/{id1}/{id2}/leaderboard_explanation/', controller = 'leaderboard', action = 'explain', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/leaderboard_explanation', controller = 'leaderboard', action = 'explain', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_explanation/', controller = 'leaderboard', action = 'explain', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_explanation', controller = 'leaderboard', action = 'explain', id1 = '{id1}', id2 = '{id2}')
    # Workshop leaderboard followed Persons page
    map.connect('/workshop/{id1}/{id2}/leaderboard_followedPersons', controller = 'leaderboard', action = 'followedPersons', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/leaderboard_followedPersons/', controller = 'leaderboard', action = 'followedPersons', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_followedPersons/', controller = 'leaderboard', action = 'followedPersons', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_followedPersons', controller = 'leaderboard', action = 'followedPersons', id1 = '{id1}', id2 = '{id2}')
    # Workshop leaderboard followed Persons page
    map.connect('/workshop/{id1}/{id2}/leaderboard_UserRanks', controller = 'leaderboard', action = 'UserRankings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/leaderboard_UserRanks/', controller = 'leaderboard', action = 'UserRankings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_UserRanks/', controller = 'leaderboard', action = 'UserRankings', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/leaderboard_UserRanks', controller = 'leaderboard', action = 'UserRankings', id1 = '{id1}', id2 = '{id2}')

    # Workshop discussion listing page
    map.connect('/workshop/{id1}/{id2}/discussion', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/discussion/', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/discussion', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/discussion/', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    # Add discussion topic for Workshop
    map.connect('/workshop/{id1}/{id2}/addDiscussion', controller = 'discussion', action = 'addDiscussion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/addDiscussion/', controller = 'discussion', action = 'addDiscussion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addDiscussion', controller = 'discussion', action = 'addDiscussion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshops/{id1}/{id2}/addDiscussion/', controller = 'discussion', action = 'addDiscussion', id1 = '{id1}', id2 = '{id2}')
    # New discussion
    map.connect('/newDiscussion/{id1}/{id2}', controller = 'discussion', action = 'newDiscussionHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newDiscussion/{id1}/{id2}/', controller = 'discussion', action = 'newDiscussionHandler', id1 = '{id1}', id2 = '{id2}')
    # Edit discussion Handler
    map.connect('/editDiscussionHandler/{id1}/{id2}', controller = 'discussion', action = 'editDiscussionHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editDiscussionHandler/{id1}/{id2}/', controller = 'discussion', action = 'editDiscussionHandler', id1 = '{id1}', id2 = '{id2}')
    # Admin discussion Handler
    map.connect('/adminDiscussionHandler/', controller = 'discussion', action = 'adminDiscussionHandler', id1 = '{id1}', id2 = '{id2}')    
    map.connect('/adminDiscussionHandler', controller = 'discussion', action = 'adminDiscussionHandler', id1 = '{id1}', id2 = '{id2}')    
    # flag discussion
    map.connect('/flagDiscussion/{id1}/{id2}', controller = 'discussion', action = 'flagDiscussion', id1 = '{id1}', id2 = '{id2}')
    # clear discussion flags 
    map.connect('/clearDiscussionFlagsHandler/{id1}/{id2}', controller = 'discussion', action = 'clearDiscussionFlagsHandler', id1 = '{id1}', id2 = '{id2}')

    
    # Workshop Discussion Admin/Edit:
    map.connect('/editDiscussion/{id1}/{id2}', controller = 'discussion', action = 'editDiscussion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editDiscussion/{id1}/{id2}/', controller = 'discussion', action = 'editDiscussion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/adminDiscussion/{id1}/{id2}', controller = 'discussion', action = 'adminDiscussion', id1 = '{id1}', id2 = '{id2}')    
    map.connect('/adminDiscussion/{id1}/{id2}/', controller = 'discussion', action = 'adminDiscussion', id1 = '{id1}', id2 = '{id2}')    

    # Workshop individual discussion page
    map.connect('/workshop/{id1}/{id2}/discussion/{id3}/{id4}', controller = 'discussion', action = 'topic', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/discussion/{id3}/{id4}/', controller = 'discussion', action = 'topic', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/discussion/{id3}/{id4}', controller = 'discussion', action = 'topic', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/discussion/{id3}/{id4}/', controller = 'discussion', action = 'topic', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')


    # Workshop configuration
    map.connect('/workshop/{id1}/{id2}/configure', controller = 'workshop', action = 'configure', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configure/', controller = 'workshop', action = 'configure', id1 = '{id1}', id2 = '{id2}')

    # Workshop configuration submit handler
    map.connect('/workshop/{id1}/{id2}/configureWorkshopHandler', controller = 'workshop', action = 'configureWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureWorkshopHandler/', controller = 'workshop', action = 'configureWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureBasicWorkshopHandler', controller = 'workshop', action = 'configureBasicWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureBasicWorkshopHandler/', controller = 'workshop', action = 'configureBasicWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureSingleWorkshopHandler', controller = 'workshop', action = 'configureSingleWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureSingleWorkshopHandler/', controller = 'workshop', action = 'configureSingleWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureMultipleWorkshopHandler', controller = 'workshop', action = 'configureMultipleWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureMultipleWorkshopHandler/', controller = 'workshop', action = 'configureMultipleWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureStartWorkshopHandler', controller = 'workshop', action = 'configureStartWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/configureStartWorkshopHandler/', controller = 'workshop', action = 'configureStartWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    
    # Workshop feedback
    map.connect('/workshop/{id1}/{id2}/feedback', controller = 'workshop', action = 'feedback', id1 = '{id1}', id2 = '{id2}')

    # Workshop admin
    map.connect('/workshop/{id1}/{id2}/admin', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/admin/', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/administrate', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/administrate/', controller = 'workshop', action = 'admin', id1 = '{id1}', id2 = '{id2}')

    # Workshop admin submit handler
    map.connect('/workshop/{id1}/{id2}/adminWorkshopHandler', controller = 'workshop', action = 'adminWorkshopHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/adminWorkshopHandler/', controller = 'workshop', action = 'adminWorkshopHandler', id1 = '{id1}', id2 = '{id2}')

    # Resources
    map.connect('/addResource/{id1}/{id2}', controller = 'resource', action = 'addResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addResource/{id1}/{id2}/', controller = 'resource', action = 'addResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newResource/{id1}/{id2}', controller = 'resource', action = 'newResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newResource/{id1}/{id2}/', controller = 'resource', action = 'newResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newSResource/{id1}/{id2}', controller = 'resource', action = 'newSResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newSResource/{id1}/{id2}/', controller = 'resource', action = 'newSResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editResource/{id1}/{id2}', controller = 'resource', action = 'editResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editResource/{id1}/{id2}/', controller = 'resource', action = 'editResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/saveResource/{id1}/{id2}', controller = 'resource', action = 'saveResource', id1 = '{id1}', id2 = '{id2}')
    map.connect('/saveResource/{id1}/{id2}/', controller = 'resource', action = 'saveResource', id1 = '{id1}', id2 = '{id2}')

    map.connect('/resource/handler/{id1}/{id2}', controller = 'resource', action = 'handler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/resource/handler/{id1}/{id2}/', controller = 'resource', action = 'handler', id1 = '{id1}', id2 = '{id2}')

    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}', controller = 'resource', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/', controller = 'resource', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/resource/{id3}/{id4}', controller = 'resource', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/resource/{id3}/{id4}/', controller = 'resource', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/inactiveResources', controller = 'workshop', action = 'inactiveResources', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/inactiveResources/', controller = 'workshop', action = 'inactiveResources', id1 = '{id1}', id2 = '{id2}')

    # Resource flagging
    map.connect('/flagResource/{id1}/{id2}', controller = 'resource', action = 'flagResource', id1 = '{id1}', id2 = '{id2}')

    # Resource modding
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modResource', controller = 'resource', action = 'modResource', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modResource/', controller = 'resource', action = 'modResource', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/clearResourceFlagsHandler/{id1}/{id2}', controller = 'resource', action = 'clearResourceFlagsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/clearResourceFlagsHandler/{id1}/{id2}/', controller = 'resource', action = 'clearResourceFlagsHandler', id1 = '{id1}', id2 = '{id2}')
    
    map.connect('/modResourceHandler', controller = 'resource', action = 'modResourceHandler')
    map.connect('/modResourceHandler/', controller = 'resource', action = 'modResourceHandler')
    map.connect('/noteResourceHandler', controller = 'resource', action = 'noteResourceHandler')
    map.connect('/noteResourceHandler/', controller = 'resource', action = 'noteResourceHandler')
    
    # Suggestions
    map.connect('/addSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'addSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/addSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'addSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'newSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'newSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'editSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'editSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/saveSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'saveSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/saveSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'saveSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/suggestion/{id3}/{id4}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshops/{id1}/{id2}/suggestion/{id3}/{id4}/', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/workshop/{id1}/{id2}/inactiveSuggestions', controller = 'workshop', action = 'inactiveSuggestions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/inactiveSuggestions/', controller = 'workshop', action = 'inactiveSuggestions', id1 = '{id1}', id2 = '{id2}')

    # Suggestion flagging
    map.connect('/flagSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'flagSuggestion', id1 = '{id1}', id2 = '{id2}')

    # Suggestion modding
    map.connect('/modSuggestion/{id1}/{id2}', controller = 'suggestion', action = 'modSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/modSuggestion/{id1}/{id2}/', controller = 'suggestion', action = 'modSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/clearSuggestionFlagsHandler/{id1}/{id2}', controller = 'suggestion', action = 'clearSuggestionFlagsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/clearSuggestionFlagsHandler/{id1}/{id2}/', controller = 'suggestion', action = 'clearSuggestionFlagsHandler', id1 = '{id1}', id2 = '{id2}')
    
    map.connect('/modSuggestionHandler', controller = 'suggestion', action = 'modSuggestionHandler')
    map.connect('/modSuggestionHandler/', controller = 'suggestion', action = 'modSuggestionHandler')
    map.connect('/adoptSuggestionHandler', controller = 'suggestion', action = 'adoptSuggestionHandler')
    map.connect('/adoptSuggestionHandler/', controller = 'suggestion', action = 'adoptSuggestionHandler')
    map.connect('/noteSuggestionHandler', controller = 'suggestion', action = 'noteSuggestionHandler')
    map.connect('/noteSuggestionHandler/', controller = 'suggestion', action = 'noteSuggestionHandler')

    # Cofacilitation invitation and response
    map.connect('/profile/{id1}/{id2}/coFacilitateInvite', controller = 'facilitator', action = 'coFacilitateInvite', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/coFacilitateInvite/', controller = 'facilitator', action = 'coFacilitateInvite', id1 = '{id1}', id2 = '{id2}')

    map.connect('/profile/{id1}/{id2}/coFacilitateHandler', controller = 'facilitator', action = 'coFacilitateHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/coFacilitateHandler/', controller = 'facilitator', action = 'coFacilitateHandler', id1 = '{id1}', id2 = '{id2}')

    map.connect('/workshop/{id1}/{id2}/resignFacilitator', controller = 'facilitator', action = 'resignFacilitatorHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/workshop/{id1}/{id2}/resignFacilitator/', controller = 'facilitator', action = 'resignFacilitatorHandler', id1 = '{id1}', id2 = '{id2}')

    # Comments
    map.connect('/addComment', controller = 'comment', action = 'addComment')
    map.connect('/addComment/', controller = 'comment', action = 'addComment')
    
    # Comment flagging
    map.connect('/flagComment/{id1}', controller = 'comment', action = 'flagComment', id1 = '{id1}')

    # Comment editing
    map.connect('/comment/edit/{id1}', controller = 'comment', action = 'edit', id1 = '{id1}')

    # Comment modding
    map.connect('/adminComment/{id1}', controller = 'comment', action = 'adminComment', id1 = '{id1}')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modComment/{id5}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'suggestion')
    map.connect('/workshop/{id1}/{id2}/suggestion/{id3}/{id4}/modComment/{id5}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'suggestion')

    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modComment/{id5}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'resource')
    map.connect('/workshop/{id1}/{id2}/resource/{id3}/{id4}/modComment/{id5}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'resource')

    map.connect('/workshop/{id1}/{id2}/background/modComment/{id3}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = 'background', id5 = 'background', id6 = 'background')
    map.connect('/workshop/{id1}/{id2}/background/modComment/{id3}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = 'background', id5 = 'background', id6 = 'background')

    map.connect('/workshop/{id1}/{id2}/feedback/modComment/{id3}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = 'feedback', id5 = 'feedback', id6 = 'feedback')
    map.connect('/workshop/{id1}/{id2}/feedback/modComment/{id3}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = 'feedback', id5 = 'feedback', id6 = 'feedback')

    map.connect('/workshop/{id1}/{id2}/discussion/{id3}/{id4}/modComment/{id5}', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'discussion')
    map.connect('/workshop/{id1}/{id2}/discussion/{id3}/{id4}/modComment/{id5}/', controller = 'comment', action = 'modComment', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}', id6 = 'discussion')

    map.connect('/modCommentHandler/{id1}', controller = 'comment', action = 'modCommentHandler', id1 = '{id1}')
    map.connect('/modCommentHandler/{id1}/', controller = 'comment', action = 'modCommentHandler', id1 = '{id1}')
    map.connect('/clearCommentFlagsHandler/{id1}', controller = 'comment', action = 'clearCommentFlagsHandler', id1 = '{id1}')
    map.connect('/clearCommentFlagsHandler/{id1}/', controller = 'comment', action = 'clearCommentFlagsHandler', id1 = '{id1}')

    # Ratings
    map.connect('/rateSuggestion/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateSuggestion', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/rateFacilitation/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateFacilitation', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/rateResource/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateResource', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/rateDiscussion/{id1}/{id2}/{id3}', controller = 'rating', action = 'rateDiscussion', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/rateComment/{id1}/{id2}', controller = 'rating', action = 'rateComment', id1 = '{id1}', id2 = '{id2}')

    map.connect('/geoHandler/{id1}/{id2}', controller = 'geo', action = 'geoHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/postal/{id1}/{id2}', controller = 'geo', action = 'showPostalInfo', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/city/{id1}/{id2}/{id3}', controller = 'geo', action = 'showCityInfo', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/geo/county/{id1}/{id2}/{id3}', controller = 'geo', action = 'showCountyInfo', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/geo/state/{id1}/{id2}', controller = 'geo', action = 'showStateInfo', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/country/{id1}', controller = 'geo', action = 'showCountryInfo', id1 = '{id1}')

    # Temporary
    map.connect('/workshops/{id1}/{id2}/discussion', controller = 'discussion', action = 'index', id1 = '{id1}', id2 = '{id2}')
    

    ########################################################################################################
    # 
    # Online Survey specific routes
    # 
    ########################################################################################################

    # Surveys
    map.connect('/survey/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'display', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'display', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/surveys/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'display', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/surveys/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'display', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')

    map.connect('/showSurveys', controller = 'survey', action = 'showSurveys')
    map.connect('/showSurveys/', controller = 'survey', action = 'showSurveys')
    
    map.connect('/viewResults/{id1}/{id2}', controller = 'survey', action = 'viewResults', id1 = '{id1}', id2 = '{id2}')
    map.connect('/viewResults/{id1}/{id2}/', controller = 'survey', action = 'viewResults', id1 = '{id1}', id2 = '{id2}')
    map.connect('/generateResults/{id1}/{id2}', controller = 'survey', action = 'generateResults', id1 = '{id1}', id2 = '{id2}')
    map.connect('/generateResults/{id1}/{id2}/', controller = 'survey', action = 'generateResults', id1 = '{id1}', id2 = '{id2}')
    
    # Survey admin
    map.connect('/surveyAdmin', controller = 'survey', action = 'adminSurvey')
    map.connect('/surveyAdmin/', controller = 'survey', action = 'adminSurvey')
    map.connect('/surveyAdmin/setFeaturedSurvey', controller = 'survey', action = 'setFeaturedSurvey')
    map.connect('/surveyAdmin/setFeaturedSurvey/', controller = 'survey', action = 'setFeaturedSurvey')
    map.connect('/survey/addFacilitator', controller = 'survey', action = 'addFacilitator')
    map.connect('/survey/addFacilitator/', controller = 'survey', action = 'addFacilitator')
    map.connect('/survey/addAdmin', controller = 'survey', action = 'addAdmin')
    map.connect('/survey/addAdmin/', controller = 'survey', action = 'addAdmin')
    
    # Adding surveys
    map.connect('/addSurvey', controller = 'survey', action = 'addSurvey')
    map.connect('/addSurvey/handler', controller = 'survey', action = 'addSurveyHandler')
    
    # Editing surveys
    map.connect('/survey/{id1}/{id2}/edit', controller = 'survey', action = 'edit', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/edit/', controller = 'survey', action = 'edit', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/edit/handler', controller = 'survey', action = 'editHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/edit/handler/', controller = 'survey', action = 'editHandler', id1 = '{id1}', id2 = '{id2}')
    
    map.connect('/survey/{id1}/{id2}/upload', controller = 'survey', action = 'upload', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/upload/', controller = 'survey', action = 'upload', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/upload/handler', controller = 'survey', action = 'uploadSurveyHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/upload/handler/', controller = 'survey', action = 'uploadSurveyHandler', id1 = '{id1}', id2 = '{id2}')
    
    map.connect('/survey/{id1}/{id2}/addFacilitator', controller = 'survey', action = 'addFacilitatorToSurvey', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/addFacilitator/', controller = 'survey', action = 'addFacilitatorToSurvey', id1 = '{id1}', id2 = '{id2}')
    
    # Activating surveys
    map.connect('/survey/{id1}/{id2}/activate', controller = 'survey', action = 'activate', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/activate/', controller = 'survey', action = 'activate', id1 = '{id1}', id2 = '{id2}')
    
    # Submitting survey answers
    map.connect('/survey/submit/radio/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'submitRadio', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/radio/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'submitRadio', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/checkbox/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'submitCheckbox', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/checkbox/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'submitCheckbox', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/textarea/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'submitTextarea', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/textarea/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'submitTextarea', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/slider/{id1}/{id2}/{id3}/{id4}', controller = 'survey', action = 'submitSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/slider/{id1}/{id2}/{id3}/{id4}/', controller = 'survey', action = 'submitSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/multiSlider/{id1}/{id2}/{id3}/{id4}', controller = 'survey', action = 'submitMultiSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/multiSlider/{id1}/{id2}/{id3}/{id4}/', controller = 'survey', action = 'submitMultiSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/itemRank/{id1}/{id2}/page/{id3}', controller = 'survey', action = 'submitItemRank', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/itemRank/{id1}/{id2}/page/{id3}/', controller = 'survey', action = 'submitItemRank', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    
    ########################################################################################################
    # 
    # User routes
    # 
    ########################################################################################################
    
    # Login and signup
    map.connect('/login', controller = 'login', action = 'loginDisplay')
    map.connect('/login/', controller = 'login', action = 'loginDisplay')
    map.connect('/loginHandler', controller = 'login', action = 'loginHandler')
    map.connect('/loginHandler/', controller = 'login', action = 'loginHandler')
    map.connect('/signup', controller = 'register', action = 'signupDisplay')
    map.connect('/signup/', controller = 'register', action = 'signupDisplay')

    # User profile
    map.connect('/profile/{id1}/{id2}', controller = 'profile', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/', controller = 'profile', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/suggestions', controller = 'profile', action = 'showUserSuggestions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/suggestions/', controller = 'profile', action = 'showUserSuggestions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/resources', controller = 'profile', action = 'showUserResources', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/resources/', controller = 'profile', action = 'showUserResources', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/discussions', controller = 'profile', action = 'showUserDiscussions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/discussions/', controller = 'profile', action = 'showUserDiscussions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/comments', controller = 'profile', action = 'showUserComments', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/comments/', controller = 'profile', action = 'showUserComments', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/followers', controller = 'profile', action = 'showUserFollowers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/followers/', controller = 'profile', action = 'showUserFollowers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/following', controller = 'profile', action = 'showUserFollows', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/following/', controller = 'profile', action = 'showUserFollows', id1 = '{id1}', id2 = '{id2}')

    # User activation
    map.connect('/activate/*id', controller = 'activate', action = 'index') # Account Activation
    
    # User profile follow/unfollow
    map.connect('/profile/{id1}/{id2}/follow', controller = 'profile', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/follow/', controller = 'profile', action = 'followHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/unfollow', controller = 'profile', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/unfollow/', controller = 'profile', action = 'unfollowHandler', id1 = '{id1}', id2 = '{id2}')
    
    # User profile enable/disable
    map.connect('/profile/{id1}/{id2}/enable', controller = 'profile', action = 'enableHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/enable/', controller = 'profile', action = 'enableHandler', id1 = '{id1}', id2 = '{id2}')

    # User accessLevel
    map.connect('/profile/{id1}/{id2}/privs', controller = 'profile', action = 'privsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/privs/', controller = 'profile', action = 'privsHandler', id1 = '{id1}', id2 = '{id2}')

    # User admin
    map.connect('/profile/{id1}/{id2}/admin', controller = 'profile', action = 'userAdmin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/admin/', controller = 'profile', action = 'userAdmin', id1 = '{id1}', id2 = '{id2}')

    # User account admin
    map.connect('/profile/{id1}/{id2}/account', controller = 'account', action = 'accountAdminHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/account/', controller = 'account', action = 'accountAdminHandler', id1 = '{id1}', id2 = '{id2}')
    
    # Edit user info
    map.connect('/profile/edit', controller = 'profile', action = 'edit')
    map.connect('/profile/editSubmit', controller = 'profile', action = 'editSubmit')
    
    ################
    # Action Lists #
    ################
    
    map.connect('/help', controller = 'actionlist', action='help')
    map.connect('/help/', controller = 'actionlist', action='help')
    map.connect('/surveys', controller = 'actionlist', action='index', id='surveys')
    map.connect('/surveys/', controller = 'actionlist', action='index', id='surveys')

    
    map.connect('/sitemap', controller='actionlist', action='index', id='sitemap')
    map.connect('/workshops', controller='actionlist', action='index', id='sitemapIssues')
    map.connect('/searchWorkshops/{id1}/{id2}', controller='actionlist', action='searchWorkshops', id='searchWorkshops', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchWorkshops/{id1}/{id2}/', controller='actionlist', action='searchWorkshops', id='searchWorkshops', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchUsers/{id1}/{id2}', controller='actionlist', action='searchUsers', id='searchUsers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchUsers/{id1}/{id2}/', controller='actionlist', action='searchUsers', id='searchUsers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchTags/{id1}', controller='actionlist', action='searchTags', id='searchTags', id1 = '{id1}')
    map.connect('/searchTags/{id1}/', controller='actionlist', action='searchTags', id='searchTags', id1 = '{id1}')
    map.connect('/searchName/{id1}/{id2}/', controller='actionlist', action='searchName', id='searchName', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchName/{id1}/{id2}', controller='actionlist', action='searchName', id='searchName', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchGeoUsers/{id1}', controller='actionlist', action='searchGeoUsers', id='searchGeoUsers', id1 = '{id1}')
    map.connect('/searchGeoUsers/{id1}/', controller='actionlist', action='searchGeoUsers', id='searchGeoUsers', id1 = '{id1}')
    map.connect('/searchGeoWorkshops', controller='actionlist', action='searchGeoWorkshops', id='searchGeoWorkshops')
    map.connect('/searchGeoWorkshops/', controller='actionlist', action='searchGeoWorkshops', id='searchGeoWorkshops')
    

    ################
    # Application  #
    ################
    map.connect('/', controller = 'home', action = 'index' ) # load the homepage.
    
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
