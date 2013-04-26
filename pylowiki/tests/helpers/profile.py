# -*- coding: utf-8 -*-
from pylowiki.tests import *
import re

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.link_definitions as linkDefs
import pylowiki.tests.helpers.page_definitions as pageDefs

import logging
log = logging.getLogger(__name__)

def assertFollowing():
    return 'Following'

def editProfile(self, params, **kwargs):
    #: set the profile's edit form's parameters and return the parameters
    if 'name' in kwargs:
        name = kwargs['name']
    else:
        name = content.generateText(6)
    if 'email' in kwargs:
        email = kwargs['email']
    else:
        email = content.generateText(6) + '@' + content.generateText(7) + '.com'
    if 'postalCode' in kwargs:
        postalCode = kwargs['postalCode']
    else:
        postalCode = '92007'
    if 'greeting' in kwargs:
        greeting = kwargs['greeting']
    else:
        greeting = content.generateText(18)            
    if 'website' in kwargs:
        website = kwargs['website']
    else:
        website = 'www.' + content.generateText(12) + '.com'
    if 'websiteDesc' in kwargs:
        websiteDesc = kwargs['websiteDesc']
    else:
        websiteDesc = content.generateText(24)
    #: put these new values in the profile parameters
    params['member_name'] = name
    params['email'] = email
    params['postalCode'] = postalCode
    params['greetingMsg'] = greeting
    params['websiteLink'] = website
    params['websiteDesc'] = websiteDesc

    #: should we return the parameters?
    if 'returnParams' in kwargs:
        if kwargs['returnParams'] == True:
            return params

    #: if the parameters aren't wanted, it's time to edit the profile
    if 'expectErrors' in kwargs:
        if kwargs['expectErrors'] == True:
            #: try to update the profile, expect it not to work
            profileNotUpdated = self.app.post(
                url=str(kwargs['editForm'].action),
                params=params,
                status=404,
                expect_errors=True
            )
            return profileNotUpdated
        else:
            #: update the profile
            profileUpdated = self.app.post(
                url=str(kwargs['editForm'].action),
                params=params
            ).follow()
            return profileUpdated
    #: update the profile
    profileUpdated = self.app.post(
        url=str(kwargs['editForm'].action),
        params=params
    ).follow()
    return profileUpdated

def followThesePeople(self, followThese = []):
    for followThis in followThese:
        atThisUser = self.app.get(url=followThis.request.url)
        followResponse = followUser(self, atThisUser)
        itWorked = self.app.get(url=atThisUser.request.url)
        assert assertFollowing() in itWorked, "couldn't follow a user"

def followUser(self, profile):
    """ how best to find this button?
    find the text 'Follow' in the span tag
    find followButton in class of button tag, it remains constant
        <span class="button_container">
        <button data-URL-list="profile_4ICj_user-two" class="btn round pull-right followButton unfollow">
        btn round pull-right followButton unfollow
        btn round pull-right followButton unfollow following
        <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
        <span> Follow </span>
        </button>
    </span>
    post example http://todd.civinomics.org/profile/4ICd/todd-anderson/follow/handler
    data example profile_4ICg_andree-toddeoroas
    """
    profileSoup = profile.html
    followUrl = None
    followButton = profileSoup.find('button', attrs={'class' : re.compile("followButton")})
    log.info("found follow data: "+str(followButton['data-url-list']))
    #: post to the form's url to disable the conversation
    if followButton is not None:
        followData = str(followButton['data-url-list'])
        followUrl = makeFollowUrl(followData)
        followResponse = self.app.post(
            url=str(followUrl)            
        )
        return followResponse
    else:
        return False

def getResources(self, profilePage):
    return profilePage.click(description=linkDefs.profileResources(), index=0)

def getConversations(self, profilePage):
    return profilePage.click(description=linkDefs.profileConversations(), index=0)

def getIdeas(self, profilePage):
    return profilePage.click(description=linkDefs.profileIdeas(), index=0)

def getObjectsPage(self, profilePage):
    """ figure out which object, go to that listing page and return it """
    return thatObjectPage.click(description=linkDefs.addConversation(), index=0)

def getEditPage(self, profilePage):
    """ return the profile editing page """
    return profilePage.click(description=linkDefs.profileEditPage(), index=0)

def getFollowingPage(self, profilePage):
    """ return the following page """
    return profilePage.click(description=linkDefs.profileFollowingPage(), index=0)

def getProfilePage(self, aPage):
    """ Returns the profile page by clicking on the profile link up top. """
    return aPage.click(description=linkDefs.profilePage())

def loginGetProfilePageLogout(self, user, **kwargs):
    """ returns the profile page for this user """
    if 'login' in kwargs:
        if kwargs['login'] == True:
            authorization.login(self, user)
    else:
        #: if there's no mention of this parameter, the default action is to log the user in
        authorization.login(self, user)
    mainPage = self.app.get(pageDefs.allWorkshops())
    userProfile = getProfilePage(self, mainPage)
    authorization.logout(self)
    return userProfile

def makeFollowUrl(followData):
    """ takes the data from the follow button """
    dataParts = followData.split('_')
    return '/'+dataParts[0]+'/'+dataParts[1]+'/'+dataParts[2]+'/follow/handler'

