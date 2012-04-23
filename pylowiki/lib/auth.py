# -*- coding: utf-8 -*-
from pylons.controllers.util import redirect
from pylons import session, config
from decorator import decorator #easy_install decorator   http://pypi.python.org/pypi/decorator
import helpers as h

#from pylowiki.model import get_user, getUserAccessLevel
#from pylowiki.lib.db.user import get_user

def _login_required(func, *args, **kw):
    check_if_login_required()
    return func(*args, **kw)

def login_required(func):
    func.cache = {}
    return decorator(_login_required, func)

def check_if_login_required():
    if 'user' not in session:
        h.flash( "Oops, you must be logged in to use that.", "warning" )
        #return redirect( h.url(controller='login', action="index") )
        return redirect(h.url(controller = 'home', action = 'index'))

# Deprecated
"""
def accessLevel(level):
    user = get_user(session["user"])
    thisLevel = getUserAccessLevel(user.id)
    if thisLevel >= level:
        return True
    #h.flash("You need the proper authorization to access that page", "warning")
    #return redirect(h.url(controller = 'home', action = 'index'))
    return False

"""