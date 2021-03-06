#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc, with_characteristic_like as wcl
import generic

log = logging.getLogger(__name__)

def getWorkshopTags(workshop, disabled = '0'):
    return meta.Session.query(Thing)\
            .filter_by(objType = 'tag')\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .all()

def searchTags(searchString, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
        .filter_by(objType = 'tag')\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wcl('title', searchString)))\
        .all()
    except:
        return False
        
def countTags(searchString, disabled = '0'):
    try:
        return meta.Session.query(Thing)\
        .filter_by(objType = 'tag')\
        .filter(Thing.data.any(wc('disabled', disabled)))\
        .filter(Thing.data.any(wcl('title', searchString)))\
        .count()
    except:
        return False

def getTagCategories():
    tags = []
    tags.append('Arts')
    tags.append('Business')
    tags.append('Civil Rights')
    tags.append('Community')
    tags.append('Economy')
    tags.append('Education')
    tags.append('Employment')
    tags.append('Energy')
    tags.append('Environment')
    tags.append('Family')
    tags.append('Government')
    tags.append('Health')
    tags.append('Housing')
    tags.append('Infrastructure')
    tags.append('Justice')
    tags.append('Land Use')
    tags.append('Municipal Services')
    tags.append('Parks and Rec')
    tags.append('Safety')
    tags.append('Sports')
    tags.append('Transportation')
    tags.append('Water')
    tags.append('Other')
    return tags

def getTagColouring():
    mapping = { 'Civil Rights':         'red-tag',
                'Health' :              'red-tag',
                'Safety' :              'red-tag',
                'Justice':              'red-tag',
                'Land Use':             'green-tag',
                'Parks and Rec':        'green-tag',
                'Environment':          'green-tag',
                'Arts':                 'orange-tag',
                'Entertainment':        'orange-tag',
                'Sports':               'orange-tag',
                'Family':               'orange-tag',
                'Community':            'orange-tag',
                'Other':                'orange-tag',
                'Business':             'black-tag',
                'Economy':              'black-tag',
                'Employment':           'black-tag',
                'Education':            'black-tag',
                'Housing':              'black-tag',
                'Energy':               'blue-tag',
                'Transportation':       'blue-tag',
                'Infrastructure':       'blue-tag',
                'Municipal Services':   'blue-tag',
                'Water':                'blue-tag',
                'Government':           'grey-tag',
                'NonProfit':            'grey-tag',
                'Policy':               'grey-tag'}
    
    #mapping = { 'red-tag': ['Civil Rights', 'Health', 'Safety', 'Justice'],
    #            'green-tag': ['Land Use', 'Environment'],
    #            'orange-tag':['Arts', 'Entertainment', 'Sports', 'Family', 'Community', 'Other'],
    #            'black-tag': ['Business', 'Economy', 'Employment', 'Education', 'Housing'],
    #            'blue-tag': ['Transportation', 'Infrastructure', 'Municipal Services'],
    #            'grey-tag': ['Government', 'NonProfit', 'Policy']
    #            }
    return mapping

def getCategoryTagCount():
    categories = getTagCategories()
    tagDict = dict()
    for category in categories:
        tagDict[category] = countTags(category)

    return tagDict

def orphanTag(tag):
        tag['workshopCode'] = 'orphan'
        tag['disabled'] = '1'
        commit(tag)

def Tag(workshop, title):
        tag = Thing('tag')
        tag['title'] = title
        tag['disabled'] = '0'
        tag = generic.linkChildToParent(tag, workshop)
        commit(tag)

