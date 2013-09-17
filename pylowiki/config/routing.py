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
    map.connect('/{systemAdmin:systemAdmin/?}', controller = 'systemAdmin', action = 'index')
    map.connect('/systemAdmin/{handler:handler/?}', controller = 'systemAdmin', action = 'handler')
    map.connect('/admin/show/{objectType}{end:s/?}', controller = 'admin')
    
    ########################################################################################################
    # 
    # Corporate routes
    # 
    ########################################################################################################
    map.connect('/corp/', controller = 'corp', action = 'index', id = 'None')
    map.connect('/corp/about', controller = 'corp', action = 'about')
    map.connect('/corp/careers', controller = 'corp', action = 'careers')
    map.connect('/corp/careers/{id}', controller = 'corp', action = 'displayCareer', id = '{id}')
    map.connect('/corp/team', controller = 'corp', action = 'team')
    map.connect('/corp/terms', controller = 'corp', action = 'terms')
    map.connect('/corp/privacy', controller = 'corp', action = 'privacy')
    map.connect('/corp/outreach', controller = 'corp', action = 'outreach')
    map.connect('/corp/contact', controller = 'corp', action = 'contact')
    map.connect('/corp/caseStudies/{id}', controller = 'corp', action = 'displayCaseStudy', id = '{id}')
    map.connect('/corp/caseStudies', controller = 'corp', action = 'caseStudies')
    map.connect('/corp/polling', controller = 'corp', action = 'polling')

    ########################################################################################################
    # 
    # Platform-specific routes
    # 
    ########################################################################################################

    map.connect('/comment/{id}', controller = 'comment', action = 'index', id = '{id}')
    map.connect('/moderation', controller = 'moderation', action = 'index')
    map.connect('/moderation/handler/{id}', controller = 'moderation', action = 'handler', id = '{id}')
    map.connect('/moderation/{id1}/{id2}', controller = 'moderation', action = 'index', id1 = '{id1}', id2 = '{id2}')
    map.connect('/rating', controller = 'rating', action = 'index')
    map.connect('/admin', controller = 'admin', action = 'index')
    #map.connect('/suggestion/rate', controller = 'suggestion', action = 'rate')
    map.connect('/slideshow/edit', controller = 'slideshow', action = 'edit')

    # Geo stuff
    map.connect('/geoHandler/{id1}/{id2}', controller = 'geo', action = 'geoHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/stateList/{id1}', controller = 'geo', action = 'geoStateHandler', id1 = '{id1}')
    map.connect('/geo/countyList/{id1}/{id2}', controller = 'geo', action = 'geoCountyHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/geo/cityList/{id1}/{id2}/{id3}', controller = 'geo', action = 'geoCityHandler', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/geo/cityStateCountry/{id1}{end:/?}', controller = 'geo', action = 'geoCityStateCountryHandler', id1 = '{id1}')
    map.connect('/geo/cityStateCountryLink/{id1}{end:/?}', controller = 'geo', action = 'geoCityStateCountryLinkHandler', id1 = '{id1}')
    map.connect('/geo/postalList/{id1}/{id2}/{id3}/{id4}', controller = 'geo', action = 'geoPostalHandler', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')

    # Geo rss stuff
    map.connect('/workshops/rss/earth{end:/?}', controller = 'geo', action = 'rss')
    map.connect('/workshops/rss/earth/{country}{end:/?}', controller = 'geo', action = 'rss')
    map.connect('/workshops/rss/earth/{country}/{state}{end:/?}', controller = 'geo', action = 'rss')
    map.connect('/workshops/rss/earth/{country}/{state}/{county}{end:/?}', controller = 'geo', action = 'rss')
    map.connect('/workshops/rss/earth/{country}/{state}/{county}/{city}{end:/?}', controller = 'geo', action = 'rss')
    map.connect('/workshops/rss/earth/{country}/{state}/{county}/{city}/{postalCode}{end:/?}', controller = 'geo', action = 'rss')
    
    # Workshop Base
    map.connect('/{workshop:workshops?}/display/create/{form:form/?}', controller = 'workshop', action = 'displayCreateForm')
    map.connect('/{workshop:workshops?}/create/{handler:handler/?}', controller = 'workshop', action = 'createWorkshopHandler')
    map.connect('/{workshop:workshops?}/display/payment/{form:form/?}', controller = 'workshop', action = 'displayPaymentForm')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/upgrade/{handler:handler/?}', controller = 'workshop', action = 'upgradeHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}{end:/|}', controller = 'workshop', action = 'display', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/guest/{guestCode}/{workshopCode}{end:/|}', controller = 'workshop', action = 'guest', guestCode = '{guestCode}', workshopCode = '{workshopCode}')
    map.connect('/{workshop:workshops?}/{code}/{workshopURL}/follow/{handler:handler/?}', controller = 'follow', action = 'followHandler', code = '{code}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{background:background/?}', controller = 'workshop', action = 'background', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{preferences:preferences/?}', controller = 'workshop', action = 'preferences', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/feedback{end:/?}', controller = 'workshop', action = 'feedback', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    # These two are duplicated
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{admin:admin/?}', controller = 'workshop', action = 'admin', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{administrate:administrate/?}', controller = 'workshop', action = 'admin', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{adminWorkshopHandler:adminWorkshopHandler/?}', controller = 'workshop', action = 'adminWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')

    # Workshop configuration submit handler
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/publish/handler{end:/?}', controller = 'workshop', action = 'publishWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configureBasicWorkshopHandler{end:/?}', controller = 'workshop', action = 'configureBasicWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configureScopeWorkshopHandler{end:/?}', controller = 'workshop', action = 'configureScopeWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configureStartWorkshopHandler{end:/?}', controller = 'workshop', action = 'configureStartWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configureTagsWorkshopHandler{end:/?}', controller = 'workshop', action = 'configureTagsWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configurePrivateWorkshopHandler{end:/?}', controller = 'workshop', action = 'configurePrivateWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/previewInvitation{end:/?}', controller = 'workshop', action = 'previewInvitation', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listPrivateMembersHandler{end:/?}', controller = 'workshop', action = 'listPrivateMembersHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configurePublicWorkshopHandler{end:/?}', controller = 'workshop', action = 'configurePublicWorkshopHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/configureContinueHandler{end:/?}', controller = 'workshop', action = 'preferences', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/update/background/handler{end:/?}', controller = 'wiki', action = 'updateBackgroundHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    
    # workshop activity feeds
    map.connect('/activity/rss{end:/?}', controller='actionlist', action='rss')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/rss{end:/?}', controller = 'workshop', action = 'rss')    

    # Workshop follower, private member notifications
    map.connect('/{workshop:workshops?}/{workshopCode}/{url}/follow/{userCode}/notifications/{handler:handler/?}', controller = 'follow', action = 'followerNotificationHandler', workshopCode = '{workshopCode}', url='{url}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/private/{userCode}/notifications/{handler:handler/?}', controller = 'workshop', action = 'pmemberNotificationHandler', workshopCode = '{workshopCode}', workshopURL='{workshopURL}', userCode = '{userCode}')
    
    # Workshop goals
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/goals/add{end:/?}', controller = 'goals', action = 'add')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/goals/get{end:/?}', controller = 'goals', action = 'getGoals')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/goals/{goalCode}/update{end:/?}', controller = 'goals', action = 'update')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/goals/{goalCode}/delete{end:/?}', controller = 'goals', action = 'delete')

    # Workshop slideshow
    map.connect('/{workshop:workshops?}/{parentCode}/{parentURL}/addImages/{handler:handler/?}', controller = 'slideshow', action = 'addImageHandler')
    map.connect('/{workshop:workshops?}/{parentCode}/{parentURL}/slide/edit', controller = 'slideshow', action = 'edit')
    map.connect('/{workshop:workshops?}/{parentCode}/{parentURL}/slide/edit/position', controller = 'slideshow', action = 'editPosition')

    # Account handler routines
    map.connect('/workshop/{workshopCode}/{workshopURL}/manage/{account:account/?}', controller = 'account', action = 'manageAccount', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/account/{accountCode}/update/billingContact/{handler:handler/?}', controller = 'account', action = 'updateBillingContactHandler', accountCode = '{accountCode}')
    map.connect('/account/{accountCode}/update/paymentInfo/{handler:handler/?}', controller = 'account', action = 'updatePaymentInfoHandler', accountCode = '{accountCode}')
    map.connect('/account/{accountCode}/close/{handler:handler/?}', controller = 'account', action = 'closeHandler', accountCode = '{accountCode}')

    # suggestions
    """
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{suggestions:suggestions?/?}', controller = 'workshop', action = 'displayAllSuggestions', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/addSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'addSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/newSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'newSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/editSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'editSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/saveSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'saveSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/{workshop:workshops?}/{id1}/{id2}/{suggestion:suggestions?}/{id3}/{id4}{end:/?}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '')
    map.connect('/{workshop:workshops?}/{id1}/{id2}/{suggestion:suggestions?}/{id3}/{id4}/{id5}{end:/?}', controller = 'suggestion', action = 'index', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}', id5 = '{id5}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{inactiveSuggestions:inactiveSuggestions/?}', controller = 'workshop', action = 'inactiveSuggestions', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/flagSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'flagSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/modSuggestion/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'modSuggestion', id1 = '{id1}', id2 = '{id2}')
    map.connect('/clearSuggestionFlagsHandler/{id1}/{id2}{end:/?}', controller = 'suggestion', action = 'clearSuggestionFlagsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/{modSuggestionHandler:modSuggestionHandler/?}', controller = 'suggestion', action = 'modSuggestionHandler')
    map.connect('/{adoptSuggestionHandler:adoptSuggestionHandler/?}', controller = 'suggestion', action = 'adoptSuggestionHandler')
    map.connect('/{noteSuggestionHandler:noteSuggestionHandler/?}', controller = 'suggestion', action = 'noteSuggestionHandler')
    """
    
    # info
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{information:information?/?}', controller = 'workshop', action = 'info', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    
    # activity
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{activity:activity?/?}', controller = 'workshop', action = 'activity', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    
    # resources
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{resources:resources?/?}', controller = 'resource', action = 'listing') 
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/{resource:resource/?}', controller = 'resource', action = 'addResource') 
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/resource/{handler:handler/?}', controller = 'resource', action = 'addResourceHandler') 
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{resource:resources?}/{resourceCode}/{resourceURL}{end:/?}', controller = 'resource', action = 'showResource') 
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{resource:resources?}/{resourceCode}/{resourceURL}/thread/{commentCode}{end:/?}', controller = 'resource', action = 'thread') 
    
    # discussions
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{discussion:discussions?/?}', controller = 'discussion', action = 'index', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/{discussion:discussions?/?}', controller = 'discussion', action = 'addDiscussion', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/discussion/{handler:handler/?}', controller = 'discussion', action = 'addDiscussionHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{discussion:discussions?}/{discussionCode}/{discussionURL}{end:/?}', controller = 'discussion', action = 'topic', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', discussionCode = '{discussionCode}', discussionURL = '{discussionURL}', revisionCode = '')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{discussion:discussions?}/{discussionCode}/{discussionURL}/thread/{revisionCode}{end:/?}', controller = 'discussion', action = 'thread', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', discussionCode = '{discussionCode}', discussionURL = '{discussionURL}', revisionCode = '{revisionCode}')

    # Ideas
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{ideas:ideas?/?}', controller = 'workshop', action = 'display', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/{idea:ideas?/?}', controller = 'idea', action = 'addIdea', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/add/{idea:ideas?}/{handler:handler/?}', controller = 'idea', action = 'addIdeaHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{idea:ideas?}/{ideaCode}/{ideaURL}{end:/?}', controller = 'idea', action = 'showIdea', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', ideaCode = '{ideaCode}', ideaURL = '{ideaURL}')    
    # ADD HERE: threaded discussion route

    # Cofacilitation invitation and response
    map.connect('/profile/{code}/{url}/facilitate/invite/{handler:handler/?}', controller = 'facilitator', action = 'facilitateInviteHandler', code = '{code}', url='{url}')
    map.connect('/profile/{code}/{url}/facilitate/response/{handler:handler/?}', controller = 'facilitator', action = 'facilitateResponseHandler', code = '{code}', url='{url}')
    map.connect('/{workshop:workshops?}/{code}/{url}/facilitate/resign/{handler:handler/?}', controller = 'facilitator', action = 'facilitateResignHandler', code = '{code}', url='{url}')

    # Facilitator notifications
    map.connect('/{workshop:workshops?}/{code}/{url}/facilitate/{userCode}/notifications/{handler:handler/?}', controller = 'facilitator', action = 'facilitatorNotificationHandler', code = '{code}', url='{url}', userCode = '{userCode}')
    
    # Listener management
    map.connect('/profile/{userCode}/{userURL}/listener/invite/{handler:handler/?}', controller = 'listener', action = 'listenerInviteHandler', userCode = '{userCode}', userURL = '{userURL}')
    map.connect('/profile/{userCode}/{userURL}/listener/response/{handler:handler/?}', controller = 'listener', action = 'listenerResponseHandler', userCode = '{userCode}', userURL = '{userURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/resign/{handler:handler/?}', controller = 'listener', action = 'listenerResignHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/add/{handler:handler/?}', controller = 'listener', action = 'listenerAddHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/edit/{handler:handler/?}', controller = 'listener', action = 'listenerEditHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/disable/{handler:handler/?}', controller = 'listener', action = 'listenerDisableHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/email/{handler:handler/?}', controller = 'listener', action = 'listenerEmailHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/suggest/{handler:handler/?}', controller = 'listener', action = 'listenerSuggestHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/{userCode}/list/{handler:handler/?}', controller = 'listener', action = 'listenerListHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/listener/title/{handler:handler/?}', controller = 'listener', action = 'listenerTitleHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}')

    # Share management
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/share/{userCode}/email/{handler:handler/?}', controller = 'share', action = 'shareEmailHandler', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', userCode = '{userCode}')
    
    map.connect('/share/facebook/{userCode}/{workshopCode}/{itemCode}/{itemURL}/{postId}', controller = 'share', action = 'shareFacebookHandler', userCode = '{userCode}', workshopCode = '{workshopCode}', itemCode = '{itemCode}', itemURL = '{itemURL}', postId = '{postId}')

    # Comment notifications
    map.connect('/profile/preferences/{id1}/{id2}/comments/{handler:handler/?}', controller = 'profile', action = 'preferencesCommentsHandler', id1 = '{id1}', id2 = '{id2}')
    
    # Listener notifications
    map.connect('/{workshop:workshops?}/{workshopCode}/{url}/listen/{userCode}/notifications/{handler:handler/?}', controller = 'listener', action = 'listenerNotificationHandler', workshopCode = '{workshopCode}', url='{url}', userCode = '{userCode}')
    
    # Comments
    map.connect('/{comment:comments?}/add/{handler:handler/?}', controller = 'comment', action = 'commentAddHandler')
    map.connect('/{workshop:workshops?}/{workshopCode}/{workshopURL}/{comment:comments?}/{revisionCode}{end:/?}', controller = 'comment', action = 'permalink')
    map.connect('/profile/{userCode}/{userURL}/{comment:comments?}/{revisionCode}{end:/?}', controller = 'comment', action = 'permalinkPhoto')

    # Ratings
    #map.connect('/rate/suggestion/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'rateSuggestion', code = '{code}', url = '{url}', amount = '{amount}')
    map.connect('/rateFacilitation/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'rateFacilitation', code = '{code}', url = '{url}', amount = '{amount}')
    map.connect('/rate/resource/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'rateResource', code = '{code}', url = '{url}', amount = '{amount}')
    map.connect('/rate/discussion/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'rateDiscussion', code = '{code}', url = '{url}', amount = '{amount}')
    map.connect('/rate/photo/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'ratePhoto', code = '{code}', url = '{url}', amount = '{amount}')
    map.connect('/rate/comment/{code}/{amount}{end:/?}', controller = 'rating', action = 'rateComment', code = '{code}', amount = '{amount}')
    map.connect('/rate/idea/{code}/{url}/{amount}{end:/?}', controller = 'rating', action = 'rateIdea', code = '{code}', url = '{url}', amount = '{amount}')
    
    # Disable/enable/delete/edit/flag Things
    map.connect('/disable/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'disable')
    map.connect('/enable/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'enable')
    map.connect('/delete/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'delete')
    map.connect('/edit/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'edit')
    map.connect('/flag/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'flag')
    map.connect('/publish/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'publish')
    map.connect('/unpublish/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'unpublish')
    map.connect('/immunify/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'immunify')
    map.connect('/adopt/{objType}/{thingCode}{end:/?}', controller = 'admin', action = 'adopt')
    map.connect('/demo/set/{thingCode}{end:/?}', controller = 'admin', action='setDemo')
    
    ########################################################################################################
    # 
    # Online Survey specific routes  map.connec
    # 
    ########################################################################################################

    # Surveys
    map.connect('/{survey:surveys?}/{id1}/{id2}/page/{id3}{end:/?}', controller = 'survey', action = 'display', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/{showSurveys:showSurveys/?}', controller = 'survey', action = 'showSurveys')
    map.connect('/viewResults/{id1}/{id2}{end:/?}', controller = 'survey', action = 'viewResults', id1 = '{id1}', id2 = '{id2}')
    map.connect('/generateResults/{id1}/{id2}{end:/?}', controller = 'survey', action = 'generateResults', id1 = '{id1}', id2 = '{id2}')

    # Survey admin
    map.connect('/{surveyAdmin:surveyAdmin/?}', controller = 'survey', action = 'adminSurvey')
    map.connect('/surveyAdmin/{setFeaturedSurvey:setFeaturedSurvey/?}', controller = 'survey', action = 'setFeaturedSurvey')
    map.connect('/survey/{addFacilitator:addFacilitator/?}', controller = 'survey', action = 'addFacilitator')
    map.connect('/survey/{addAdmin:addAdmin/?}', controller = 'survey', action = 'addAdmin')

    # Adding surveys
    map.connect('/{addSurvey:addSurvey/?}', controller = 'survey', action = 'addSurvey')
    map.connect('/addSurvey/{handler:handler/?}', controller = 'survey', action = 'addSurveyHandler')
    
    # Editing surveys
    map.connect('/survey/{id1}/{id2}/{edit:edit/?}', controller = 'survey', action = 'edit', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/edit/{handler:handler/?}', controller = 'survey', action = 'editHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/{upload:upload/?}', controller = 'survey', action = 'upload', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/upload/{handler:handler/?}', controller = 'survey', action = 'uploadSurveyHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/survey/{id1}/{id2}/{addFacilitator:addFacilitator/?}', controller = 'survey', action = 'addFacilitatorToSurvey', id1 = '{id1}', id2 = '{id2}')
    
    # Activating surveys
    map.connect('/survey/{id1}/{id2}/{activate:activate/?}', controller = 'survey', action = 'activate', id1 = '{id1}', id2 = '{id2}')
    
    # Submitting survey answers
    map.connect('/survey/submit/radio/{id1}/{id2}/page/{id3}{end:/?}', controller = 'survey', action = 'submitRadio', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/checkbox/{id1}/{id2}/page/{id3}{end:/?}', controller = 'survey', action = 'submitCheckbox', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/textarea/{id1}/{id2}/page/{id3}{end:/?}', controller = 'survey', action = 'submitTextarea', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/survey/submit/slider/{id1}/{id2}/{id3}/{id4}{end:/?}', controller = 'survey', action = 'submitSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/multiSlider/{id1}/{id2}/{id3}/{id4}{end:/?}', controller = 'survey', action = 'submitMultiSlider', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}', id4 = '{id4}')
    map.connect('/survey/submit/itemRank/{id1}/{id2}/page/{id3}{end:/?}', controller = 'survey', action = 'submitItemRank', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    
    ########################################################################################################
    # 
    # User routes
    # 
    ########################################################################################################
    
    # Login and signup
    map.connect('/login{end:/?}', controller = 'login', action = 'loginDisplay', workshopCode = 'None', workshopURL = 'None', thing = 'None', thingCode = 'None', thingURL = 'None')
    map.connect('/loginNoExtAuth{end:/?}', controller = 'login', action = 'loginNoExtAuthDisplay', workshopCode = 'None', workshopURL = 'None', thing = 'None', thingCode = 'None', thingURL = 'None')
    map.connect('/workshop/{workshopCode}/{workshopURL}/login{end:/?}', controller = 'login', action = 'loginDisplay', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', thing = 'None', thingCode = 'None', thingURL = 'None')
    map.connect('/workshop/{workshopCode}/{workshopURL}/login/{thing}{end:/?}', controller = 'login', action = 'loginDisplay', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', thing = '{thing}', thingCode = 'None', thingURL = 'None')
    map.connect('/workshop/{workshopCode}/{workshopURL}/clogin/{thing}/{thingCode}/{thingURL}{end:/?}', controller = 'login', action = 'loginDisplay', workshopCode = '{workshopCode}', workshopURL = '{workshopURL}', thing = '{thing}', thingCode = '{thingCode}', thingURL = '{thingURL}')
    map.connect('/{loginHandler:loginHandler/?}', controller = 'login', action = 'loginHandler')
    map.connect('/{signup:signup/?}', controller = 'register', action = 'signupDisplay')
    map.connect('/{signupNoExtAuth:signupNoExtAuth/?}', controller = 'register', action = 'signupNoExtAuthDisplay')
    map.connect('/signup/handler{end:/?}', controller = 'register', action= 'signupHandler')
    map.connect('/{forgotPassword:forgotPassword/?}', controller = 'login', action = 'forgotPassword')
    map.connect('/{forgotPasswordHandler:forgotPasswordHandler/?}', controller = 'login', action = 'forgot_handler')

    # external authentication routes
    map.connect('/fbLogin{end:/?}', controller = 'login', action = 'fbLoginHandler')
    map.connect('/fbLoggingIn{end:/?}', controller = 'login', action = 'fbLoggingIn')
    map.connect('/fbNewAccount{end:/?}', controller = 'register', action = 'fbNewAccount')
    map.connect('/signup/fbSignUp{end:/?}', controller = 'register', action = 'fbSignUpDisplay')
    map.connect('/signup/fbSigningUp{end:/?}', controller = 'register', action = 'fbSigningUp')
    map.connect('/{flogin:flogin/?}', controller = 'flogin', action = 'login')
    
    # for ajax request from page after pinging fb for auth info
    map.connect('/extauth/fbEmail/{id1}{end:/?}', controller = 'login', action = 'fbAuthCheckEmail', id1 = '{id1}')
    map.connect('/extauth/fbProfilePicSmall/{id1}{end:/?}', controller = 'profile', action = 'fbProfilePicSmall', id1 = '{id1}')

    # User activation
    map.connect('/activate/*id', controller = 'activate', action = 'index')

    # User profile
    map.connect('/profile/{id1}/{id2}{end:/?}', controller = 'profile', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}', id3 = '')
    map.connect('/profile/{id1}/{id2}/revision/{id3}{end:/?}', controller = 'profile', action = 'showUserPage', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    #map.connect('/profile/{id1}/{id2}/{suggestions:suggestions/?}', controller = 'profile', action = 'showUserSuggestions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{resources:resources/?}', controller = 'profile', action = 'showUserResources', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{discussions:discussions/?}', controller = 'profile', action = 'showUserDiscussions', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{ideas:ideas/?}', controller = 'profile', action = 'showUserIdeas', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{watching:watching/?}', controller = 'profile', action = 'showUserWatching', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{pictures:pictures/?}', controller = 'profile', action = 'showUserPhotos', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{listening:listening/?}', controller = 'profile', action = 'showUserListening', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{facilitating:facilitating/?}', controller = 'profile', action = 'showUserFacilitating', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{comments:comments/?}', controller = 'profile', action = 'showUserComments', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{followers:followers/?}', controller = 'profile', action = 'showUserFollowers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{following:following/?}', controller = 'profile', action = 'showUserFollows', id1 = '{id1}', id2 = '{id2}')
    #map.connect('/profile/{id1}/{id2}/stats.json', controller = 'profile', action = 'stats', id1 = '{id1}', id2 = '{id2}')
    #map.connect('/profile/{id1}/{id2}/stats.csv', controller = 'profile', action = 'statsCSV', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{code}/{id2}/follow/{handler:handler/?}', controller = 'follow', action = 'followHandler', code = '{code}')
    map.connect('/profile/{id1}/{id2}/enable/{handler:handler/?}', controller = 'profile', action = 'enableHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/privs/{handler:handler/?}', controller = 'profile', action = 'privsHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/{admin:admin/?}', controller = 'profile', action = 'userAdmin', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{edit:edit/?}', controller = 'profile', action = 'edit')
    map.connect('/profile/{editSubmit:editSubmit/?}', controller = 'profile', action = 'editSubmit')
    map.connect('/profile/{id1}/{id2}/{edit:edit/?}', controller = 'profile', action = 'edit', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/edit/info/{handler:handler/?}', controller = 'profile', action = 'infoEditHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/picture/upload/{handler:handler/?}', controller = 'profile', action = 'pictureUploadHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/photo/upload/{handler:handler/?}', controller = 'profile', action = 'photoUploadHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/photo/{id3}/update/{handler:handler/?}', controller = 'profile', action = 'photoUpdateHandler', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/profile/{id1}/{id2}/photo/show/{id3}{end:/?}', controller = 'profile', action = 'showUserPhoto', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/profile/{id1}/{id2}/photos/show{end:/?}', controller = 'profile', action = 'showUserPhotos', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/picture/set/image/source{end:/?}', controller = 'profile', action = 'setImageSource')
    map.connect('/profile/{id1}/{id2}/password/update/{handler:handler/?}', controller = 'profile', action = 'passwordUpdateHandler', id1 = '{id1}', id2 = '{id2}')
    map.connect('/profile/{id1}/{id2}/search/workshop/tag/{id3}', controller = 'profile', action = 'searchWorkshopTag', id1 = '{id1}', id2 = '{id2}', id3 = '{id3}')
    map.connect('/profile/{id1}/{id2}/archives', controller = 'profile', action = 'showUserArchives', id1 = '{id1}', id2 = '{id2}')
    
    ################
    # Messaging    #
    ################
    map.connect('/messages/{id1}/{id2}{end:/?}', controller = 'profile', action = 'showUserMessages', id1 = '{id1}', id2 = '{id2}', id3 = '')
    map.connect('/message/{urlCode}/mark/read{end:/?}', controller = 'message', action = 'markRead')
    
    ################
    # Action Lists #
    ################
    
    map.connect('/{help:help/?}', controller = 'help', action='help')
    map.connect('/help/{facilitatorGuide:facilitatorGuide/?}', controller = 'help', action='facilitatorGuide')
    map.connect('/help/{faq:faq/?}', controller = 'help', action='faq')
    map.connect('/help/{reportIssue:reportIssue/?}', controller = 'help', action='reportIssue')
    map.connect('/help/{reportAbuse:reportAbuse/?}', controller = 'help', action='reportAbuse')
    map.connect('/help/{abuseHandler:abuseHandler/?}', controller = 'help', action='abuseHandler')
    map.connect('/help/{feedbackWorkshop:feedbackWorkshop/?}', controller = 'help', action='feedbackWorkshop')
    map.connect('/{surveys:surveys/?}', controller = 'actionlist', action='index', id='surveys')
    map.connect('/{sitemap:sitemap/?}', controller='actionlist', action='index', id='sitemap')
    map.connect('/{workshop:workshops?/?}', controller='actionlist', action='index', id='sitemapIssues')
    map.connect('/searchWorkshops/{id1}/{id2}{end:/?}', controller='actionlist', action='searchWorkshops', id='searchWorkshops', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchUsers/{id1}/{id2}{end:/?}', controller='actionlist', action='searchUsers', id='searchUsers', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchName/{id1}/{id2}{end:/?}', controller='actionlist', action='searchName', id='searchName', id1 = '{id1}', id2 = '{id2}')
    map.connect('/searchGeoUsers/{id1}{end:/?}', controller='actionlist', action='searchGeoUsers', id='searchGeoUsers', id1 = '{id1}')
    map.connect('/{searchGeoWorkshops:searchGeoWorkshops/?}', controller='actionlist', action='searchGeoWorkshops', id='searchGeoWorkshops')

    ################
    # Search       #
    ################

    map.connect('/search{end:/?}', controller = 'search', action = 'search')
    map.connect('/search/workshops/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchWorkshops', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/search/people/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchPeople', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/search/resources/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchResources', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/search/discussions/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchDiscussions', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/search/ideas/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchIdeas', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/search/photos/{searchType}/{searchString}{end:/?}', controller = 'search', action = 'searchPhotos', searchType = '{searchType}', searchString = '{searchString}')
    map.connect('/searchTags/{id1}{end:/?}', controller='search', action='searchWorkshopCategoryTags', id1 = '{id1}')
    map.connect('/workshops/geo/{planet}/', controller = 'search', action = 'searchWorkshopGeo', country = 'united-states')
    map.connect('/workshops/geo/{planet}/{country}{end:/?}', controller = 'search', action = 'searchWorkshopGeo')
    map.connect('/workshops/geo/{planet}/{country}/{state}{end:/?}', controller = 'search', action = 'searchWorkshopGeo')
    map.connect('/workshops/geo/{planet}/{country}/{state}/{county}{end:/?}', controller = 'search', action = 'searchWorkshopGeo')
    map.connect('/workshops/geo/{planet}/{country}/{state}/{county}/{city}{end:/?}', controller = 'search', action = 'searchWorkshopGeo')
    map.connect('/workshops/geo/{planet}/{country}/{state}/{county}/{city}/{postalCode}{end:/?}', controller = 'search', action = 'searchWorkshopGeo')

    ################
    # Application  #
    ################
    map.connect('/', controller = 'home', action = 'index' ) # load the homepage.
    
    map.connect('/{controller}', controller='{controller}', action='index') # Maps url to controller index
    map.connect('/{controller}/', controller = '{controller}', action = 'index')
    map.connect('/{controller}/{action}', controller='{controller}', action='{action}')
    map.connect('/{controller}/{action}/', controller='{controller}', action='{action}')
    map.connect('/{controller}/{action}/{id}')
    
    return map
