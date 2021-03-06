# -*- coding: utf-8 -*-
"""Helper functions


Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html.tags import *
from webhelpers.html.builder import literal, lit_sub
from webhelpers.html.tools import mail_to

from pylons import url

from routes import url_for

from pylowiki.lib.auth import * 

from webhelpers.pylonslib.flash import Flash as _Flash
flash = _Flash()

from pylowiki.lib.reST2HTML import reST2HTML

from urllib import quote, unquote
