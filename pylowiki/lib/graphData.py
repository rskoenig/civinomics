import logging

from pylons import session, tmpl_context as c
from pylons import tmpl_context as c, config, session

import pylowiki.lib.d3Helpers       as d3Helpers
import pylowiki.lib.utils           as utils

from math import ceil
from operator import itemgetter
import simplejson as json
log = logging.getLogger(__name__)

##################################################
# builds a new json data structure for a constancy chart
##################################################
def buildConstancyData(parent, activities, **kwargs):
    if 'cap' in kwargs:
        cap = kwargs['cap']
    else:
        cap = 100
    if 'typeFilter' in kwargs:
        typeFilter = kwargs['typeFilter']
    else:
        typeFilter = 'all'

    oneList = []
    ideaList = []
    discussionList = []
    resourceList = []
    for item in activities:
        if (item['disabled'] == "1") or (item['deleted'] == "1"):
            continue
        # make a link for this item
        # note: for some reason, 'title' isn't accessible in here so I've modded thingURL to get it for me
        views, title, url = utils.thingURL(parent, item, returnTitle=True)
        # log.info("views: %s"%views)
        # get the date and vote stats
        thisTime = str(item.date)
        upVotes = int(item['ups'])
        downVotes = int(item['downs'])
        totalVotes = upVotes + downVotes
        myComments = 0
        if 'numComments' in item:
            myComments = int(item['numComments'])
        if totalVotes > 0:
            yesPercent = int(float(upVotes)/float(totalVotes) * 100)
            noPercent = int(float(downVotes)/float(totalVotes) * 100)
        else:
            yesPercent = noPercent = 0
        
        if typeFilter == 'all':
            if item.objType == 'idea':
                ideaList.append({
                    'code':item['urlCode'],
                    'title':utils.cap(title, cap),
                    'url':url,
                    'views':int(views),
                    'totalVotes':totalVotes,
                    'yesPercent':yesPercent,
                    'Number of Comments':myComments,
                    '% Yes Votes':yesPercent,
                    'Total Votes':totalVotes,
                    '% No Votes':noPercent,
                    'Total Views':int(views)
                })
            elif item.objType == 'discussion':
                discussionList.append({
                    'code':item['urlCode'],
                    'title':utils.cap(title, cap),
                    'url':url,
                    'views':int(views),
                    'totalVotes':totalVotes,
                    'yesPercent':yesPercent,
                    '% No Votes':noPercent,
                    '% Yes Votes':yesPercent,
                    'Total Votes':totalVotes,
                    'Total Views':int(views),
                    'Number of Comments':myComments
                })
            elif item.objType == 'resource':
                resourceList.append({
                    'code':item['urlCode'],
                    'title':utils.cap(title, cap),
                    'url':url,
                    'views':int(views),
                    'totalVotes':totalVotes,
                    'yesPercent':yesPercent,
                    '% No Votes':noPercent,
                    '% Yes Votes':yesPercent,
                    'Total Votes':totalVotes,
                    'Total Views':int(views),
                    'Number of Comments':myComments
                })
        elif typeFilter == item.objType:
            newList.append({
                'code':item['urlCode'],
                'title':utils.cap(title, 90),
                'url':url,
                'views':int(views),
                'totalVotes':totalVotes,
                'yesPercent':yesPercent,
                '% No Votes':noPercent,
                '% Yes Votes':yesPercent,
                'Total Votes':totalVotes,
                'Total Views':int(views),
                'Number of Comments':myComments
            })
        #elif item.objType == 'comment':
        #    for (key, val) in item:
        #        log.info(key)

    #return json.dumps(newList)
    return json.dumps(oneList), json.dumps(ideaList), json.dumps(discussionList), json.dumps(resourceList)

##################################################
# builds a new json data structure for a bar chart
##################################################
def buildBarData(parent, activities, **kwargs):
    if 'typeFilter' in kwargs:
        typeFilter = kwargs['typeFilter']
    else:
        typeFilter = 'all'

    newList = []
    for item in activities:
        # make a link for this item
        # note: for some reason, 'title' isn't accessible in here so I've modded thingURL to get it for me
        views, title, url = utils.thingURL(parent, item, returnTitle=True)
        # log.info("views: %s"%views)
        # get the date and vote stats
        thisTime = str(item.date)
        upVotes = int(item['ups'])
        downVotes = int(item['downs'])
        totalVotes = upVotes + downVotes

        if typeFilter == 'all':
            newList.append({
                'title':item.objType,
                'type':item.objType,
                'views':int(views),
                'totalVotes':totalVotes,
                'upVotes':upVotes,
                'downVotes':downVotes
            })
        elif typeFilter == item.objType:
            newList.append({
                'title':item.objType,
                'type':item.objType,
                'views':int(views),
                'totalVotes':totalVotes,
                'upVotes':upVotes,
                'downVotes':downVotes
            })
        #elif item.objType == 'comment':
        #    for (key, val) in item:
        #        log.info(key)

    return json.dumps(newList)

    

