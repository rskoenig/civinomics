import logging, string

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
from hashlib import md5
from pylons import tmpl_context         as c, config, session
import pylowiki.lib.db.discussion 		as discussionLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.user           as userLib
import pylowiki.lib.db.generic          as generic
import pylowiki.lib.fuzzyTime           as fuzzyTime 
import pylowiki.lib.utils           	as utils    

import urllib2

import misaka as m
import copy as copy
from HTMLParser import HTMLParser

log = logging.getLogger(__name__)

# For base62 conversion
BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

def getJsonProperties(item):
    myRatings = {}
    if 'ratings' in session:
        myRatings = session['ratings']

    entry = {}
    # item attributes
    entry['title'] = item['title']
    entry['objType'] = item.objType
    if item.objType == 'discussion':
        if item['discType'] == 'update':
            entry['objType'] = 'update'
    entry['urlCode'] = item['urlCode']
    entry['url'] = item['url']
    entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
    entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)
    if 'views' in item:
        entry['views'] = str(item['views'])
    else:
        entry['views'] = '0'

    # attributes that vary accross items
    entry['text'] = ''
    if 'text' in item:
        entry['text'] = item['text']
    elif 'description' in item:
        entry['text'] = item['description']
    entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
    if 'link' in item:
        entry['link'] = item['link']
    else:
        entry['link'] = ''
    if 'cost' in item:
        entry['cost'] = item['cost']
    else:
        entry['cost'] = ''
    entry['article'] = 'a'
    if entry['objType'] == 'idea' or entry['objType'] == 'update' or entry['objType'] == 'initiative':
        entry['article'] = 'an'

    # href
    # note: we should standardize the way object urls are constructed
    if item.objType == 'photo':
        entry['href'] = '/profile/' + item['userCode'] + '/' + item['user_url'] + "/photo/show/" + item['urlCode']
    else:
        entry['href'] = '/' + item.objType + '/' + item['urlCode'] + '/' + item['url']

    if 'workshopCode' in item:
        entry['parentHref'] = '/workshop/' + item['workshopCode'] + '/' + item['workshop_url']
        entry['href'] = entry['parentHref'] + entry['href']
    elif 'initiativeCode' in item:
        entry['parentHref'] = '/initiative/' + item['initiativeCode'] + '/' + item['initiative_url']
        if entry['objType'] == 'update':
            entry['href'] = entry['parentHref'] + '/updateShow/' + item['urlCode']
        else:
            entry['href'] = entry['parentHref'] + entry['href']
    
    # modifications for children of workshops and initiatives
    entry['parentTitle'] = ''
    entry['parentObjType'] = ''
    if 'workshopCode' in item:
        entry['parentTitle'] = item['workshop_title']
        entry['parentObjType'] = 'workshop'
    elif 'initiativeCode' in item:
        entry['parentTitle'] = item['initiative_title']
        entry['parentObjType'] = 'initiative'

    # photo
    if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
        entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
        entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
    elif entry['parentObjType'] == 'workshop':
        mainImage = mainImageLib.getMainImageByCode(item['workshopCode'])
        if mainImage['pictureHash'] == 'supDawg':
            entry['thumbnail'] = "/images/slide/thumbnail/supDawg.thumbnail"
        elif 'format' in mainImage.keys():
            entry['thumbnail'] = "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
        else:
            entry['thumbnail'] = "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])

    elif entry['parentObjType'] == 'initiative':
        initiative = initiativeLib.getInitiative(item['initiativeCode'])
        entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(initiative['directoryNum_photos'], initiative['pictureHash_photos'])
        entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(initiative['directoryNum_photos'], initiative['pictureHash_photos'])
    else:
        entry['mainPhoto'] = '0'
        entry['thumbnail'] = '0'

    #tags
    tags = []
    tagList = []
    if 'tags' in item:
        tagList = item['tags'].split('|')
    elif 'initiative_tags' in item:
        tagList = item['initiative_tags'].split('|')
    elif 'workshop_category_tags' in item:
        tagList = item['workshop_category_tags'].split('|')
    for tag in tagList:
        if tag and tag != '':
            tags.append(tag)
    entry['tags'] = tags

    # scope attributes
    if 'scope' in item:
        entry['scope'] = item['scope']
    elif 'initiative_scope' in item:
        entry['scope'] = item['initiative_scope']
    elif 'workshop_public_scope' in item:
        entry['scope'] = item['workshop_public_scope']
    else:
        entry['scope'] = '0||united-states||0||0||0|0'
    scopeInfo = utils.getPublicScope(entry['scope'])
    entry['scopeName'] = scopeInfo['name']
    entry['scopeLevel'] = scopeInfo['level']
    entry['scopeHref'] = scopeInfo['href']
    entry['flag'] = scopeInfo['flag']

    # user rating
    if entry['urlCode'] in myRatings:
        entry['rated'] = myRatings[entry['urlCode']]
        entry['vote'] = 'voted'
    else:
        entry['rated'] = 0
        entry['vote'] = 'nvote'

    # votes
    entry['voteCount'] = int(item['ups']) + int(item['downs'])
    entry['ups'] = int(item['ups'])
    entry['downs'] = int(item['downs'])
    entry['netVotes'] = int(item['ups']) - int(item['downs'])

    #goal votes
    if entry['voteCount'] < 100:
        entry['goal'] = 100
    elif 'goal' in item:
        entry['goal'] = item['goal']
    else:
        entry['goal'] = 100

    # comments
    discussion = discussionLib.getDiscussionForThing(item)
    entry['discussion'] = discussion['urlCode']
    entry['numComments'] = 0
    if 'numComments' in item:
        entry['numComments'] = item['numComments']

    # author data
    # CCN - need to find a way to optimize this lookup
    author = userLib.getUserByID(item.owner)
    entry['authorName'] = author['name']
    entry['authorPhoto'] = utils._userImageSource(author)
    entry['authorCode'] = author['urlCode']
    entry['authorURL'] = author['url']
    entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

    entry['parentTitle'] = ''
    entry['parentObjType'] = ''
    entry['article'] = 'a'
    if entry['objType'] == 'idea' or entry['objType'] == 'update' or entry['objType'] == 'initiative':
        entry['article'] = 'an'

    # modifications for children of workshops and initiatives
    if 'workshopCode' in item:
        entry['parentTitle'] = item['workshop_title']
        entry['parentObjType'] = 'workshop'
    elif 'initiativeCode' in item:
        entry['parentTitle'] = item['initiative_title']
        entry['parentObjType'] = 'initiative'

    return entry