# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import *

#from webhelpers.date import *
#from webhelpers.text import *
#from webhelpers.html.converters import *
#from webhelpers.html.tools import *
#from webhelpers.util import *

from webhelpers.html import literal
from webhelpers.html import lit_sub
from webhelpers.html.tools import mail_to

from pylons import url

from routes import url_for

from pylowiki.lib.auth import * 

from webhelpers.pylonslib.flash import Flash as _Flash
flash = _Flash()

from pylowiki.lib.reST2HTML import reST2HTML

from urllib import quote, unquote
