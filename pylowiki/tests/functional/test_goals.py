from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

from nose.plugins.skip import Skip, SkipTest

import pylowiki.tests.helpers.authorization as authorization
import pylowiki.tests.helpers.goals as goals
import pylowiki.tests.helpers.registration as registration
import pylowiki.tests.helpers.workshops as workshop

class TestGoalsController(TestController):
    """ This class tests that goals work correctly. A workshop's goals are created using json messages.
    The interface is managed by angular. """

    """ test to see if I can get the goals for a workshop. The criteria being that if a workshop
     is public, anyone should be able to get the goals. If a workshop is private, only an admin, the 
     facilitator, or a member of the workshop should be able to get the goals. """

    def test_get_public_goals_public(self):
        """ Test that a public workshop's goals can be retrieved when a public user visits. """
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: set the workshop to public
        workshop.setPublic(self, newWorkshop, newUser)
        #: logout, see if I can grab the goals
        authorization.logout(self)
        gotGoals = goals.getGoals(self, newWorkshop)
        
        assert firstGoal in gotGoals, "public not able to get goals of pubic workshop"
        assert secondGoal in gotGoals, "public not able to get all goals of pubic workshop"

    def test_get_public_goals_user(self):
        """ Test that a public workshop's goals can be retrieved when a public user visits. """
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: set the workshop to public
        workshop.setPublic(self, newWorkshop, newUser)
        #: logout, see if I can grab the goals as a site member 
        #: who is not part of this public workshop
        authorization.logout(self)
        notMember = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        authorization.login(self, notMember)
        gotGoals = goals.getGoals(self, newWorkshop)
        #assert gotGoals.status_int == 404
        assert firstGoal in gotGoals, "public not able to get goals of pubic workshop"
        assert secondGoal in gotGoals, "public not able to get all goals of pubic workshop"

    def test_get_private_goals_admin(self):
        """ Test that a private workshop's goals are retrievable by an admin. """
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: logout, create an admin, login as the admin and get the workshop's goals
        authorization.logout(self)
        adminUser = registration.create_and_activate_a_user(self, postal='95060', name='Admin User', accessLevel='200')
        authorization.login(self, adminUser)
        #: retrieve the workshop's goals
        gotGoals = goals.getGoals(self, newWorkshop)
        assert firstGoal in gotGoals, "admin not able to get goals of private workshop"
        assert secondGoal in gotGoals, "public not able to get all goals of pubic workshop"

    def test_get_private_goals_facilitator(self):
        """ Test that a private workshop's goals are retrievable by a facilitator. """
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='Facilitator')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: retrieve the workshop's goals
        gotGoals = goals.getGoals(self, newWorkshop)
        assert firstGoal in gotGoals, "public not able to get goals of pubic workshop"
        assert secondGoal in gotGoals, "public not able to get all goals of pubic workshop"

    def test_get_private_goals_member(self):
        """ Test that a private workshop's goals are retrievable by a member of the workshop. """
        # * use this function:
        # guestLink = workshop.inviteGuest(self, newWorkshop, guestLink=True)
        # customize if needed to invite by email, use email of newMemebr here
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='Facilitator')
        newMember = registration.create_and_activate_a_user(self, postal='95864', name='Member')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: retrieve the workshop's goals
        gotGoals = goals.getGoals(self, newWorkshop)
        assert firstGoal in gotGoals, "public not able to get goals of pubic workshop"
        assert secondGoal in gotGoals, "public not able to get all goals of pubic workshop"

    def test_get_private_goals_user(self):
        """ Test that a private workshop's goals are NOT retrievable by a site user who is not
        a member of the workshop. """
        #: NOTE this test is functioning prop
        #: create a user, goal and workshop
        newUser = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        firstGoal = 'Have many goals.'
        secondGoal = 'Dont repeat goals.'
        workshopTitle = 'public workshop for testing goals'
        newWorkshop = workshop.create_new_workshop(self, newUser, title=workshopTitle)
        assert workshopTitle in newWorkshop, "user not able to create workshop"
        #: add a goal via json
        workshopGoalAdded = goals.addGoal(self, newWorkshop, firstGoal)
        assert workshopGoalAdded == True, "something went wrong with adding the goal"
        anotherWorkshopGoalAdded = goals.addGoal(self, newWorkshop, secondGoal)
        assert anotherWorkshopGoalAdded == True, "something went wrong with adding the 2nd goal"
        #: logout, see if I can grab the goals as a site member 
        #: who is not part of this private workshop
        authorization.logout(self)
        notMember = registration.create_and_activate_a_user(self, postal='95864', name='New User')
        authorization.login(self, notMember)
        gotGoals = goals.getGoals(self, newWorkshop, expect_errors=True)

        assert firstGoal not in gotGoals, "site member not part of private workshop able to get goals of the workshop"
        assert secondGoal not in gotGoals, "site member not part of private workshop able to get some goals of the workshop"

    """ more tests to write if needed """

    def test_edit_goal_admin(self):
        """Status: 200, POST
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICM/update
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICM","done":false,"title":"1 edited goal","editing":true}[]"""

    def test_delete_goal_admin(self):
        """Status: 200[OK], POST
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICs/delete
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICs","done":false,"title":"FOR GOALS INQUIRE WITHIN","editing":false}[]"""

    def test_complete_goal_admin(self):
        """Status: 200[OK], POST 
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICM/update
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICM","done":true,"title":"1 edited goal","editing":false}[]"""

    def test_add_goal_facilitator(self):
        """added goal
        Status: 200, POST
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/add
        Content-Type[application/json;charset=utf-8]
        Post Data: {"title":"1 goal","done":false}[]"""

    def test_edit_goal_facilitator(self):
        """Status: 200, POST
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICM/update
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICM","done":false,"title":"1 edited goal","editing":true}[]"""

    def test_delete_goal_facilitator(self):
        """Status: 200[OK], POST
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICs/delete
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICs","done":false,"title":"FOR GOALS INQUIRE WITHIN","editing":false}[]"""

    def test_complete_goal_facilitator(self):
        """Status: 200[OK], POST 
        http://todd.civinomics.org/workshop/4ICj/my-private-workshop/goals/4ICM/update
        Content-Type[application/json;charset=utf-8]
        Post Data: {"code":"4ICM","done":true,"title":"1 edited goal","editing":false}[]"""

    """ The tests after this point should fail do to insufficient permission levels. """