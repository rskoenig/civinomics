# -*- coding: utf-8 -*-
from pylowiki.tests import *

from pylowiki.lib.db.user import User

##################
# design idea - for guaranteed unique generated emails:
#   - use the activation hash
#       - it should be able to make a unique email
#   - supply the name as the calling test class name plus an index associated 
#   with this class that is stored for the duration of the test.
#       - how? in paste.testing_variables?
#           - I believe this is a 'global' dictionary that is available to all tests
##################

def generateHash(*length):
    """Return a system generated hash for randomization of user params"""
    from string import letters, digits
    from random import choice
    pool, size = letters + digits, length or 10
    hash =  ''.join([choice(pool) for i in range(size)])
    return hash.lower()

def give_me_user(**kwargs):
    if 'email' in kwargs:
        email = kwargs['email']
    else:
        email = '%s@civinomics.com'%(generateHash())
    if 'password' in kwargs:
        password = kwargs['password']
    else:
        password = 'password'
    if 'country' in kwargs:
        country = kwargs['country']
    else:
        country = 'United States'
    if 'zip' in kwargs:
        zip = kwargs['zip']
    else:
        zip = 'zip'
    if 'name' in kwargs:
        name = kwargs['name']
    else:
        name = 'name name'
    if 'memberType' in kwargs:
        memberType = kwargs['memberType']
    else:
        memberType = 'individual'
    if 'authName' in kwargs:
        authValDict = {
            'user' : '0',
            'facilitator' : '100',
            'admin' : '200'
        }
        if authName in authValDict:
            authLevel = authValDict[authName]
        else:
            authLevel = authValDict['user']
    if 'authLevel' in kwargs:
        # do I expect user/facilitator/admin or 100/200/300?
        # if I accept name, then I cannot accept #?
        # if I accept both, must one trump the other? we only use the #, so # should trump name.
        authLevel = kwargs['authLevel']
    else:
        authLevel = '0'
    new_user = {
        'email' : email,
        'password' : password,
        'country' : country,
        'zip' : 95060,
        'name' : name,
        'memberType' : memberType,
        'authLevel' : authLevel
    }
    return new_user

def createActivatedUser(**kwargs):
    newUser = give_me_user(**kwargs)
    u = User(newUser['email'], newUser['name'], newUser['password'], newUser['country'], newUser['memberType'], newUser['zip'])
    u['activated'] = '1'
    return newUser

##################
# make_user
#   Creates an object containing all of the parameters required for creating a user on the site.
##################
def make_user(**kwargs):
    return give_me_user(**kwargs)


# test.ini admin
# NOTE - fill these fields with those found in test.ini where applicable. for those that are not?
def get_test_admin():
    test_admin = {
        'email' : 'username@civinomics.com',
        'password' : 'password',
        'zip' : '95060',
        'first' : 'test',
        'last' : 'admin',
        'type' : 'individual',
        'access' : 'admin'
    }
    return test_admin