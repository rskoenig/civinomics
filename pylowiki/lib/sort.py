"""
        Basic functions for sorting that can be combined for more complex calculations.
"""
import logging
log = logging.getLogger(__name__)


"""
    ******************************
    *
    *    Functions for sorting binary rating systems (up/down)
    *
    ******************************
"""
def sortBinaryByTopPop(objects):
    """
        Used to sort objects that can be rated 'up' or 'down'.
        Just a straightforward ups - downs calculation.  Ratio of ups to downs is not taken into consideration.
        Good to think of this as a measure of popularity.
        
        Input:        objects    ->    list of Things
        Output:     l                ->    sorted list of Things
    """
    d = {}
    
    for obj in objects:
        score = int(obj['ups']) - int(obj['downs'])
        if score not in d:
            d[score] = [obj]
        else:
            d[score].append(obj)
    
    l = []
    scores = d.keys()
    scores.sort()
    scores.reverse()
    for score in scores:
        objs = d.pop(score)
        if len(objs) > 1:
            for item in objs:
                l.append(item)
        else:
            l.append(objs[0])
    return l

def sortBinaryByBotPop(objects):
    """
        Used to sort objects that can be rated 'up' or 'down'.
        Just a straightforward downs - ups calculation.  Ratio of downs to ups is not taken into consideration.
        Good to think of this as a measure of reverse popularity.
        
        Input:        objects    ->    list of  Things
        Output:     l                ->    sorted list of Things
    """
    l = sortBinaryByTopPop(objects)
    l.reverse()
    return l

def sortBinaryByTopRatio(objects):
    """
        Used to sort objects that can be rated 'up' or 'down'.
        Just a straight forward ups/downs ratio calculation.  The popularity (number of ratings) is not taken into consideration.
        Good to think of this as a measure of quality.
        
        Input:        objects    ->    list of Things
        Output:     l                ->    sorted list of Things
    """
    d = {}
    
    for obj in objects:
        score = float(obj['ups']) / float(obj['downs'])
        if score not in d:
            d[score] = [obj]
        else:
            d[score].append(obj)
            
    l = []
    scores = d.keys()
    scores.sort()
    scores.reverse()
    for score in scores:
        objs = d.pop(score)
        if len(objs) > 1:
            for item in objs:
                l.append(item)
        else:
            l.append(objs[0])
    return l
    
def sortBinaryByBotRatio(objects):
    """
        Used to sort objects that can be rated 'up' or 'down'.
        Just a straight forward downs/ups ratio calculation.  The popularity (number of ratings) is not taken into consideration.
        Good to think of this as a reverse measure of quality.
        
        Input:        objects    ->    list of Things
        Output:     l                ->    sorted list of Things
    """
    l = sortBinaryByTopRatio(objects)
    l.reverse()
    return l


"""
    ******************************
    *
    *    Functions for sorting more continuous rating systems (rate from a to b, where b > a + 1)
    *
    ******************************
"""

def sortContByAvgTop(objects, ratingType):
    """
            Reads the 'ratingAvg_ratingType' field in each Thing and sorts accordingly.
            
            Input:        objects        ->    list of Things
            Output:     l                    ->    sorted list of Things
    """
    d = {}
    
    for obj in objects:
        key = 'ratingAvg_%s' %ratingType
        if key not in obj:
            score = 0
        else:
            score = float(obj[key])
        if score not in d:
            d[score] = [obj]
        else:
            d[score].append(obj)
            
    l = []
    scores = d.keys()
    scores.sort()
    scores.reverse()
    for score in scores:
        objs = d.pop(score)
        if len(objs) > 1:
            for item in objs:
                l.append(item)
        else:
            l.append(objs[0])
    return l
    
def sortContByAvgBot(objects, ratingType):
    """
            Reads the 'ratingAvg_ratingType' field in each Thing and sorts accordingly.
            
            Input:        objects        ->    list of Things
            Output:     l                    ->    sorted list of Things
    """
    l = sortContByAvgTop(objects, ratingType)
    l.reverse()
    return l