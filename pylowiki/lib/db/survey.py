from pylons import tmpl_context as c
from pylons import config

from pylowiki.model import Thing, meta
from pylowiki.lib.utils import urlify, toBase62
from pylowiki.lib.db.facilitator import Facilitator
from pylowiki.lib.db.geoInfo import GeoInfo
from pylowiki.lib.db.surveySlide import SurveySlide
from pylowiki.lib.images import smartCrop, makeSurveyThumbnail, cropHeader, cropHeight
from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl

import xml.etree.ElementTree as ET

import time, datetime, os, logging

log = logging.getLogger(__name__)

def getActiveSurveys( deleted = False):
     try:
        return meta.Session.query(Thing).filter_by(objType = 'survey').filter(Thing.data.any(wc('deleted', deleted))).filter(Thing.data.any(wc('active', 1))).all()
     except:
        return False
    
def getAllSurveys( deleted = False ):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'survey').filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False
    
def getSurveysByMember(owner, deleted = False):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'survey').filter_by(owner = owner.id).filter(Thing.data.any(wc('deleted', deleted))).all()
    except:
        return False
    
def getSurvey(urlCode, url):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'survey').filter(Thing.data.any(wc('urlCode', urlCode))).filter(Thing.data.any(wc('url', url))).one()
    except:
        return False
    
def getSurveyByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'survey').filter_by(id = id).one()
    except:
        return False
    
def Survey(owner, title, description, publicOrPrivate, estimatedTime):
    """
        Creates a survey Thing and sets up some basic properties.
        
        Inputs:         owner                ->    The user Thing that called this function
                        title                ->    The survey's title/name, a string
                        description          ->    A short description of the survey, a string
                        publicOrPrivate      ->    A string, either 'public' or 'private'
                        estimatedTime        ->    The estimated amount of time it will take to complete
                                                   the survey, in minutes.

        Outputs:        s                    ->    The survey Thing
    """
    s = Thing('survey', owner.id)
    s['publicOrPrivate'] = publicOrPrivate
    s['title'] = title
    s['description'] = description
    s['deleted'] = 0
    s['active'] = 0
    s['facilitators'] = 0
    s['estimatedTime'] = estimatedTime
    if len(title) > 20:
        s['url'] = urlify(title[:20])
    else:
        s['url'] = urlify(title)
    s['origFileName'] = 'flash'# The file name
    s['surveyType'] = 'normal'
    s['directoryNum'] = 0
    s['hash'] = 'flash'
    s['uploadVersion'] = 0 # A versioning key, keeps track of the number of times a starter file has been uploaded
    
    commit(s)
    s['urlCode'] = toBase62(s)
    commit(s)
    return s

def parseSurvey(file, survey):
    """
        file                 ->    The file that was uploaded.  This file should be
                                   a compressed file (.rar, .tar, .zip, .tar.gz, .gzip).
                                   The root of the compressed file contains the XML spec
                                   for the survey, and contains a single folder that
                                   contains all images used.

    """
    try:
        tree = ET.parse(file)
        if tree is None:
            return (False, 'No XML tree found')
        root = tree.getroot()
        if root is None:
            return (False, 'No XML root found')
        
        label = root.get('label')
        if label is None:
            return (False, 'No label attribute found in root of tree')
        survey['imgDir'] = label
        
        version = root.get('version')
        if version is None:
            return (False, 'No version attribute found in root of tree')
        survey['version'] = version
        
        date = root.get('date')
        if date is None:
            return (False, 'No date attribute found in root of tree')
        survey['date'] = date
        
        logo = root.get('logo')
        if logo is None:
            return (False, 'No logo attribute found in root of tree')
        survey['logo'] = logo

        
        # Here we assume the presence of 'lightColor' means 'darkColor' is here as well.  If not, the engine should be OK,
        # but the rendering will be wacky.
        lightColor = root.get('lightColor')
        darkColor = root.get('darkColor')
        if lightColor is not None:
            survey['lightColor'] = lightColor
            survey['darkColor'] = darkColor
        pages = root.getchildren()
        if len(pages) == 0:
            return (False, 'No pages found in XML file')
        foundThankYou = False
        
        # ids  and slideNum correspond to regular slides in the survey.
        # extraIDs and extraSlideNum correspond to slides after the 'thank you' page in the survey.
        ids = []
        slideNum = 0
        extraIDs = []
        extraSlideNum = 0
        groupName = ''
        i = 0
        for page in pages:
            log.info('i = %s' % slideNum)
            i += 1
            thankYou = page.find('thankYou')
            if thankYou is not None:
                # Keep the 'thankYou' slide as part of the main survey, not after
                slide = SurveySlide(page, c.authuser, survey, slideNum, foundThankYou)
                foundThankYou = True
            else:
                slide = SurveySlide(page, c.authuser, survey, slideNum, foundThankYou)
            if slide:
                if not foundThankYou:
                    slideNum += 1
                    ids.append(slide.id)
                else:
                    if thankYou is not None:
                        slideNum += 1
                        ids.append(slide.id)
                    else:
                        extraSlideNum += 1
                        extraIDs.append(slide.id)
                    if groupName == '' and page.get('groupName') is not None:
                        groupName = page.get('groupName')
                
                # Thumbnail generation
                if slide['image'] != '':
                    try:
                        directory = os.path.join(config['app_conf']['surveyDirectory'], survey['surveyType'], survey['directoryNum'], survey['hash'], survey['imgDir'])
                        filename = slide['image']
                        postfix = 'thumbnail'
                        header = False
                        if not foundThankYou:
                            # Main survey slides at the top
                            x = 60
                            y = 45
                        else:
                            # FAQ slides along the side
                            x = 220
                            y = 165
                        makeSurveyThumbnail(filename, directory, x, y, postfix)
                        
                        # Crop the image if necessary
                        imageBased = root.get('imageBased')
                        if imageBased is not None:
                            if slide['type'] == 'checkbox' or slide['type'] == 'slider' or slide['type'] == 'feedback':
                                smartCrop(directory, filename)
                        if 'header' in slide.keys():
                            header = True
                            cropAmount = 55 # number of pixels to chop
                            cropHeader(directory, filename, cropAmount)
                        if 'height' in slide.keys():
                            cropAmount = int(slide['height'])
                            cropHeight(directory, filename, cropAmount, header)
                    except:
                        return (False, 'Failed on image processing')
            
        if len(ids) == 0:
            return (False, 'No slides found')            
        survey['slides'] = ','.join(map(str, ids))
        if len(extraIDs) > 0:
            survey['extraSlides'] = ','.join(map(str, extraIDs))
        if groupName == '':
            survey['extraSlidesName'] = 'FAQ'
        else:
            survey['extraSlidesName'] = groupName
        commit(survey)
        return (survey, 'Success')
    except:
        return (False, 'Generic error message')