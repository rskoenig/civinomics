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
import pylowiki.lib.db.revision     as  revisionLib

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
        elif item['discType'] == 'organization_position':
            entry['objType'] = 'position'
            if item['position'] == 'support':
                entry['position'] = 'support'
            else:
                entry['position'] = 'oppose'
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
    # cut off the <p> </p> misaka is injecting
    entry['html'] = entry['html'][3:-5]

    
    #This is likely to be too large...

    if item.objType == 'initiative':
        entry['fullText'] = item['proposal']
    else:
        entry['fullText'] = ''
    entry['fullText'] = m.html(entry['fullText'], render_flags=m.HTML_SKIP_HTML)

    """    
    if item.objType == 'initiative':
        if item['proposal'] != None and item['proposal'] != '':
            entry['fullText'] = True;
    else:
        entry['fullText'] = False
    """

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

        if 'workshopCode' in item and 'initiativeCode' not in item:
            entry['parentHref'] = '/workshop/' + item['workshopCode'] + '/' + item['workshop_url']
            #entry['href'] = entry['parentHref'] + entry['href']
        elif 'initiativeCode' in item:
            entry['parentHref'] = '/initiative/' + item['initiativeCode'] + '/' + item['initiative_url']
            if entry['objType'] == 'update':
                entry['href'] = entry['parentHref'] + '/updateShow/' + item['urlCode']
            else:
                entry['href'] = entry['parentHref'] + entry['href']
    
    # modifications for children of workshops and initiatives
    entry['parentTitle'] = ''
    entry['parentObjType'] = ''
    if 'workshopCode' in item and 'initiativeCode' not in item:
        entry['parentTitle'] = item['workshop_title']
        entry['parentObjType'] = 'workshop'
    elif 'initiativeCode' in item:
        entry['parentTitle'] = item['initiative_title']
        entry['parentObjType'] = 'initiative'
    
    # should list the more specific object rather than workshop if possible
    if 'ideaCode' in item:
        if 'idea_title' in item:
            entry['parentTitle'] = item['idea_title']
        entry['parentObjType'] = 'idea'
        if 'ideaCode' in item and 'idea_url' in item: 
            entry['parentHref'] = '/idea/' + item['ideaCode'] + '/' + item['idea_url']

    # to support listing of comments in the profile
    if item.objType == 'comment':
        if 'ideaCode' in item:
            parentCode = item['ideaCode']
            parentURL = item['parent_url']
            parentObjType = 'idea'
            parentObjType = 'idea'
            if 'idea_title' in item:
                entry['parentTitle'] = item['idea_title']
            else:
                entry['parentTitle'] == ''
            entry['parentHref'] = "/" + parentObjType + "/" + parentCode + "/" + parentURL
        elif 'resourceCode' in item:
            parentCode = item['resourceCode']
            parentURL = item['parent_url']
            parentObjType = 'resource'
            parentObjType = 'resource'
            if 'resource_title' in item:
                entry['parentTitle'] = item['resource_title']
            else:
                entry['parentTitle'] == ''
            entry['parentHref'] = "/" + parentObjType + "/" + parentCode + "/" + parentURL
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
        elif 'discussionCode' in item:
            parentCode = item['discussionCode']
            parentURL = item['parent_url']
            parentObjType = 'discussion'
            if 'discussion_title' in item:
                entry['parentTitle'] = item['discussion_title']
            else:
                entry['parentTitle'] == ''
            entry['parentHref'] = "/" + parentObjType + "/" + parentCode + "/" + parentURL
        elif 'photoCode' in item:
            parentCode = item['photoCode']
            parentURL = item['parent_url']
            parentObjType = 'photo'
            entry['parentHref'] = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
        elif 'meetingCode' in item:
            parentCode = item['meetingCode']
            parentURL = item['meeting_url']
            parentObjType = 'meeting'
            entry['parentHref'] = "/meeting/" + parentCode + "/" + parentURL + "/show/"
        elif 'profileCode' in item:
            parentCode = item['profileCode']
            entry['parentHref'] = "/profile/" + item['profileCode'] + "/" + item['profile_url'] + "/photo/show/" + parentCode
        elif 'workshopCode' in item:
            workshopLink = "/workshop/" + item['workshopCode'] + "/" + item['workshop_url']
            entry['parentHref'] = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
        else:
            entry['parentHref'] = workshopLink + "/" + parentObjType + "/" + parentCode + "/" + parentURL
        
        # comment author
        author = userLib.getUserByID(item.owner)
        entry['authorName'] = author['name']
        entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']
        entry['authorPhoto'] = utils._userImageSource(author)
        if 'user' in session and (c.authuser.id == item.owner or userLib.isAdmin(c.authuser.id)):
            entry['canEdit'] = 'yes'
        else:
            entry['canEdit'] = 'no'
            
        # get revisions
        revisions = revisionLib.getRevisionsForThing(item)
        if revisions:
            entry['revisions'] = 'yes'
        else:
            entry['revisions'] = 'no'
        entry['revisionList'] = []
        if revisions:
            for rev in revisions:
                revision = {}
                code = rev['urlCode'] 
                date = str(rev.date)
                text = rev['data']
                html = m.html(rev['data'], render_flags=m.HTML_SKIP_HTML)
                if 'commentRole' in rev:
                    role = rev['commentRole']
                else:
                    role = 'Neutral'
                    
                if role == 'yes':
                    role = 'Pro'
                elif role == 'no':
                    role = 'Con'
                else:
                    role = 'Neutral'
                    
                revision['date'] = date
                revision['urlCode'] = code
                revision['text'] = text
                revision['html'] = html
                revision['role'] = role
                entry['revisionList'].append(revision)
        entry['commentRole'] = ''
        if 'commentRole' in item:
            entry['commentRole'] = item['commentRole']
        if 'ideaCode' in item or 'initiativeCode' in item or 'meetingCode' in item:
            entry['doCommentRole'] = 'yes'
        else:
            entry['doCommentRole'] = 'no'

    if 'parentTitle' in entry:
        if len(entry['parentTitle']) >= 35:
            entry['parentTitleAbrv'] = entry['parentTitle'][0:32] + '...'
        else:
            entry['parentTitleAbrv'] = entry['parentTitle']

    # photo
    if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
        entry['mainPhoto'] = "/images/photos/%s/orig/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
        entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
    elif item.objType == 'initiative':
        entry['mainPhoto'] = "/images/icons/generalInitiative.jpg"
        entry['thumbnail'] = "/images/icons/generalInitiative.jpg"

    # to place workshop thumbnail in child listings
    #elif entry['parentObjType'] == 'workshop':
    #    mainImage = mainImageLib.getMainImageByCode(item['workshopCode'])
    #    if mainImage['pictureHash'] == 'supDawg':
    #        entry['thumbnail'] = "/images/slide/thumbnail/supDawg.thumbnail"
    #    elif 'format' in mainImage.keys():
    #        entry['thumbnail'] = "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
    #    else:
    #        entry['thumbnail'] = "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])

    elif entry['parentObjType'] == 'initiative':
        initiative = initiativeLib.getInitiative(item['initiativeCode'])
        if 'directoryNum_photos' in initiative:
            entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(initiative['directoryNum_photos'], initiative['pictureHash_photos'])
            entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(initiative['directoryNum_photos'], initiative['pictureHash_photos'])
        else: 
            entry['mainPhoto'] = "/images/icons/generalInitiative.jpg"
            entry['thumbnail'] = "/images/icons/generalInitiative.jpg"
    else:
        entry['mainPhoto'] = '0'
        entry['thumbnail'] = '0'

    #tags
    tags = []
    tagList = []
    if 'tags' in item:
        if item['tags'] != None:
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
    if 'discussion_child' in item:    
        entry['discussion'] = item['discussion_child']
    elif item.objType == 'disucssion':
        entry['discussion'] = item['urlCode']
    else:
        discussion = discussionLib.getDiscussionForThing(item)
        if discussion:    
            entry['discussion'] = discussion['urlCode']

    entry['numComments'] = 0
    if 'numComments' in item:
        entry['numComments'] = item['numComments']


    if 'user_name' in item:
        entry['authorName'] = item['user_name']    
        entry['authorCode'] = item['userCode']
        entry['authorURL'] = item['user_url']
        entry['authorHref'] = '/profile/' + item['userCode'] + '/' + item['user_url']
        if 'user_avatar' in item:
            entry['authorPhoto'] = item['user_avatar']
        else: 
            entry['authorPhoto'] = ""

        #hack to show initiative authors/coauthors
        # better to add featured author data to the object
        if item['user_name'] == 'Civinomics Facilitator':
            coAuthors = facilitatorLib.getFacilitatorsByInitiative(item)
            if len(coAuthors) != 0:
                f = coAuthors[0]
                author = userLib.getUserByID(f.owner)
                entry['authorName'] = author['name']
                entry['authorPhoto'] = utils._userImageSource(author)
                entry['authorCode'] = author['urlCode']
                entry['authorURL'] = author['url']
                entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

            else:
                author = userLib.getUserByID(item.owner)
                entry['authorName'] = item['user_name']
                entry['authorPhoto'] = item['user_avatar']
                entry['authorCode'] = item['userCode']
                entry['authorURL'] = item['user_url']
                entry['authorHref'] = '/profile/' + item['userCode'] + '/' + item['user_url']
    else:
        author = userLib.getUserByID(item.owner)
        entry['authorName'] = author['name']
        entry['authorPhoto'] = utils._userImageSource(author)
        entry['authorCode'] = author['urlCode']
        entry['authorURL'] = author['url']
        entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']


    # special case for meetings
    if item.objType == 'meeting':
        aCount = meetingLib.getAgendaItems(item['urlCode'], 1)
        dList = item['meetingDate'].split('-')
        entry['meetingDate'] = "%s-%s-%s"%(dList[1], dList[2], dList[0])
        if 'agendaPostDate' in item and item['agendaPostDate'] != '':
            dList = item['agendaPostDate'].split('-')
            if len(dList) == 3:
                entry['agendaPostDate'] = "%s-%s-%s"%(dList[1], dList[2], dList[0])
            else:
                entry['agendaPostDate'] = item['agendaPostDate']
        else:
            entry['agendaPostDate'] = ""
        entry['meetingTime'] = item['meetingTime']
        entry['location'] = item['location']
        entry['group'] = item['group']
        entry['href'] += '/show'
        entry['agendaItemCount'] = str(aCount)
    
    if 'readOnly' in item:
        entry['readOnly'] = item['readOnly']
    else:
        entry['readOnly'] = "0"

    if 'commentRole' in item:
        entry['position'] = item['commentRole']

    if 'adopted' in item and item['adopted'] == '1':
        entry['status'] = 'adopted'
    elif 'disabled' in item and item['disabled'] == '1':
        entry['status'] = 'disabled'
    else:
        entry['status'] = '0'

    if 'readOnly' in item and item['readOnly'] == '1':
        entry['readOnly'] = '1'
    else:
        entry['readOnly'] = '0'
        
        #Subcategory tags
    if 'subcategory_tags' in item:
        entry['subcategory_tags'] = item['subcategory_tags']

    return entry


