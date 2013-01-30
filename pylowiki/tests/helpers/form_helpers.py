# -*- coding: utf-8 -*-
from pylowiki.tests import *

def loadWithSubmitFields(webtestForm):
    params = {}
    for key, value in webtestForm.submit_fields():
        params[key] = value
    return params