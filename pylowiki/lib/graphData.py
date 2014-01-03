import logging

from pylons import session, tmpl_context as c
from pylons import tmpl_context as c, config, session

import pylowiki.lib.utils           as utils

from operator import itemgetter
import simplejson as json
log = logging.getLogger(__name__)

##################################################
# builds a json data structure that works for nvd3's multiBarHorizontalChart
# expects a group of initiatives
##################################################
def buildStackedBarInitiativeData(initiatives):
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
