from pylowiki.tests import *
from webtest import TestResponse
from routes import url_for

import pylowiki.tests.helpers.content as content
import pylowiki.tests.helpers.form_definitions as formDefs
import pylowiki.tests.helpers.form_helpers as formHelpers
import pylowiki.tests.helpers.link_definitions as linkDefs
import pylowiki.tests.helpers.noun_verb_tests as nounVerbTest
import pylowiki.tests.helpers.workshops as  workshop
from pylowiki.tests.helpers.authorization import login, logout
from pylowiki.tests.helpers.registration import create_and_activate_a_user

import logging
log = logging.getLogger(__name__)

class TestResourceController(TestController):
    """ This class tests that resources work correctly. A workshop's resources are created
    similar to how resources and conversations are created. """


    """ ****************************************************************************************** """
    """ ****************************************************************************************** """
    """ This group of tests focuses on permissions for disabling and enabling. In the tests
    where there should be a successful disabling of the resource, the cases for enabling will
    be tested as well. """
    
    def test_disable_resource_admin_admin(self):
        """ Create a resource as an admin, then disable this resource as an admin. 
        In order to test a more realistic situation, these admins will be different users. """
        nounVerbTest.test_disable_noun_admin_admin(self, 'resource')

    def test_disable_resource_facilitator_admin(self):
        """ Create a resource as a facilitator, then disable this resource as an admin. """
        nounVerbTest.test_disable_noun_facilitator_admin(self, 'resource')

    def test_disable_resource_user_admin(self):
        """ Create a resource as a user of the workshop, then disable this resource as an admin. """
        nounVerbTest.test_disable_noun_user_admin(self, 'resource')

    def test_disable_resource_admin_facilitator(self):
        """ Create a resource as an admin, then try to disable it as a facilitator. """
        nounVerbTest.test_disable_noun_admin_facilitator(self, 'resource')

    def test_disable_resource_facilitator_facilitator(self):
        """ Create a resource as a facilitator, then disable it as a facilitator. """
        nounVerbTest.test_disable_noun_facilitator_facilitator(self, 'resource')
        
    def test_disable_resource_user_facilitator(self):
        """ Create a resource as a user of the workshop, then disable this resource as its facilitator. """
        nounVerbTest.test_disable_noun_user_facilitator(self, 'resource')
        
    def test_disable_resource_admin_user(self):
        """ Create a resource as an admin, then disable this resource as a user of the workshop. """
        nounVerbTest.test_disable_noun_admin_user(self, 'resource')

    def test_disable_resource_facilitator_user(self):
        """ Create a resource as a facilitator, then disable this resource as a user of the workshop. """
        nounVerbTest.test_disable_noun_facilitator_user(self, 'resource')

    def test_disable_resource_user_user(self):
        """ Create a resource as a user, then disable this resource as a user of the workshop. """
        nounVerbTest.test_disable_noun_user_user(self, 'resource')

    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ TEST IMMUNITY - PRIVATE WORKSHOPS """
    """ In this next group, we will be looking for holes in the ability to immunify an object.
    There are many possible combinations of situations, but only a few of them should be successful. Therefore, 
    in order to reduce the number of tests here, the attempts to immunify that should
    not be successful will be attempted before testing what should be a successful setting of an object's immunity. """

    def test_immunify_privateWorkshop_user_facilitator(self):
        """ Create a resource in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 1/12 for this group
        nounVerbTest.test_immunify_private_noun_user_facilitator(self, 'resource')
        
    def test_immunify_privateWorkshop_facilitator_facilitator(self):
        """ Create a resource in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 2/12 for this group
        nounVerbTest.test_immunify_private_noun_facilitator_facilitator(self, 'resource')
        
    def test_immunify_privateWorkshop_admin_facilitator(self):
        """ Create a resource in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 3/12 for this group
        nounVerbTest.test_immunify_private_noun_admin_facilitator(self, 'resource')

    def test_immunify_privateWorkshop_user_admin(self):
        """ Create a resource in a private workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 4/12 for this group
        nounVerbTest.test_immunify_noun_user_admin(self, 'resource')

    def test_immunify_privateWorkshop_facilitator_admin(self):
        """ Create a resource in a private workshop as its facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 5/12 for this group
        nounVerbTest.test_immunify_private_noun_facilitator_admin(self, 'resource')

    def test_immunify_privateWorkshop_admin_admin(self):
        """ Create a resource in a private workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 6/12 for this group
        nounVerbTest.test_immunify_private_noun_admin_admin(self, 'resource')

    """ ****************************************************************************************** """
    """ This next group of tests are the same as the previous ones that started at 
    'TEST IMMUNITY - PRIVATE WORKSHOPS', except for the fact that these are working 
    with public workshops. """


    def test_immunify_publicWorkshop_user_facilitator(self):
        """ Create a resource in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 7/12 for this group
        nounVerbTest.test_immunify_public_noun_user_facilitator(self, 'resource')

    def test_immunify_publicWorkshop_facilitator_facilitator(self):
        """ Create a resource in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 8/12 for this group
        nounVerbTest.test_immunify_public_noun_facilitator_facilitator(self, 'resource')
        
    def test_immunify_publicWorkshop_admin_facilitator(self):
        """ Create a resource in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as the workshop's facilitator.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 9/12 for this group
        nounVerbTest.test_immunify_public_noun_admin_facilitator(self, 'resource')

    def test_immunify_publicWorkshop_user_admin(self):
        """ Create a resource in a public workshop as a user, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 10/12 for this group
        nounVerbTest.test_immunify_public_noun_user_admin(self, 'resource')

    def test_immunify_publicWorkshop_facilitator_admin(self):
        """ Create a resource in a public workshop as the facilitator, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 11/12 for this group
        nounVerbTest.test_immunify_public_noun_facilitator_admin(self, 'resource')

    def test_immunify_publicWorkshop_admin_admin(self):
        """ Create a resource in a public workshop as an admin, try to immunify and confirm it hasn't
        happened with each role that shouldn't be able to, then immunify the object as an admin.
        At this point, confirm that it is immune by attempting to flag the object as each of the roles that shouldn't
        be able to, confirming after each attempt this is true. Finally, flag the object as an admin and assert this
        has been successful. """
        # test 12/12 for this group
        nounVerbTest.test_immunify_public_noun_admin_admin(self, 'resource')

    """ ****************************************************************************************** """ 
    """ ****************************************************************************************** """ 
    """ This next group of tests will cover deletion permissions. Bottom line is, only an admin 
        can delete an object. """

    def test_delete_resource_admin_admin(self):
        """ Create a resource as an admin, then delete this resource as an admin."""
        # test 1
        nounVerbTest.test_delete_noun_admin_admin(self, 'resource')
        
    def test_delete_resource_facilitator_admin(self):
        """ Create a resource as a facilitator, then delete this resource as an admin."""
        # test 2
        nounVerbTest.test_delete_noun_facilitator_admin(self, 'resource')
        
    def test_delete_resource_user_admin(self):
        """ Create a resource as a user of the private workshop, then delete this resource 
        as an admin."""
        # test 3
        nounVerbTest.test_delete_noun_user_admin(self, 'resource')

    """ ****************************************************************************************** """ 
    """ Second set will deal with this within public workshops. """

    def test_delete_public_resource_admin_admin(self):
        """ Create a resource as an admin in a public workshop, then delete this resource 
        as an admin."""
        # test 4
        nounVerbTest.test_delete_public_noun_admin_admin(self, 'resource')
    
    def test_delete_public_resource_facilitator_admin(self):
        """ Create a resource as a facilitator in a public workshop, then delete this resource 
        as an admin."""
        # test 5
        nounVerbTest.test_delete_public_noun_facilitator_admin(self, 'resource')
        
    def test_delete_public_resource_user_admin(self):
        """ Create a resource as a user in a public workshop, then delete this resource 
        as an admin."""
        # test 6
        nounVerbTest.test_delete_public_noun_user_admin(self, 'resource')
        
