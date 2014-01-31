import os, logging, re

from pylons import session, config, request, tmpl_context as c

import pylowiki.lib.utils       as utils

log = logging.getLogger(__name__)


"""
    General workflow for facebook library:

"""

class FacebookShareObject(object):

    def __init__(self, itemType=None, url=None, thingCode=None, image=None, title="", description=None, caption="", shareOk=None):
    
        self.facebookAppId = config['facebook.appid']
        self.channelUrl = config['facebook.channelUrl']
        self.baseUrl = utils.getBaseUrl()
    
        if itemType is None:
            self.itemType = ""
        else:
            self.itemType = itemType

        # ${( "%s%s"%(c.baseUrl, lib_6.workshopLink(c.w, embed=True, raw=True)),
        if url is None:
            self.url = self.baseUrl
        else:
            self.url = self.baseUrl + url

        if thingCode is None:
            self.thingCode = 'noCode'
        else:
            self.thingCode = thingCode

        if image is None:
            self.image = self.baseUrl + '/images/slide/slideshow/supDawg.slideshow'
        else:
            self.image = self.baseUrl + image

        self.title = title
        
        if description is None:
            self.description = "Civinomics is an Open Intelligence platform. Collaborate to create solutions."
        else:
            self.description = description

        self.caption = caption

        if shareOk is None:
            self.shareOk = False
        else:    
            self.shareOk = shareOk

    def updateUrl(self, newUrl):
        self.url = self.baseUrl + newUrl


