from pylowiki.tests import *

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.noun_verb_actions as nounAction
import pylowiki.tests.helpers.page_definitions as pageDefs
import pylowiki.tests.helpers.profile as profile
import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop

class TestProfileController(TestController):

    def edit_profile(self):
        """ set up a profile, make sure the user and can edit it. then make sure other roles can't """
        name1 = 'ima newuser'
        name2 = 'ive changedmyname'
        name3 = 'admin changedIt'
        email1 = 'testinemail@civinomics.com'
        email2 = 'newemail@civinomics.com'
        email3 = 'thirde@civ.net'
        postal1 = '95060'
        postal2 = '95067'
        postal3 = '95065'
        greeting = 'hey there im a friendly civinom'
        greeting2 = 'admin says your greeting is old'
        website = 'www.imcool.org'
        website2 = 'www.nerd.com'
        websiteDesc = 'its a really cool website'
        websiteDesc2 = 'my website is better'
        #: create a person
        user = registration.create_and_activate_a_user(self, postal=postal1, name=name1, email=email1)
        admin = registration.create_and_activate_a_user(self, accessLevel='200')
        #: login
        loggedIn = authorization.login(self, user)
        #: go to the profile page
        mainPage = self.app.get(pageDefs.allWorkshops())
        profilePage = profile.getProfilePage(self, mainPage)
        #: grab the edit form
        editForm = profilePage.forms[formDefs.profile_edit()]
        editParams = {}
        editParams = formHelpers.loadWithSubmitFields(editForm)
        #: set the new values
        profileUpdated = profile.editProfile(
            self,
            editParams,
            name=name2, 
            email=email2,
            postalCode=postal2,
            greeting=greeting, 
            website=website,
            websiteDesc=websiteDesc,
            editForm=editForm
        )
        #: make sure it worked
        assert name2 in profileUpdated
        assert email2 in profileUpdated
        assert postal2 in profileUpdated
        assert greeting in profileUpdated
        assert website in profileUpdated
        assert websiteDesc in profileUpdated
        #: switch to admin
        authorization.logout(self)
        authorization.login(self, admin)
        #: reload the user's profile page
        profilePage2 = self.app.get(url=profileUpdated.request.url)
        #: grab the edit form
        editForm2 = profilePage2.forms[formDefs.profile_edit()]
        editParams2 = {}
        editParams2 = formHelpers.loadWithSubmitFields(editForm)
        #: set new values
        profileUpdated2 = profile.editProfile(
            self,
            editParams2,
            name=name3, 
            email=email3,
            postalCode=postal3,
            greeting=greeting2, 
            website=website2,
            websiteDesc=websiteDesc2,
            editForm=editForm2
        )
        #: make sure it worked
        assert name3 in profileUpdated2
        assert email3 in profileUpdated2
        assert postal3 in profileUpdated2
        assert greeting2 in profileUpdated2
        assert website2 in profileUpdated2
        assert websiteDesc2 in profileUpdated2
        #: update the user's email so login still works
        user['email'] = email3
        #: now make sure other roles can't do this
        #: public
        authorization.logout(self)
        profileNotUpdated = profile.editProfile(
            self,
            editParams2,
            editForm=editForm2,
            expectErrors=True
        )
        #: make sure the info is still the same        
        authorization.login(self, user)
        mainPage = self.app.get(pageDefs.allWorkshops())
        profilePage = profile.getProfilePage(self, mainPage)
        assert name3 in profilePage
        assert email3 in profilePage
        assert postal3 in profilePage
        assert greeting2 in profilePage
        assert website2 in profilePage
        assert websiteDesc2 in profilePage
        authorization.logout(self)
        #: test as a guest
        guest = registration.create_and_activate_a_user(self, postal='92007', name='Guest')
        facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        #: create a workshop
        workshopTitle = 'workshop objects'
        newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: invite a guest
        guestLink = workshop.inviteGuest(self, newWorkshop, email=guest['email'], guestLink=True)
        authorization.logout(self)
        guestOnSite = self.app.get(url=guestLink)
        #: try to update the profile
        profileNotUpdated = profile.editProfile(
            self,
            editParams2,
            editForm=editForm2,
            expectErrors=True
        )
        #: make sure the info is still the same
        authorization.logout(self)
        authorization.login(self, user)
        mainPage = self.app.get(pageDefs.allWorkshops())
        profilePage = profile.getProfilePage(self, mainPage)
        assert name3 in profilePage
        assert email3 in profilePage
        assert greeting2 in profilePage
        assert website2 in profilePage
        assert websiteDesc2 in profilePage
        authorization.logout(self)
        #: test as a different user
        newUser = registration.create_and_activate_a_user(self, postal='92007', name='New User')
        authorization.login(self, newUser)
        #: try to update the profile
        profileNotUpdated = profile.editProfile(
            self,
            editParams2,
            editForm=editForm2,
            expectErrors=True
        )
        #: make sure the info is still the same
        authorization.logout(self)
        authorization.login(self, user)
        mainPage = self.app.get(pageDefs.allWorkshops())
        profilePage = profile.getProfilePage(self, mainPage)
        assert name3 in profilePage
        assert email3 in profilePage
        assert greeting2 in profilePage
        assert website2 in profilePage
        assert websiteDesc2 in profilePage
        authorization.logout(self)

    def can_see_private_objects(self):
        """
        Create a set of objects in a private workshop. Go to the profile page, make sure they're 
        there. Then, comment on these objects and make sure the comments list and their links work.
        Do all this as the author, then make sure the admin can see these objects as well.
        Finally, make sure all other roles cannot see these objects listed on the user's profile.
        """
        #: create a person and a workshop
        user = registration.create_and_activate_a_user(self, postal='92007')
        facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        workshopTitle = 'workshop objects displayed'
        newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        guestLink = workshop.inviteGuest(self, newWorkshop, email=user['email'], guestLink=True)
        authorization.logout(self)
        authorization.login(self, user)
        joinedWorkshop = self.app.get(url=guestLink)
        #: make some objects
        rTitle = 'resource title'
        rText = 'r text'
        rType = 'resource'
        rAdded = nounAction.addNounToWorkshop(
            self, 
            rType, 
            newWorkshop, 
            title=rTitle,
            text=rText
        )
        assert rTitle in rAdded, "resource object not created"
        cTitle = 'conversation title'
        cText = 'c text'
        cType = 'conversation'
        cAdded = nounAction.addNounToWorkshop(
            self, 
            cType, 
            newWorkshop, 
            title=cTitle,
            text=cText
        )
        assert cTitle in cAdded, "conversation object not created"
        iTitle = 'idea title'
        iText = 'i text'
        iType = 'idea'
        iAdded = nounAction.addNounToWorkshop(
            self, 
            iType, 
            newWorkshop, 
            title=iTitle,
            text=iText
        )
        assert iTitle in iAdded, "idea object not created"
        #: this user has now created 1 of each main object type, let's confirm it is 
        #: listed on their own profile page
        profilePage = profile.getProfilePage(self, iAdded)
        resourcesList = profile.getResources(self, profilePage)
        conversationsList = profile.getConversations(self, profilePage)
        ideasList = profile.getIdeas(self, profilePage)
        assert rTitle in resourcesList
        assert cTitle in conversationsList
        assert iTitle in ideasList
        #: once the objects do list, make sure they link back to themselves

        #: NOTE need to comment on these objects now, and make sure the comments list and 
        # the links work

        #: make sure these objects display for the admin, the comments as well
        
        #: finally, make sure these don't show up for other roles types.

    def can_see_public_objects(self):
        """
         - [ Activity, Resources, Ideas, Conversations ]
        visitors that can see public workshop objects created by this user:
        - everyone (public, guest, nonmember, member, facilitator, admin)
        Create a set of objects in a private workshop. Go to the profile page, make sure they're 
        there. Then, comment on these objects and make sure the comments list and their links work.
        Do all this as the author, then make sure the admin can see these objects as well.
        Finally, make sure all other roles cannot see these objects listed on the user's profile.=
        """
        #: create a person and a workshop
        user = registration.create_and_activate_a_user(self, postal='92007')
        facilitator = registration.create_and_activate_a_user(self, postal='92007', name='Facilitator')
        workshopTitle = 'workshop objects displayed'
        newWorkshop = workshop.create_new_workshop(self, facilitator, title=workshopTitle)
        assert workshopTitle in newWorkshop, "not able to create workshop"
        #: make the workshop public
        #: upgrade to professional
        workshop.upgradeToProfessional(self, newWorkshop, facilitator)
        #: set the scope
        scopeDict = {}
        scopeDict = content.scopeDict(country='united-states', state='california')
        scopeString = workshop.createScope(self, country=scopeDict['country'], state=scopeDict['state'])
        workshop.setWorkshopScope(self, newWorkshop, facilitator, scopeString)
        workshop.startWorkshop(self, newWorkshop, facilitator)
        #: make sure it's public
        allWorkshops = self.app.get(pageDefs.allWorkshops())
        assert workshopTitle in allWorkshops, "public workshop not listed on all workshops page"
        #: add objects as a user of the workshop
        authorization.logout(self)
        authorization.login(self, user)
        atWorkshop = self.app.get(url=newWorkshop.request.url)
        #: make some objects
        rTitle = 'resource title'
        rText = 'r text'
        rType = 'resource'
        rAdded = nounAction.addNounToWorkshop(
            self, 
            rType, 
            atWorkshop, 
            title=rTitle,
            text=rText
        )
        assert rTitle in rAdded, "resource object not created"
        cTitle = 'conversation title'
        cText = 'c text'
        cType = 'conversation'
        cAdded = nounAction.addNounToWorkshop(
            self, 
            cType, 
            atWorkshop, 
            title=cTitle,
            text=cText
        )
        assert cTitle in cAdded, "conversation object not created"
        iTitle = 'idea title'
        iText = 'i text'
        iType = 'idea'
        iAdded = nounAction.addNounToWorkshop(
            self, 
            iType, 
            atWorkshop, 
            title=iTitle,
            text=iText
        )
        assert iTitle in iAdded, "idea object not created"
        #: this user has now created 1 of each main object type, let's confirm it is 
        #: listed on their own profile page
        profilePage = profile.getProfilePage(self, iAdded)
        resourcesList = profile.getResources(self, profilePage)
        conversationsList = profile.getConversations(self, profilePage)
        ideasList = profile.getIdeas(self, profilePage)
        assert ideasList == 404
        assert rTitle in resourcesList
        assert cTitle in conversationsList
        assert iTitle in ideasList
        #: once the objects do list, make sure they link back to themselves

        #: NOTE need to comment on these objects now, and make sure the comments list and 
        # the links work

        #: make sure these objects display for the admin, the comments as well
        
        #: finally, make sure these don't show up for other roles types.

    def runFollowingTests(self, followingPage, names = [], roles = []):
        """ make sure each of these names are on the following page
        also that this is visible to each of the roles provided """
        authorization.logout(self)
        for role in roles:
            authorization.login(self, role)
            for name in names:
                assert name in followingPage, "logged in as "+role['name']+", can't find "+name +" on the following page"
            authorization.logout(self)
        return True

    def test_following(self):
        """ Make sure that the people you are following are listed in the following list
        * activated users can be user, facilitator of public, facilitator of private and admin
        
        - [ Following ]
        visitors that can see who this person is following
        - everyone (public, guest, nonmember, member, facilitator, admin)
        """
        #: create the people we need for this and get a hold of their profile pages
        user1 = registration.create_and_activate_a_user(self, postal='92007', name='User One')
        profileUser1 = profile.loginGetProfilePageLogout(self, user1)
        #: second user
        user2 = registration.create_and_activate_a_user(self, postal='92007', name='User Two')
        profileUser2 = profile.loginGetProfilePageLogout(self, user2)
        #: this user is a facilitator of a public workshop
        facpub1 = registration.create_and_activate_a_user(self, postal='92007', name='FacilitatorPublic One')
        workshop1 = workshop.create_new_workshop(self, facpub1, title=facpub1['name'])
        pubWorkshop1 = workshop.setPublic(self, workshop1, facpub1)
        profileFacpub1 = profile.loginGetProfilePageLogout(self, facpub1, login=False)
        #: this user is a facilitator of a public workshop
        facpub2 = registration.create_and_activate_a_user(self, postal='92007', name='FacilitatorPublic Two')
        workshop2 = workshop.create_new_workshop(self, facpub2, title=facpub2['name'])
        pubWorkshop2 = workshop.setPublic(self, workshop2, facpub2)
        profileFacpub2 = profile.loginGetProfilePageLogout(self, facpub2, login=False)
        #: this user is a facilitator of a private workshop
        facpriv1 = registration.create_and_activate_a_user(self, postal='92007', name='FacilitatorPrivate One')
        privWorkshop1 = workshop.create_new_workshop(self, facpriv1, title=facpriv1['name'])
        profileFacpriv1 = profile.loginGetProfilePageLogout(self, facpriv1, login=False)
        #: this user is a facilitator of a private workshop
        facpriv2 = registration.create_and_activate_a_user(self, postal='92007', name='FacilitatorPrivate Two')
        privWorkshop2 = workshop.create_new_workshop(self, facpriv2, title=facpriv2['name'])
        profileFacpriv2 = profile.loginGetProfilePageLogout(self, facpriv2, login=False)
        #: this user is an admin
        admin1 = registration.create_and_activate_a_user(self, postal='92007', name='Admin One', accessLevel='200')
        profileAdmin1 = profile.loginGetProfilePageLogout(self, admin1)
        #: this user is a second admin
        admin2 = registration.create_and_activate_a_user(self, postal='92007', name='Admin Two', accessLevel='200')
        profileAdmin2 = profile.loginGetProfilePageLogout(self, admin2)

        #: create following scenarios
        #: first batch - can a user follow all these people?
        authorization.login(self, user1)
        followThese = [profileUser2, profileFacpub1, profileFacpriv1, profileAdmin1]
        profile.followThesePeople(self, followThese)
        #: now that this user has followed all these people, check they list on the following page
        userFollowing = profile.getFollowingPage(self, profileUser1)
        names = [user2['name'], facpub1['name'], facpriv1['name'], admin1['name']]
        #: every role should be able to see these followed users listed, so we only need
        #: to define this once
        roles = [user1, user2, facpub1, facpub2, facpriv1, facpriv2, admin1, admin2]
        weGood = TestProfileController.runFollowingTests(
            self,
            userFollowing,
            names,
            roles
        )
        authorization.logout(self)
        #: next batch - can a public workshop facilitator do this as well?
        authorization.login(self, facpub1)
        followThese = [profileUser2, profileFacpub2, profileFacpriv2, profileAdmin2]
        profile.followThesePeople(self, followThese)
        #: now that this user has followed all these people, check they list on the following page
        userFollowing = profile.getFollowingPage(self, profileFacpub1)
        """ every role should be able to see this """
        names = [user2['name'], facpub2['name'], facpriv2['name'], admin2['name']]
        weGood = TestProfileController.runFollowingTests(
            self,
            userFollowing,
            names,
            roles
        )
        authorization.logout(self)
        #: next batch - can a private workshop facilitator do this as well?
        authorization.login(self, facpriv1)
        followThese = [profileUser1, profileFacpub1, profileFacpriv2, profileAdmin1]
        profile.followThesePeople(self, followThese)
        #: now that this user has followed all these people, check they list on the following page
        userFollowing = profile.getFollowingPage(self, profileFacpriv1)
        """ every role should be able to see this """
        names = [user1['name'], facpub1['name'], facpriv2['name'], admin1['name']]
        weGood = TestProfileController.runFollowingTests(
            self,
            userFollowing,
            names,
            roles
        )
        authorization.logout(self)
        #: next batch - can an admin do this as well?
        authorization.login(self, admin1)
        followThese = [profileUser1, profileFacpub1, profileFacpriv1, profileAdmin2]
        profile.followThesePeople(self, followThese)
        #: now that this user has followed all these people, check they list on the following page
        userFollowing = profile.getFollowingPage(self, profileAdmin1)
        """ every role should be able to see this """
        names = [user1['name'], facpub1['name'], facpriv1['name'], admin2['name']]
        weGood = TestProfileController.runFollowingTests(
            self,
            userFollowing,
            names,
            roles
        )
        authorization.logout(self)
        """
        * user->user
        * user->facpub
        * user->facpriv
        * user->admin
        * facpub->user
        * facpub->facpub
        * facpub->facpriv
        * facpub->admin
        * facpriv->user
        * facpriv->facpub
        * facpriv->facpriv
        * facpriv->admin
        *admin->user
        *admin->facpub
        *admin->facpriv
        *admin->admin"""
        #: when to check on who's following who?

        # find the follow button and post to a url built from the button tag's data-url-list info
        # e.g. http://todd.civinomics.org/profile/4ICd/todd-anderson/follow/handler
        # e.g. profile_4ICg_andree-toddeoroas

        # find the button, break it into pieces:
        # 1 profile
        # 2 code
        # 3 username
        # add follow/handler

    def test_followed(self):
        """ If you are being followed, you should see who it is that is following you.
             - [ Followed ]
        visitors that can see who is following this person
        - everyone (public, guest, nonmember, member, facilitator, admin)
        
        create a person, create others: plain user, member of public workshop, member of private 
        workshop. follow these peeps, make sure they are listed in the user's following list

        """
       
    def test_bookmarks(self):
        """ - [ Bookmarks, My Workshops (own page) ]
        visitors that can see private workshops this person has bookmarked
        - self, admin 

        create a person

        then some workshops, private and public

        bookmark these workshops

        make sure as self, the whole list shows up on the profile page

        make sure other roles can only see the public ones - which covers:

         - [ Bookmarks ]
        visitors that can see public workshops this person has bookmarked
        - everyone (public, guest, nonmember, member, facilitator, admin) 

        """

    def test_my_workshops(self):
        """ - [ My Workshops ]
        visitors that can see private workshops this person is involved with (facilitator, listening, bookmarked?)
        - self, admin
        visitors that can see public workshops this person is involved with (facilitator, listening, bookmarked?)
        - everyone (public, guest, nonmember, member, facilitator, admin) 

        make some workshops, private and public

        make sure self and admin can see all of them

        make sure everyone else can only see the public ones

        """

    def test_email_settings(self):
        """ - [ email selections ]
        who can change the alert settings for a workshop?
        - self, admin 

        make some workshops

        check out the alerts on them, try out the different setting combos, making sure each 
        one works

        """

    def test_invites(self):
        """
        - [ invite selections ]
        who can send an invite?
        - self, admin ( if an admin sends, make sure the invite associates the guest )
        what invites are listed?
        - any workshops I facilitate, when on another's profile page there will be an invitation to co-facilitate and an invitation to listen to each of these workshops ( unless they have already been invited or set to listener )
        - if I am on my own page, I can invite myself to be a listener ( notable )



        """