##################################################
# builds a new json data structure for a bullet chart
##################################################
def buildBulletData(parent, activities, **kwargs):
    newList = []
    for item in activities:
        # make a link for this item
        # note: for some reason, 'title' isn't accessible in here so I've modded thingURL to get it for me
        views, title, url = utils.thingURL(parent, item, returnTitle=True)
        # log.info("views: %s"%views)
        # get the date and vote stats
        thisTime = str(item.date)
        upVotes = int(item['ups'])
        downVotes = int(item['downs'])
        totalVotes = upVotes + downVotes
        newList.append({
            'title':title,
            'subtitle':item.objType,
            'ranges':[downVotes, upVotes, totalVotes],
            'measures':[views],
            'markers':[1]
        })

    return json.dumps(newList)


##################################################
# builds a new json data structure
##################################################
def buildNewData(parent, activities, **kwargs):
    
    newList = []
    for item in activities:
        # make a link for this item
        # note: for some reason, 'title' isn't accessible in here so I've modded thingURL to get it for me
        views, title, url = utils.thingURL(parent, item, returnTitle=True)
        log.info("views: %s"%views)
        # get the date and vote stats
        thisTime = str(item.date)
        upVotes = int(item['ups'])
        downVotes = int(item['downs'])
        totalVotes = upVotes + downVotes
        newList.append({
            'date':thisTime,
            'downVotes':downVotes,
            'title':title,
            'totalVotes':totalVotes,
            'type':item.objType,
            'upVotes':upVotes,
            'url':url,
            'views':views
        })

    return json.dumps(newList)

##################################################
# builds a json data structure that works for nvd3's multiBarChart
# expects a group of activities
##################################################
def buildActivityStackedGroupedData1(activities):
    sbgData = []
    ideas = {
        'key':'Ideas',
        'values':[]
    }
    resources = {
        'key':'Resources',
        'values':[]
    }
    discussions = {
        'key':'Discussions',
        'values':[]
    }
    comments = {
        'key':'Comments',
        'values':[]
    }
    timeList = []
    for item in activities:
        #log.info(item.objType)
        #log.info(item.date
        # round timestamp to nearest day so the bars stack (86,400 seconds in a day)
        itemTime = int(item.date.strftime("%s"))
        nearestDay = itemTime - (itemTime % 86400)
        # create a timestring that nvd3 likes (millisecond precision)
        thisTime = "%s000"%str(nearestDay)
        if 'views' in item.keys():
            y = int(item['views'])
        else:
            y = 1
        ups = int(item['ups'])
        downs = int(item['downs'])
        numVotes = ups + downs
        if thisTime not in timeList:
            newTime = True
        else:
            newTime = False
        if item.objType == 'idea':
            ideas = d3Helpers.addOrUpdateStackedGroupedData(ideas, thisTime, y, newTime=newTime, numVotes=numVotes, ups=ups)
            if newTime:
                resources = d3Helpers.addOrUpdateStackedGroupedData(resources, thisTime, 0, numVotes=0, ups=0)
                discussions = d3Helpers.addOrUpdateStackedGroupedData(discussions, thisTime, 0, numVotes=0, ups=0)
                comments = d3Helpers.addOrUpdateStackedGroupedData(comments, thisTime, 0, numVotes=0, ups=0)
        elif item.objType == 'resource':
            resources = d3Helpers.addOrUpdateStackedGroupedData(resources, thisTime, y, newTime=newTime, numVotes=numVotes, ups=ups)
            if newTime:
                ideas = d3Helpers.addOrUpdateStackedGroupedData(ideas, thisTime, 0, numVotes=0, ups=0)
                discussions = d3Helpers.addOrUpdateStackedGroupedData(discussions, thisTime, 0, numVotes=0, ups=0)
                comments = d3Helpers.addOrUpdateStackedGroupedData(comments, thisTime, 0, numVotes=0, ups=0)
        elif item.objType == 'discussion':
            discussions = d3Helpers.addOrUpdateStackedGroupedData(discussions, thisTime, y, newTime=newTime, numVotes=numVotes, ups=ups)
            if newTime:
                ideas = d3Helpers.addOrUpdateStackedGroupedData(ideas, thisTime, 0, numVotes=0, ups=0)
                resources = d3Helpers.addOrUpdateStackedGroupedData(resources, thisTime, 0, numVotes=0, ups=0)
                comments = d3Helpers.addOrUpdateStackedGroupedData(comments, thisTime, 0, numVotes=0, ups=0)
        elif item.objType == 'comment':
            comments = d3Helpers.addOrUpdateStackedGroupedData(comments, thisTime, y, newTime=newTime, numVotes=numVotes, ups=ups)
            if newTime:
                ideas = d3Helpers.addOrUpdateStackedGroupedData(ideas, thisTime, 0, numVotes=0, ups=0)
                resources = d3Helpers.addOrUpdateStackedGroupedData(resources, thisTime, 0, numVotes=0, ups=0)
                discussions = d3Helpers.addOrUpdateStackedGroupedData(discussions, thisTime, 0, numVotes=0, ups=0)
        timeList.append(thisTime)
    sbgData.append(ideas)
    sbgData.append(resources)
    sbgData.append(discussions)
    sbgData.append(comments)

    return json.dumps(sbgData)

