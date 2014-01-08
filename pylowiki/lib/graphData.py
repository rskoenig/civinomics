import logging

from pylons import session, tmpl_context as c
from pylons import tmpl_context as c, config, session

import pylowiki.lib.utils           as utils

import pylowiki.lib.d3Helpers       as d3Helpers

from operator import itemgetter
import simplejson as json
log = logging.getLogger(__name__)

##################################################
# builds a new json data structure
##################################################
def buildNewData(activities, **kwargs):
    
    newList = []
    for item in activities:
        #log.info(item.date)
        thisTime = str(item.date)
        if 'type' in kwargs:
            if kwargs['type'] == 'downs':
                val = int(item['downs'])
            else:
                val = int(item['ups'])
        else:
            val = int(item['ups'])
        newList.append({
            'date':thisTime,
            'close':val
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
