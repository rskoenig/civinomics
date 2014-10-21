# -*- coding: utf-8 -*-
import logging
import math

from pylons import request, response, session, config, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
from pylowiki.lib.utils import urlify

import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.geoInfo          as geoInfoLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.generic          as genericLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.dbHelpers        as dbHelpers
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.pmember          as pMemberLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.revision         as revisionLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.db.photo            as photoLib
import pylowiki.lib.db.mainImage        as mainImageLib
import pylowiki.lib.db.initiative       as initiativeLib
import pylowiki.lib.fuzzyTime           as fuzzyTime

from pylowiki.lib.facebook              import FacebookShareObject
import pylowiki.lib.images              as imageLib
import pylowiki.lib.utils               as utils

import time, datetime
import simplejson as json
import copy as copy
import misaka as m


log = logging.getLogger(__name__)

class CrmController(BaseController):
        
    def crmPrototype(self):
        return render("/derived/crm_prototype.bootstrap")
        
    def crmDashboard(self):
        return render("/derived/crm_dashboard.bootstrap")




