import logging, string

from urllib import quote
from zlib import adler32
from pylons import session, tmpl_context as c
from hashlib import md5
from pylons import tmpl_context         as c, config, session
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.message          as messageLib
import pylowiki.lib.db.photo            as photoLib
import pylowiki.lib.db.pmember          as pMemberLib
import pylowiki.lib.sort                as sort
import pylowiki.lib.db.mainImage        as mainImageLib
import pylowiki.lib.db.follow           as followLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.initiative       as initiativeLib
import pylowiki.lib.db.activity         as activityLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.comment          as commentLib
import pylowiki.lib.db.meeting          as meetingLib
import pylowiki.lib.utils               as utils
import pylowiki.lib.fuzzyTime           as fuzzyTime
import pylowiki.lib.db.dbHelpers        as dbHelpers

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
    if 'title' in item:
        entry['title'] = item['title']
    else: 
        entry['title'] = ''
    entry['objType'] = item.objType
    if item.objType == 'discussion':
        if item['discType'] == 'update':
            entry['objType'] = 'update'
    entry['urlCode'] = item['urlCode']
    if 'url' in item:
        entry['url'] = item['url']
    else:
        entry['url'] = ''
    entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
    entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)
    if 'views' in item:
        views = int(item['views'])
    else:
        views = 1

    views += 1
    item['views'] = str(views)
    dbHelpers.commit(item)
    entry['views'] = item['views']

    # attributes that vary accross items
    entry['text'] = ''
    if 'text' in item:
        entry['text'] = item['text']
    elif 'description' in item:
        entry['text'] = item['description']
    elif 'data' in item:
        entry['text'] = item['data']


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

    elif item.objType != 'comment':
        entry['href'] = '/' + item.objType + '/' + item['urlCode'] + '/' + item['url']
        # need to account for comment obj type

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

    # to support listing of comments in the profile
    if item.objType == 'comment':
        if 'workshopCode' in item:
            workshopLink = "/workshop/" + item['workshopCode'] + "/" + item['workshop_url']
            if 'ideaCode' in item:
                parentCode = item['ideaCode']
                parentURL = item['parent_url']
                parentObjType = 'idea'
            elif 'resourceCode' in item:
                parentCode = item['resourceCode']
                parentURL = item['parent_url']
                parentObjType = 'resource'
            elif 'discussionCode' in item:
                parentCode = item['discussionCode']
                parentURL = item['parent_url']
                parentObjType = 'discussion'
            entry['parentHref'] = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL

        elif 'photoCode' in item:
            parentCode = item['photoCode']
            parentURL = item['parent_url']
            parentObjType = 'photo'
            entry['parentHref'] = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
        elif 'initiativeCode' in item and 'resourceCode' in item:
            parentCode = item['resourceCode']
            parentURL = item['parent_url']
            parentObjType = 'resource'
            entry['parentHref'] = "/initiative/" + item['initiativeCode'] + "/" + item['initiative_url'] + "/resource/"+ parentCode + "/" + parentURL
        elif 'initiativeCode' in item:
            parentCode = item['initiativeCode']
            parentURL = item['parent_url']
            parentObjType = 'initiative'
            entry['parentHref'] = "/initiative/" + parentCode + "/" + parentURL + "/show/"
        elif 'meetingCode' in item:
            parentCode = item['meetingCode']
            parentURL = item['meeting_url']
            parentObjType = 'meeting'
            entry['parentHref'] = "/meeting/" + parentCode + "/" + parentURL + "/show/"
        elif 'profileCode' in item:
            entry['parentHref'] = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
        else:
            log.info("no parentObjType item is %s"%item.keys())
            entry['parentHref'] = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL


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
    if 'ups' in item:
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
    if discussion:    
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

    # special case for meetings
    if item.objType == 'meeting':
        aCount = meetingLib.getAgendaItems(item['urlCode'], 1)
        dList = item['meetingDate'].split('-')
        entry['meetingDate'] = "%s-%s-%s"%(dList[1], dList[2], dList[0])
        if 'agendaPostDate' in item and item['agendaPostDate'] != '':
            dList = item['agendaPostDate'].split('-')
            entry['agendaPostDate'] = "%s-%s-%s"%(dList[1], dList[2], dList[0])
        else:
            entry['agendaPostDate'] = ""
        entry['meetingTime'] = item['meetingTime']
        entry['location'] = item['location']
        entry['group'] = item['group']
        entry['href'] += '/show'
        entry['agendaItemCount'] = str(aCount)

    if 'commentRole' in item:
        entry['position'] = item['commentRole']

    return entry