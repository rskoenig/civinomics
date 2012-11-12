# -*- coding: utf-8 -*-

from pylons.controllers.util import redirect
from pylons import session, config, tmpl_context as c
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
        return redirect(h.url(controller = 'home', action = 'index'))
    if not c.authuser:
        session.delete()
        return redirect(h.url(controller = 'home', action = 'index'))

def check_access_level(userAsk, userSet, accessLevel):
    if int(userAsk['accessLevel']) < accessLevel or int(userAsk['accessLevel']) < int(userSet['accessLevel']):
        return False
    return True