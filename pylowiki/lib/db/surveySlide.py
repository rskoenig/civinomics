from pylons import tmpl_context as c
from pylowiki.model import Thing, meta
from pylowiki.lib.utils import toBase62
from dbHelpers import commit, with_characteristic as wc
from pylowiki.lib.utils import toBase62
from hashlib import md5
#import xml.etree.ElementTree as ET

import logging, time

log = logging.getLogger(__name__)

def getSurveySlide(hash, parent):
    """
        Uses the slide's hash as seen in the URL
    """
    try:
        return meta.Session.query(Thing).filter_by(objType = 'surveySlide').filter(Thing.data.any(wc('hash', hash))).filter(Thing.data.any(wc('parent', parent))).one()
    except:
        return False

def getSurveySlideByID(id):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'surveySlide').filter_by(id = id).one()
    except:
        return False

def getSurveySlideByName(name, survey):
    """
        Uses the content inside the 'name' tag from an XML file.
    """
    try:
        return meta.Session.query(Thing).filter_by(objType = 'surveySlide').filter(Thing.data.any(wc('name', name))).filter(Thing.data.any(wc('parent', survey.id))).filter(Thing.data.any(wc('uploadVersion', survey['uploadVersion']))).one()
    except:
        return False

def SurveySlide(slide, owner, survey, slideNum, foundThankYou):
    """
        Inputs:         slide            ->    An ElementTree object corresponding to a slide in the XML tree
                        owner            ->    The user Thing owning this slide
                        survey           ->    The survey Thing to which we are attaching this slide
                        slideNum         ->    The current slide number
                        foundThankYou    ->    A boolean, used to determine if the slide is within the survey or an extra slide after the end
                        
    """
    slideType = slide.find('type').text
    ignore = slide.find('ignore')
    if ignore is not None:
        return False
    if slideType == 'splash':
        return setupSplash(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'info':
        return setupInfo(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'checkbox':
        return setupCheckbox(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'slider':
        return setupSlider(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'multi-slider':
        return setupMultiSlider(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'feedback':
        return setupFeedback(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'itemRanking':
		return setupItemRanking(slide, owner, survey, slideNum, foundThankYou)
    elif slideType == 'save survey':
        # Do nothing
        return False
    else:
        return False
    
def basicSetup(slide, owner, survey, slideNum, foundThankYou):
    s = Thing('surveySlide', c.authuser.id)
    s['slideNum'] = slideNum
    s['uploadVersion'] = survey['uploadVersion']
    image = slide.find('image')
    if image is not None:
        s['image'] = image.text
        height = image.get('height')
        if height is not None:
            s['height'] = height
        ignore = image.get('ignore')
        if ignore is not None:
            if ignore == 'true':
                s['ignore'] = 1
    else:
        s['image'] = ''
        
    title = slide.find('title')
    if title is not None:
        s['title'] = title.text
    
    caption = slide.find('caption')
    if caption is not None:
        s['caption'] = caption.text
    
    header = slide.find('header')
    if header is not None:
        s['header'] = header.find('description').text
    
    noHeaderLogo = slide.find('noHeaderLogo')
    if noHeaderLogo is not None:
        s['noHeaderLogo'] = 1
        
    s['name'] = slide.find('name').text
    s['parent'] = survey.id
    vocal = slide.find('vocal')
    if vocal is not None:
        s['vocal'] = vocal.text
    else:
        s['vocal'] = ''
    if foundThankYou:
        s['surveySection'] = 'after'
    else:
        s['surveySection'] = 'before'
    commit(s)
    s['hash'] = toBase62(s)
    return s
    
def setupSplash(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'splash'
    commit(s)
    return s

def setupInfo(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'info'
        
    lookForhAnswerBox = slide.find('hAnswerBox')
    if lookForhAnswerBox is not None:
        hAnswerBoxes = [element for element in slide.getchildren() if element.tag == 'hAnswerBox']
        s['numhAnswerBoxes'] = len(hAnswerBoxes)
        hAnswerBoxNum = 1
        for hAnswerBox in hAnswerBoxes:
            s['hAnswerBox_coords_%s'%hAnswerBoxNum] = hAnswerBox.find('coords').text
            s['hAnswerBox_label_%s'%hAnswerBoxNum] = hAnswerBox.find('label').text
            s['hAnswerBox_alignment_%s'%hAnswerBoxNum] = hAnswerBox.find('alignment').text
            s['hAnswerBox_textSize_%s'%hAnswerBoxNum] = hAnswerBox.find('textSize').text
            hAnswerBoxNum += 1
    else:
        s['numhAnswerBoxes'] = 0

    
    hCheckboxType = slide.find('hCheckboxType')
    if hCheckboxType is not None:
        s['hCheckboxType'] = hCheckboxType.text
        hCheckboxes = [element for element in slide.getchildren() if element.tag == 'hCheckbox']
        s['numhCheckboxes'] = len(hCheckboxes)
        hCheckboxNum = 1
        for box in hCheckboxes:
            s['hCheckbox_coords_%s'%hCheckboxNum] = box.find('coords').text
            # NOTE - custom checkbox graphics are used for these element types:
            # <buttonDefault>, <buttonPressed>, <buttonSelected>
            s['hCheckbox_label_%s'%hCheckboxNum] = box.find('label').text
            hCheckboxLink = box.find('link')
            if hCheckboxLink is not None:
                s['hCheckbox_link_%s'%hCheckboxNum] = hCheckboxLink.text
            else:
                s['hCheckbox_link_%s'%hCheckboxNum] = ''
            hCheckboxNum += 1
    else:
        s['numhCheckboxes'] = 0
        
    hLink = slide.find('hLink')
    if hLink is not None:
        hLinks = [element for element in slide.getchildren() if element.tag == 'hLink']
        s['numhLinks'] = len(hLinks)
        hLinkNum = 1
        for link in hLinks:
            s['hLink_coords_%s'%hLinkNum] = link.find('coords').text
            s['hLink_link_%s'%hLinkNum] = link.find('link').text
            hLinkImage = link.find('image')
            if hLinkImage is not None:
                s['hLink_image_%s'%hLinkNum] = hLinkImage.text
                s['hLink_hash_%s'%hLinkNum] = s['hash'] # Should not work
            else:
                s['hLink_image_%s'%hLinkNum] = ''
            hLinkNum += 1
    else:
        s['numhLinks'] = 0

    
    commit(s)
    return s

def setupItemRanking(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'itemRanking'
    s['rankItemTitleText'] = slide.find('rankItemTitleText').text
    s['rankItemHeader'] = slide.find('rankItemHeader').text
    
    lookForRankItem = slide.find('rankItem')
    if lookForRankItem is not None:
        rankItems = [element for element in slide.getchildren() if element.tag == 'rankItem']
        s['numRankItems'] = len(rankItems)
        rankItemNum = 1
        for rankItem in rankItems:
            s['rankItem_title_%s'%rankItemNum] = rankItem.find('title').text
            s['rankItem_label_%s'%rankItemNum] = rankItem.find('label').text
            rankItemNum += 1
    else:
        s['numRankItems'] = 0
        
    commit(s)
    return s


def setupMultiSlider(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'multi-slider'
    s['sliderTitleText'] = slide.find('sliderTitleText').text
    s['leftSliderText'] = slide.find('leftSliderText').text
    s['middleSliderText'] = slide.find('middleSliderText').text
    s['rightSliderText'] = slide.find('rightSliderText').text
    
    lookForSlider = slide.find('slider')
    if lookForSlider is not None:
        sliders = [element for element in slide.getchildren() if element.tag == 'slider']
        s['numSliders'] = len(sliders)
        sliderNum = 1
        for slider in sliders:
            s['slider_title_%s'%sliderNum] = slider.find('title').text
            s['slider_label_%s'%sliderNum] = slider.find('label').text
            sliderNum += 1
    else:
        s['numSliders'] = 0
        
    commit(s)
    return s

def setupSlider(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'slider'
    s['leftSliderText'] = slide.find('leftSliderText').text
    s['middleSliderText'] = slide.find('middleSliderText').text
    s['rightSliderText'] = slide.find('rightSliderText').text
    
    commit(s)
    return s

def setupCheckbox(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'checkbox'
    s['checkboxType'] = slide.find('checkboxType').text
    s['checkboxSize'] = slide.find('checkboxSize').text
    checkboxes = [element for element in slide.getchildren() if element.tag == 'checkbox']
    s['numCheckboxes'] = len(checkboxes)
    checkboxNum = 1
    for box in checkboxes:
        s['checkbox_description_%s'%checkboxNum] = box.find('description').text
        s['checkbox_label_%s'%checkboxNum] = box.find('label').text
        checkboxNum += 1
    commit(s)
    return s

def setupFeedback(slide, owner, survey, slideNum, foundThankYou):
    s = basicSetup(slide, owner, survey, slideNum, foundThankYou)
    
    s['type'] = 'feedback'
    commit(s)
    return s