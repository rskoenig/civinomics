from pylons import tmpl_context as c, config, session
from pylowiki.model import Thing, meta, Data
from pylowiki.lib.utils import urlify, toBase62
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl
import generic


log = logging.getLogger(__name__)

def getParentTags(parent):
    parentCode = parent.objType + 'Code'
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'tags')\
                .filter(Thing.data.any(wc(parentCode, parent['urlCode'])))\
                .all()
    except:
        return False
        
def getSearchTags(tag, disabled = '0'):
    searchTag = '|' + tag + '|'
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'tags')\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .filter(Thing.data.any(wcl('tagString', searchTag)))\
                .all()
    except:
        return False

def getWorkshopTagCategories():
    workshopTags = []
    workshpTags.append('Arts')
    workshopTags.append('Business')
    workshopTags.append('Civil Rights')
    workshopTags.append('Community')
    workshopTags.append('Economy')
    workshopTags.append('Education')
    workshopTags.append('Employment')
    workshopTags.append('Entertainment')
    workshopTags.append('Environment')
    workshopTags.append('Family')
    workshopTags.append('Government')
    workshopTags.append('Health')
    workshopTags.append('Housing')
    workshopTags.append('Infrastructure')
    workshopTags.append('Justice')
    workshopTags.append('Land Use')
    workshopTags.append('Municipal Services')
    workshopTags.append('NonProfit')
    workshopTags.append('Policy')
    workshopTags.append('Safety')
    workshopTags.append('Sports')
    workshopTags.append('Transportation')
    workshopTags.append('Other')
    return workshopTags       

def getWorkshopCategoryTagCount(disabled = '0'):
    workshopTagsList =  meta.Session.query(Thing)\
            .filter_by(objType = 'tags')\
            .filter(Thing.data.any(wc('tagsType', 'workshopTags')))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .all()
    workshopTagsCount = dict()
    for tags in workshopTagsList:
        # tag strings are prepended, appended, and separated by the | character
        # so we strip off the first and last character here to avoid empty list elements
        tagsList = tags['tagsString'][1:-1].split('|')
        for tag in tagsList:
            tag = tag.strip()
            if tag in tagDict:
                workshopTagsCount[tag] += 1
            else:
                workshopTagsCount[tag] = 1

    return workshopTagsCount

def setTagsEnable(parent, disabled):
    parentCode = parent.objType + 'Code'
    tagsList =  meta.Session.query(Thing)\
            .filter_by(objType = 'tags')\
            .filter(Thing.data.any(wc(parentCode, thing['urlCode'])))\
            .all()
    for tags in tagsList:
       tags['disabled'] = disabled
       commit(tags)
            
def Tags(tagsType, tagsString, parent, owner):
    tags = Thing('tags', owner.id)
    tags['type'] = tagsType
    tags['tagsString'] = tagsString
    tags['disabled'] = '0'
    commit(tags)
    tags['urlCode'] = toBase62(tags)
    tags = generic.linkChildToParent(tags, parent)
    commit(tags)


