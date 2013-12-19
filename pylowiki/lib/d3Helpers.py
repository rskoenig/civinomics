import logging, string

from pylons import session, tmpl_context as c
from pylons import tmpl_context as c, config, session

log = logging.getLogger(__name__)

def addOrUpdateListInSeries(series, thisTime, thisValue):
    if len(series['values']) == 0:
        # add a new entry to the series list, add this time to the timelist
        series['values'].append(
            {
                'x':int(thisTime),
                'y':thisValue
            })
    else:
        # add the views for this object to this day if it's already present in the list
        foundIt = False
        for day in series['values']:
            if int(thisTime) == day['x']:
                # add the value of this item to this day's entry
                # extra: update the label for this day's entry to reflect the number of objects responsible
                day['y'] = day['y'] + thisValue
                foundIt = True
                # stop cycling through the list
                break
        if not foundIt:
            # add a new entry to the series list, add this time to the timelist
            series['values'].append(
                {
                    'x':int(thisTime),
                    'y':thisValue
                })
    return series
