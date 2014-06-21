import logging, string

from pylons import session, tmpl_context as c
from pylons import tmpl_context as c, config, session

log = logging.getLogger(__name__)

##################################################
# adds a new piece of data depending if the date is covered yet.
##################################################
def addOrUpdateNewData(series, thisTime, thisValue, **kwargs):
    if len(series) == 0:
        # add a new entry to the series list, add this time to the timelist
        series.append(
            {
                'date':int(thisTime),
                'close':thisValue
            })
    else:
        #if 'newTime' in kwargs:
            #if kwargs['newTime'] == True:
                # react to this flag by appending this time to the values list
                # otherwise, search for this time in the list and add this value to it
                # works in theory, but not in this function
        ########### # # # # #
        # add the views for this object to this day if it's already present in the list
        foundIt = False
        for day in series:
            if int(thisTime) == day['date']:
                # add the value of this item to this day's entry
                # extra: update the label for this day's entry to reflect the number of objects responsible
                day['close'] = day['close'] + thisValue
                foundIt = True
                # stop cycling through the list
                break
        if not foundIt:
            # add a new entry to the series list, add this time to the timelist
            series.append(
                {
                    'date':int(thisTime),
                    'close':thisValue
                })
    return series

##################################################
# adds a new piece of data depending if the date is covered yet.
##################################################
def addOrUpdateStackedGroupedData(series, thisTime, thisValue, **kwargs):
    ups = 0
    downs = 0
    upsOrDowns = 0
    numVotes = 0
    if 'ups' in kwargs:
        ups = kwargs['ups']
    if 'downs' in kwargs:
        downs = kwargs['downs']
    if 'upsOrDowns' in kwargs:
        upsOrDowns = kwargs['upsOrDowns']
    if 'numVotes' in kwargs:
        numVotes = kwargs['numVotes']
    if len(series['values']) == 0:
        # add a new entry to the series list, add this time to the timelist
        series['values'].append(
            {
                'x':int(thisTime),
                'y':thisValue,
                'ups':ups,
                'downs':downs,
                'upsOrDowns':upsOrDowns,
                'numVotes':numVotes
            })
    else:
        #if 'newTime' in kwargs:
            #if kwargs['newTime'] == True:
                # react to this flag by appending this time to the values list
                # otherwise, search for this time in the list and add this value to it
                # works in theory, but not in this function
        ########### # # # # #
        # add the views for this object to this day if it's already present in the list
        foundIt = False
        for day in series['values']:
            if int(thisTime) == day['x']:
                # add the value of this item to this day's entry
                # extra: update the label for this day's entry to reflect the number of objects responsible
                day['y'] = day['y'] + thisValue
                day['ups'] = day['ups'] + ups
                day['downs'] = day['downs'] + downs
                day['upsOrDowns'] = day['upsOrDowns'] + upsOrDowns
                day['numVotes'] = day['numVotes'] + numVotes
                foundIt = True
                # stop cycling through the list
                break
        if not foundIt:
            # add a new entry to the series list, add this time to the timelist
            series['values'].append(
                {
                    'x':int(thisTime),
                    'y':thisValue,
                    'ups':ups,
                    'downs':downs,
                    'upsOrDowns':upsOrDowns,
                    'numVotes':numVotes
                })
    return series
