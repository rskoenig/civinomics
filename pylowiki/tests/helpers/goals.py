# -*- coding: utf-8 -*-
from pylowiki.tests import *
    
import pylowiki.tests.helpers.workshops as workshop

def addGoal(self, thisWorkshop, goal):
    """adds a goal to a workshop
    - add goal -
        Status: 200, POST
        {baseUrl}/workshop/{workshopCode}/{workshopName}/goals/add
        Content-Type[application/json;charset=utf-8]
        Post Data: {"title":"1 goal","done":false}[]"""
    workshopCode = workshop.getWorkshopCode(self, thisWorkshop)
    workshopName = workshop.getWorkshopLinkName(self, thisWorkshop)
    params = {}
    params['title'] = goal
    params['done'] = False
    addedGoal = self.app.post_json(
        '/workshop/' + workshopCode + '/' + workshopName + '/goals/add',
        params=params
    )
    
    if addedGoal.status_int == 200:
        return True
    else:
        return False

    """post_json(url, params=<class 'webtest.app.NoDefault'>, headers=None, extra_environ=None, 
        status=None, expect_errors=False)
        Do a POST request. Very like the .get() method. params are dumps to json and put in the 
        body of the request. Content-Type is set to application/json.
        Returns a webob.Response object. """

    """workshopCreated = self.app.post(
        url=workshopStartUrl, 
        content_type='multipart/form-data',
        params={'name' : 'startWorkshop'}
    ).follow() """

def getGoals(self, thisWorkshop, **kwargs):
    """ retrieves the goals of a workshop 
    {baseUrl}/workshop/{workshopCode}/{workshopName}/goals/get
    """
    workshopCode = workshop.getWorkshopCode(self, thisWorkshop)
    workshopName = workshop.getWorkshopLinkName(self, thisWorkshop)
    # from routing /{workshop:workshops?}/{workshopCode}/{workshopURL}/goals/get{end:/?}', controller = 'goals', action = 'getGoals')
    if 'expect_errors' in kwargs:
        if kwargs['expect_errors'] == True:
            expectErrors = True
        else:
            expectErrors = False
    else:
        expectErrors = False
    goals = self.app.get(
        '/workshop/' + workshopCode + '/' + workshopName + '/goals/get/',
        expect_errors = expectErrors
    )
    return goals