##################################################
# builds a json data structure that works for nvd3's multiBarChart
# expects a group of activities
##################################################
def buildActivityStackedGroupedData2(activities):
    #stacked bar graph data struct 2
    sbgData2 = []
    upList = {
        'key':'Yes Votes',
        'color':'#075D00',
        'values':[]
    }
    downList = {
        'key':'No Votes',
        'color':'#b94a48',
        'values':[]
    }
    timeList = []
    for item in activities:
        itemTime = int(item.date.strftime("%s"))
        nearestDay = itemTime - (itemTime % 86400)
        # create a timestring that nvd3 likes (millisecond precision)
        thisTime = "%s000"%str(nearestDay)
        ups = int(item['ups'])
        downs = int(item['downs'])
        if thisTime not in timeList:
            newTime = True
        else:
            newTime = False
        upList = d3Helpers.addOrUpdateStackedGroupedData(upList, thisTime, 0, newTime=newTime, upsOrDowns=ups)
        downList = d3Helpers.addOrUpdateStackedGroupedData(downList, thisTime, 0, newTime=newTime, upsOrDowns=downs)

        timeList.append(thisTime)
    sbgData2.append(upList)
    sbgData2.append(downList)

    return json.dumps(sbgData2)

##################################################
# builds a json data structure that works for nvd3's multiBarHorizontalChart
# expects a group of initiatives
##################################################
def buildMultiBarHorizontalInitiativeData(initiatives):
    log.info('buildStackedBarInitiativeData')
    initiativeData = []
    series1 = {
        'key':'Low Approval',
        'color':'#b94a48',
        'values':[]
    }
    series2 = {
        'key':'High Approval',
        'color':'#075D00',
        'values':[]
    }
    unsorted2 = []
    unsorted1 = []
    for initiative in initiatives:
        i = initiative
        # u = generic.getThing(i['userCode'])
        # for some reason above wasn't working for new initiatives, replaced with get author routine used in 6_lib
        
            
        if i['deleted'] != u'0' or i['disabled'] != u'0':
            continue
        if i['public'] == '0':
            continue
        entry = {}
        entry['title'] = i['title']
        #entry['description'] = i['description'][:200]
        #if len(entry['description']) >= 200:
        #    entry['description'] += "..."
        #entry['tags'] = i['tags']
        
        entry['voteCount'] = int(i['ups']) + int(i['downs'])
        entry['ups'] = int(i['ups'])
        entry['downs'] = int(i['downs'])
        if entry['voteCount'] > 0:
            #log.info("in total")
            entry['percentYes'] = int(float(entry['ups'])/float(entry['voteCount']) * 100)
            entry['percentNo'] = int(float(entry['downs'])/float(entry['voteCount']) * 100)
            #entry['percentYes'] = float(entry['ups'])/float(entry['voteCount'])
            #entry['percentNo'] = float(entry['downs'])/float(entry['voteCount'])

        #entry['urlCode'] = i['urlCode']
        #entry['url'] = i['url']
        #entry['tag'] = i['tags']
        #entry['initiativeLink'] = "/initiative/" + i['urlCode'] + "/" + i['url'] + "/show"

        if entry['percentYes'] > 50:
            unsorted2.append(
                {
                    'label':"%s, %s percent approval"%(utils.cap(entry['title'], 80), int(entry['percentYes'])),
                    'value':int(entry['voteCount'])
                })
        else:
            unsorted1.append(
                {
                    'label':"%s, %s percent approval"%(utils.cap(entry['title'], 80), int(entry['percentYes'])),
                    'value':int(entry['voteCount'])
                    #'value':int(0 - entry['percentNo'])
                })

    series2['values'] = sorted(unsorted2, key=itemgetter('value'))
    series1['values'] = sorted(unsorted1, key=itemgetter('value'))

    series2['values'].reverse()
    series1['values'].reverse()

    initiativeData.append(series2)
    initiativeData.append(series1)

    return json.dumps(initiativeData)