def getJsonInitiativesShort(item):
    myRatings = {}
    if 'ratings' in session:
        myRatings = session['ratings']

    entry = {}
    # item attributes
    entry['title'] = item['title']
    entry['objType'] = item.objType
    entry['text'] = item['description']
    entry['urlCode'] = item['urlCode']
    entry['url'] = item['url']
    entry['href'] = '/initiative/' + item['urlCode'] + '/' + item['url']
    entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
    entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)

    # assuming for now...
    entry['parentObjType'] = 'workshop'

    if 'views' in item:
        views = int(item['views'])
    else:
        views = 1
    views += 1
    item['views'] = str(views)
    dbHelpers.commit(item)
    entry['views'] = item['views']

    #photo
    if 'directoryNum_photos' in item:
        entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
        entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
    else: 
        entry['mainPhoto'] = "/images/icons/generalInitiative.jpg"
        entry['thumbnail'] = "/images/icons/generalInitiative.jpg"

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

    # comments
    if 'discussion_child' in item:    
        entry['discussion'] = item['discussion_child']
        entry['userCommented'] = False
        if c.authuser:
            result = commentLib.checkUserCommentInDiscussion(c.authuser, entry['discussion'])
            if result:
                entry['userCommented'] = True

    entry['numComments'] = 0
    if 'numComments' in item:
        entry['numComments'] = item['numComments']
    


    if 'user_name' in item:
        entry['authorName'] = item['user_name']    
        entry['authorCode'] = item['userCode']
        entry['authorURL'] = item['user_url']
        entry['authorHref'] = '/profile/' + item['userCode'] + '/' + item['user_url']
        entry['authorPhoto'] = item['user_avatar']

        #hack to show initiative authors/coauthors
        # better to add featured author data to the object
        if item['user_name'] == 'Civinomics Facilitator':
            coAuthors = facilitatorLib.getFacilitatorsByInitiative(item)
            if len(coAuthors) != 0:
                f = coAuthors[0]
                author = userLib.getUserByID(f.owner)
                entry['authorName'] = author['name']
                entry['authorPhoto'] = utils._userImageSource(author)
                entry['authorCode'] = author['urlCode']
                entry['authorURL'] = author['url']
                entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

            else:
                author = userLib.getUserByID(item.owner)
                entry['authorName'] = item['user_name']
                entry['authorPhoto'] = item['user_avatar']
                entry['authorCode'] = item['userCode']
                entry['authorURL'] = item['user_url']
                entry['authorHref'] = '/profile/' + item['userCode'] + '/' + item['user_url']
    else:
        author = userLib.getUserByID(item.owner)
        entry['authorName'] = author['name']
        entry['authorPhoto'] = utils._userImageSource(author)
        entry['authorCode'] = author['urlCode']
        entry['authorURL'] = author['url']
        entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

        

    #Subcategory tags
    if 'subcategory_tags' in item:
        entry['subcategory_tags'] = item['subcategory_tags']
    
    if 'readOnly' in item:
        entry['readOnly'] = item['readOnly']
    else:
        entry['readOnly'] = "0"

    if 'adopted' in item and item['adopted'] == '1':
        entry['status'] = 'adopted'
    elif 'disabled' in item and item['disabled'] == '1':
        entry['status'] = 'disabled'
    else:
        entry['status'] = '0'

    return entry
