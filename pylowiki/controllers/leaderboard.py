import logging, datetime, time, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.db.suggestion import getActiveSuggestionsForWorkshop
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.comment import getComment
from pylowiki.lib.db.resource import getActiveResourcesByWorkshopID
from pylowiki.lib.db.discussion import getActiveDiscussionsForWorkshop
from pylowiki.lib.db.follow import getUserFollows, isFollowing
from pylowiki.lib.db.user import getActiveUsers, getUserByID
from pylowiki.lib.db.rating import getRatingByID
from pylowiki.lib.fuzzyTime import timeSince


from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

"""
    This file contains all leaderboard lists generated.
    The format of this file includes many Board functions which are making a ranking system
        These functions use helper functions which will be directly above the Board function
        There is also an addRank function which adds the user's rank on these lists to their main leaderboard
    Also there is a GenerateLists function which calls the Board functions to use
        Which is called by the page rendering function
"""

# Recursively gets the number of children a comment has + number of votes each child has

def MostActiveSuggestions(sug):
    "Gets when the suggestion was created as "
    sugCreated = time.mktime(sug.date.timetuple())
    curTime = time.time()
    elapsedTime = sugCreated - curTime
    popularity = getSuggestionPopularity(sug)
    if popularity > 0:
        Activity = -(elapsedTime/popularity)
        return Activity 
    else:
        return 0

def SugActivityBoard(page, suggestions):

    " Sorted by most actions per amount of time, basically actions/(duration of existence)"
    sugActiveList = sorted(suggestions, key=lambda x: MostActiveSuggestions(x))

    userSugActiveRank = [i for i,x in enumerate(sugActiveList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userSugActiveRank != []:
        sug = sugActiveList[userSugActiveRank[0]]
        sugCreated = time.mktime(sug.date.timetuple())
        curTime = time.time()
        elapsedTime = -(sugCreated - curTime)
        value = str(getSuggestionPopularity(sug)) + ' Comments/Ratings Over ' + str(timeSince(sug.date))
        title = [sug['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + sug['urlCode'] + '/' + sug['url'])] 
    addRanks('Suggestion Activity', 'sugActivity', userSugActiveRank, len(sugActiveList), title, value) 


    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Ratings', 'Average Rating'] 
        rows = [] 
        count = 1 
        
        for s in sugActiveList:
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            totalComs = getDiscussionByID(int(s['discussion_id']))['numComments']
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
                                    
            row.append(count) 
            row.append(name) 
            row.append(totalComs) 
            row.append(numRatings) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Suggestion Activity', 'sugActivity', headers, rows) 
        
    if page == 'userRanks' and userSugActiveRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Ratings', 'Average Rating'] 
        rows = [] 
        
        for index in userSugActiveRank:
            s = sugActiveList[index]
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            totalComs = getDiscussionByID(int(s['discussion_id']))['numComments']
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
                                    
            row.append(str(index+1) + ' / ' + str(len(sugActiveList))) 
            row.append(name) 
            row.append(totalComs) 
            row.append(numRatings) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            
        addBoardDict('Suggestion Activity', 'sugActivity', headers, rows) 
        

def MostActiveResource(res):
    "Gets when the suggestion was created as "
    resCreated = time.mktime(res.date.timetuple())
    curTime = time.time()
    elapsedTime = resCreated - curTime
    popularity = getResourcePopularity(getDiscussionByID(int(res['discussion_id'])))
    if popularity > 0:
        Activity = -(elapsedTime/popularity)
        return Activity 
    else:
        return 0

def ResActivityBoard(page, resources):
    
    " Sorted by most actions per amount of time, basically actions/(duration of existence)"
    resActiveList = sorted(resources, key=lambda x: MostActiveResource(x))

    userResActiveRank = [i for i,x in enumerate(resActiveList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userResActiveRank != []:
        res = resActiveList[userResActiveRank[0]]
        resCreated = time.mktime(res.date.timetuple())
        curTime = time.time()
        elapsedTime = -(resCreated - curTime)
        value = str(getResourcePopularity(getDiscussionByID(res['discussion_id']))) + ' Comments/Ratings Over ' + str(str(timeSince(res.date)))
        title = [res['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + res['urlCode'] + '/' + res['url'])]
    addRanks('Resource Activity', 'resActivity', userResActiveRank, len(resActiveList), title, value) 
 
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1     

        for r in resActiveList:
            row = [] 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Resource Activity', 'resActivity', headers, rows) 

    if page == 'userRanks' and userResActiveRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 

        for index in userResActiveRank:
            r = resActiveList[index]
            row = [] 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append((str(index+1) + ' / ' + str(len(resActiveList))) ) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            
        addBoardDict('Resource Activity', 'resActivity', headers, rows) 

def getSuggestionPopularity(sug):
    ratingsList = sug['ratingIDs_overall'].split(',')
    ratings = len(ratingsList)
    numComments = getDiscussionByID(int(sug['discussion_id']))['numComments']
    popularity = ratings + int(numComments)
    return popularity

"Most Popular Suggestion LeaderBoard: Determined by #Comment + #Ratings"
def SugPopularityBoard(page, suggestions):

    "Sorted By most comments and ratings"
    sugPopularList = sorted(suggestions, key=lambda x: getSuggestionPopularity(x), reverse = True)

    userSugPopularRank = [i for i,x in enumerate(sugPopularList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userSugPopularRank != []:
        s = sugPopularList[userSugPopularRank[0]]
        value = str(getSuggestionPopularity(s)) + ' Comments/Ratings' 
        title = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
    addRanks('Suggestion Popularity', 'sugPopular', userSugPopularRank, len(sugPopularList), title, value) 

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Ratings', 'Average Rating'] 
        rows = [] 
        count = 1 
        
        for s in sugPopularList:
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            totalComs = getDiscussionByID(int(s['discussion_id']))['numComments']
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
            
            row.append(count) 
            row.append(name) 
            row.append(totalComs) 
            row.append(numRatings) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Suggestion Popularity', 'sugPopular', headers, rows) 
    
    if page == 'userRanks' and userSugPopularRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Ratings', 'Average Rating'] 
        rows = [] 
        
        for index in userSugPopularRank:
            s = sugPopularList[index]
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            totalComs = getDiscussionByID(int(s['discussion_id']))['numComments']
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
            
            row.append(str(index+1) + ' / ' + str(len(sugPopularList))) 
            row.append(name) 
            row.append(totalComs) 
            row.append(numRatings) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            
        addBoardDict('Suggestion Popularity', 'sugPopular', headers, rows) 

"Best Suggestion Rating LeaderBoard"
def SugRatingBoard(page, suggestions):
    
    "Sorted By Rating (Avg of all slider bar ratings)"
    sugRatingList = sorted(suggestions, key=lambda x: float(x['ratingAvg_%s' % 'overall']), reverse = True)

    userSugRatingRank = [i for i,x in enumerate(sugRatingList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userSugRatingRank != []:
        s = sugRatingList[userSugRatingRank[0]]
        value = str(int(s['ratingAvg_%s' % 'overall'])) + ' Average Rating' 
        title = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
    addRanks('Suggestion Rating', 'sugRating', userSugRatingRank, len(sugRatingList), title, value) 
    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Ratings', 'You Rated', 'Average Rating'] 
        rows = [] 
        count = 1  
           
        for s in sugRatingList:
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            userRate = '-' 
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall'])) 
                if s.id in sugRateDict.keys():
                    userRate = getRatingByID(sugRateDict[s.id])['rating']

            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
    
            row.append(count) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userRate) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Suggestion Rating', 'sugRating', headers, rows) 

    if page == 'userRanks' and userSugRatingRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Ratings', 'You Rated', 'Average Rating'] 
        rows = [] 
           
        for index in userSugRatingRank:
            s = sugRatingList[index]
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            userRate = '-' 
            if 'ratedThings_suggestion_overall' in c.authuser.keys():
                sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall'])) 
                if s.id in sugRateDict.keys():
                    userRate = getRatingByID(sugRateDict[s.id])['rating']

            fuzzUpperAvgRating = int((float(s['ratingAvg_overall'])) + (5-(float(s['ratingAvg_overall']))%5))
            fuzzLowerAvgRating = int((float(s['ratingAvg_overall'])) - ((float(s['ratingAvg_overall']))%5))
    
            row.append(str(index+1) + ' / ' + str(len(sugRatingList))) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userRate) 
            row.append(str(fuzzLowerAvgRating) + " - " + str(fuzzUpperAvgRating))
            
            rows.append(row) 
            
        addBoardDict('Suggestion Rating', 'sugRating', headers, rows) 
        
        
def ResRatingBoard(page, resources):

    "Sorted by Ratings : ups/(ups + downs)"
    resRatingList = sorted(resources, key=lambda x: 0 if (int(x['ups'])+int(x['downs']) ==0) else (float(x['ups'])/(float(x['ups'])+float(x['downs']))), reverse = True)

    userResRatingRank = [i for i,x in enumerate(resRatingList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userResRatingRank != []:
        r = resRatingList[userResRatingRank[0]]
        PercentRating = '--'
        if int(r['ups']) > 0 or int(r['downs']) > 0:    
            PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
        value = str(PercentRating) + ' Average Rating' 
        title = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
    addRanks('Resource Rating', 'resRating', userResRatingRank, len(resRatingList), title, value) 
 

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1     

        for r in resRatingList:
            row = [] 
            count = 1 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Resource Rating', 'resRating', headers, rows) 

    if page == 'userRanks' and userResRatingRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 

        for index in userResRatingRank:
            r = resRatingList[index]
            row = [] 
            count = 1 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append(str(index+1) + ' / ' + str(len(resRatingList))) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Resource Rating', 'resRating', headers, rows) 


" Get Resource Popularity through number of comments and votes for each comment "
def getResourcePopularity(disc):
    popularity = 0
    if 'children' in disc.keys():
        for comID in disc['children'].split(','):
            nextCom = getComment(int(comID))
            if nextCom:
                popularity += 1 + int(nextCom['ups']) + int(nextCom['downs']) + getResourcePopularity(nextCom)
    return popularity

def ResPopularityBoard(page, resources):

    "Sorted by comments + rating votes"
    resPopularList = sorted(resources, key=lambda x: (getResourcePopularity(getDiscussionByID(x['discussion_id'])) + int(x['ups']) + int(x['downs'])), reverse = True)

    userResPopularRank = [i for i,x in enumerate(resPopularList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userResPopularRank != []:
        r = resPopularList[userResPopularRank[0]]
        value = str(getResourcePopularity(getDiscussionByID(r['discussion_id']))) + ' Comments/Ratings' 
        title = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
    addRanks('Resource Popularity', 'resPopular', userResPopularRank, len(resPopularList), title, value) 

    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
        count = 1 
                
        for r in resPopularList:
            row = [] 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            totalComs = getDiscussionByID(int(r['discussion_id']))['numComments']
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(totalComs)
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Resource Popularity', 'resPopular', headers, rows) 

    if page == 'userRanks' and userResPopularRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
                
        for index in userResPopularRank:
            r = resPopularList[index]
            row = [] 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            totalComs = getDiscussionByID(int(r['discussion_id']))['numComments']
            userVote = '--' 
            if 'ratedThings_resource_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if r.id in resRateDict.keys():
                    userVote = getRatingByID(resRateDict[r.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(r['ups']) > 0 or int(r['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(r['ups'])+int(r['downs'])))*100)/5))
            
            row.append(str(index+1) + ' / ' + str(len(resPopularList))) 
            row.append(name) 
            row.append(totalComs)
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            
        addBoardDict('Resource Popularity', 'resPopular', headers, rows) 
    
def DiscRatingBoard(page, discussions):

    "Sorted by Ratings : ups/(ups + downs)"
    discRatingList = sorted(discussions, key=lambda x: 0 if (int(x['ups'])+int(x['downs']) ==0) else (float(x['ups'])/(float(x['ups'])+float(x['downs']))), reverse = True)

    userDiscRatingRank = [i for i,x in enumerate(discRatingList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userDiscRatingRank != []:
        d = discRatingList[userDiscRatingRank[0]]
        PercentRating = '--'
        if int(d['ups']) > 0 or int(d['downs']) > 0:    
            PercentRating = int(5*round(((int(d['ups'])/(int(d['ups'])+int(d['downs'])))*100)/5))
        value = str(PercentRating) + ' Average Rating' 
        title = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + d['urlCode'] + '/' + d['url'])] 
    addRanks('Discussion Rating', 'discRating', userDiscRatingRank, len(discRatingList), title, value) 
 

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1     

        for d in discRatingList:
            row = [] 
            count = 1 
            name = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/discussion/' + d['urlCode'] + '/' + d['url'])] 
            numRatings = int(d['ups']) + int(d['downs'])
            userVote = '--' 
            if 'ratedThings_discussion_overall' in c.authuser.keys():
                discRateDict = pickle.loads(str(c.authuser['ratedThings_discussion_overall'])) 
                if d.id in discRateDict.keys():
                    userVote = getRatingByID(discRateDict[d.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(d['ups']) > 0 or int(d['downs']) > 0:    
                PercentRating = int(5*round(((int(d['ups'])/(int(d['ups'])+int(d['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Discussion Rating', 'discRating', headers, rows) 

    if page == 'userRanks' and userDiscRatingRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 

        for index in userDiscRatingRank:
            d = discRatingList[index]
            row = [] 
            count = 1 
            name = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/discussion/' + d['urlCode'] + '/' + d['url'])] 
            numRatings = int(d['ups']) + int(d['downs'])
            userVote = '--' 
            if 'ratedThings_discussion_overall' in c.authuser.keys():
                resRateDict = pickle.loads(str(c.authuser['ratedThings_discussion_overall'])) 
                if d.id in discRateDict.keys():
                    userVote = getRatingByID(discRateDict[d.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(d['ups']) > 0 or int(d['downs']) > 0:    
                PercentRating = int(5*round(((int(r['ups'])/(int(d['ups'])+int(d['downs'])))*100)/5))
            
            row.append(str(index+1) + ' / ' + str(len(discRatingList))) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Discussion Rating', 'discRating', headers, rows) 


" Get Resource Popularity through number of comments and votes for each comment "
def getDiscussionPopularity(disc):
    popularity = 0
    if 'children' in disc.keys():
        for comID in disc['children'].split(','):
            nextCom = getComment(int(comID))
            if nextCom:
                popularity += 1 + int(nextCom['ups']) + int(nextCom['downs']) + getDiscussionPopularity(nextCom)
    return popularity

def DiscPopularityBoard(page, discussions):

    "Sorted by comments + rating votes"
    discPopularList = sorted(discussions, key=lambda x: (getDiscussionPopularity(x) + int(x['ups']) + int(x['downs'])), reverse = True)

    userDiscPopularRank = [i for i,x in enumerate(discPopularList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userDiscPopularRank != []:
        d = discPopularList[userDiscPopularRank[0]]
        value = str(getDiscussionPopularity(d)) + ' Comments/Ratings' 
        title = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/discussion/' + d['urlCode'] + '/' + d['url'])] 
    addRanks('Discussion Popularity', 'discPopular', userDiscPopularRank, len(discPopularList), title, value) 

    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
        count = 1 
                
        for d in discPopularList:
            row = [] 
            name = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/discussion/' + d['urlCode'] + '/' + d['url'])] 
            numRatings = int(d['ups']) + int(d['downs'])
            totalComs = d['numComments']
            userVote = '--' 
            if 'ratedThings_discussion_overall' in c.authuser.keys():
                discRateDict = pickle.loads(str(c.authuser['ratedThings_discussion_overall'])) 
                if d.id in discRateDict.keys():
                    userVote = getRatingByID(discRateDict[d.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(d['ups']) > 0 or int(d['downs']) > 0:    
                PercentRating = int(5*round(((int(d['ups'])/(int(d['ups'])+int(d['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(totalComs)
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Discussion Popularity', 'discPopular', headers, rows) 

    if page == 'userRanks' and userDiscPopularRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Title', 'Total Comments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
                
        for index in userDiscPopularRank:
            d = discPopularList[index]
            row = [] 
            name = [d['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/discussion/' + d['urlCode'] + '/' + d['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            totalComs = d['numComments']
            userVote = '--' 
            if 'ratedThings_discussion_overall' in c.authuser.keys():
                discRateDict = pickle.loads(str(c.authuser['ratedThings_discussion_overall'])) 
                if d.id in discRateDict.keys():
                    userVote = getRatingByID(discRateDict[d.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(d['ups']) > 0 or int(d['downs']) > 0:    
                PercentRating = int(5*round(((int(d['ups'])/(int(d['ups'])+int(d['downs'])))*100)/5))
            
            row.append(str(index+1) + ' / ' + str(len(discPopularList))) 
            row.append(name) 
            row.append(totalComs)
            row.append(numRatings) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            
        addBoardDict('Discussion Popularity', 'discPopular', headers, rows) 
        
    
def CommentRatingBoard(page, comList):

    " Sorted by Ratings : ups/(ups + downs) "
    comRatingList = sorted(comList, key=lambda x: 0 if (int(x['ups'])+int(x['downs']) ==0) else (float(x['ups'])/(float(x['ups'])+float(x['downs']))), reverse = True)

    userComRatingRank = [i for i,x in enumerate(comRatingList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userComRatingRank != []:
        com = comRatingList[userComRatingRank[0]]
        PercentRating = '--'
        if int(com['ups']) > 0 or int(com['downs']) > 0:    
            PercentRating = int(5*round(((int(com['ups'])/(int(com['ups'])+int(com['downs'])))*100)/5))
        value = str(PercentRating) + ' Average Rating' 
        
        Disc = getDiscussionByID(int(com['discussion_id']))
        href = ''
        if Disc['discType'] == 'suggestion':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
        elif Disc['discType'] == 'resource':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
        elif Disc['discType'] == 'feedback':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
        title = [com['data'][:15], href] 
        
    addRanks('Comment Rating', 'comRating', userComRatingRank, len(comRatingList), title, value) 

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Entry', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1 
    
        for com in comRatingList:
            row = [] 
            
            Disc = getDiscussionByID(int(com['discussion_id']))
            href = ''
            if Disc['discType'] == 'suggestion':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
            elif Disc['discType'] == 'resource':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
            elif Disc['discType'] == 'feedback':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
            
            name = [com['data'][:15], href] 
            
            numVotes = int(com['ups']) + int(com['downs'])
            userVote = '--' 
            if 'ratedThings_comment_overall' in c.authuser.keys():
                comRateDict = pickle.loads(str(c.authuser['ratedThings_comment_overall'])) 
                if com.id in comRateDict.keys():
                    userVote = getRatingByID(comRateDict[com.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(com['ups']) > 0 or int(com['downs']) > 0:    
                PercentRating = int(5*round(((int(com['ups'])/(int(com['ups'])+int(com['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(numVotes) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Comment Rating', 'comRating', headers, rows) 

    if page == 'userRanks' and userComRatingRank !=[]:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Entry', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1 
    
        for index in userComRatingRank:
            com = comRatingList[index]
            row = [] 
            
            Disc = getDiscussionByID(int(com['discussion_id']))
            href = ''
            if Disc['discType'] == 'suggestion':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
            elif Disc['discType'] == 'resource':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
            elif Disc['discType'] == 'feedback':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
            
            name = [com['data'][:15], href] 
            
            numVotes = int(com['ups']) + int(com['downs'])
            userVote = '--' 
            if 'ratedThings_comment_overall' in c.authuser.keys():
                comRateDict = pickle.loads(str(c.authuser['ratedThings_comment_overall'])) 
                if com.id in comRateDict.keys():
                    userVote = getRatingByID(comRateDict[com.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(com['ups']) > 0 or int(com['downs']) > 0:    
                PercentRating = int(5*round(((int(com['ups'])/(int(com['ups'])+int(com['downs'])))*100)/5))
            
            row.append(str(index+1) + ' / ' + str(len(comRatingList))) 
            row.append(name) 
            row.append(numVotes) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            
        addBoardDict('Comment Rating', 'comRating', headers, rows) 


def getCommentPopularity(com):
    children = 0
    children += int(com['ups']) + int(com['downs'])
    if 'children' in com.keys():
        for comID in com['children'].split(','):
            nextCom = getComment(int(comID))
            if nextCom:
                children += 1 + getCommentPopularity(nextCom)
    return children

def getSubComments(com):
    children = 0
    if 'children' in com.keys():
        for comID in com['children'].split(','):
            nextCom = getComment(int(comID))
            if nextCom:
                children += 1 + getSubComments(nextCom)
    return children

def CommentPopularityBoard(page, comList):

    " Sorted by comment children + rating votes "
    comPopularList = sorted(comList, key=lambda x: getCommentPopularity(x), reverse = True)
    
    userComPopularRank = [i for i,x in enumerate(comPopularList) if x.owner == c.authuser.id]
    value = '--'
    title = '--'
    if userComPopularRank != []:
        com = comPopularList[userComPopularRank[0]]
        value = str(getCommentPopularity(com)) + ' SubComments/Ratings'    
                 
        Disc = getDiscussionByID(int(com['discussion_id']))
        href = ''
        if Disc['discType'] == 'suggestion':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
        elif Disc['discType'] == 'resource':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
        elif Disc['discType'] == 'feedback':
            href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
            
        title = [com['data'][:15], href] 
    
    addRanks('Comment Popularity', 'comPopular', userComPopularRank, len(comPopularList), title, value) 

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Entry', 'Total SubComments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
        count = 1 
        
        for com in comPopularList:
            row = [] 

            Disc = getDiscussionByID(int(com['discussion_id']))
            href = ''
            if Disc['discType'] == 'suggestion':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
            elif Disc['discType'] == 'resource':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
            elif Disc['discType'] == 'feedback':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
                
            name = [com['data'][:15], href] 
            
            numVotes = int(com['ups']) + int(com['downs'])
            totalComs = getSubComments(com)
            userVote = '--' 
            if 'ratedThings_comment_overall' in c.authuser.keys():
                comRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if com.id in comRateDict.keys():
                    userVote = getRatingByID(comRateDict[com.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(com['ups']) > 0 or int(com['downs']) > 0:    
                PercentRating = int(5*round(((int(com['ups'])/(int(com['ups'])+int(com['downs'])))*100)/5))
            
            row.append(count) 
            row.append(name) 
            row.append(totalComs)
            row.append(numVotes) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Comment Popularity', 'comPopular', headers, rows) 

    if page == 'userRanks' and userComPopularRank != []:
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Entry', 'Total SubComments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
        count = 1 
        
        for index in userComPopularRank:
            com = comPopularList[index]
            row = [] 

            Disc = getDiscussionByID(int(com['discussion_id']))
            href = ''
            if Disc['discType'] == 'suggestion':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + Disc['suggestionCode'] + '/' + Disc['suggestionURL']
            elif Disc['discType'] == 'resource':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + Disc['resourceCode'] + '/' + Disc['resourceURL']
            elif Disc['discType'] == 'feedback':
                href = '/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/feedback'
                
            name = [com['data'][:15], href] 
            
            numVotes = int(com['ups']) + int(com['downs'])
            totalComs = getSubComments(com)
            userVote = '--' 
            if 'ratedThings_comment_overall' in c.authuser.keys():
                comRateDict = pickle.loads(str(c.authuser['ratedThings_resource_overall'])) 
                if com.id in comRateDict.keys():
                    userVote = getRatingByID(comRateDict[com.id])['rating']
                if userVote == '1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png'}
                elif userVote == '-1':
                    userVote = {'img': '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png'}

            PercentRating = '--'
            if int(com['ups']) > 0 or int(com['downs']) > 0:    
                PercentRating = int(5*round(((int(com['ups'])/(int(com['ups'])+int(com['downs'])))*100)/5))
            
            row.append(str(index) + ' / ' + str(len(comPopularList))) 
            row.append(name) 
            row.append(totalComs)
            row.append(numVotes) 
            row.append(userVote) 
            row.append(PercentRating)
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Comment Popularity', 'comPopular', headers, rows) 

"User Most Followers leaderboard"
def peoplefollowsBoard(page, userList):

    followList = sorted(userList, key=lambda x: len(getUserFollows(x.id)), reverse = True)

    "Adding to the User's leaderboard"
    userFollowerRank = [i for i,x in enumerate(followList) if x.id == c.authuser.id]
    value = '--'
    title = '--'
    if userFollowerRank != []:
        value = str(len(getUserFollows(followList[userFollowerRank[0]].id))) + ' Followers' 
        title = [c.authuser['name'], ('/profile/' + c.authuser['urlCode'] + '/' + c.authuser['url'])]
    addRanks('Followers', 'Followers', userFollowerRank, len(followList), title, value) 

    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', ['icon-user', 'Name'], 'Total Followers', 'Following'] 
        rows = [] 
        count = 1 
        
        for user in followList:
            row = [] 
            picture = ''
            if user['pictureHash'] == 'flash':
                picture = "/images/avatars/flash.profile"
            else:
                picture = '/images/avatar/' + user['directoryNumber'] + '/profile/' + user['pictureHash'] + '.profile'


            name = [[picture, user['name']], ('/profile/' + user['urlCode'] + '/' + user['url'])] 
            numFollowers = len(getUserFollows(user.id)) 
            following = 'No' 
            if int(user.id) == int(c.authuser.id):
                following = '--' 
            elif isFollowing(c.authuser.id, user.id):
                following = 'Yes'
    
            row.append(count) 
            row.append(name) 
            row.append(numFollowers) 
            row.append(following) 
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Followers', 'Followers', headers, rows)
        
        
def UserWorkshopInput(user, sugs, res, coms):
    input = 0;
    for s in sugs:
        if s.owner == user.id:
            input+= 1
    for r in res:
        if r.owner == user.id:
            input+= 1
    for com in coms:
        if com.owner == user.id:
            input+= 1
    return input

"Board for Your Followed Persons Main Stats"
def followedPersonsBoard(sugs, res, coms):

    follows = getUserFollows(c.authuser.id)
    usersfollowing = []
    for follow in follows:
        usersfollowing.append(getUserByID(follow['thingID']))

    followed = sorted(usersfollowing, key=lambda x:(UserWorkshopInput(x, sugs, res, coms)), reverse = True)
    
    "Setting up LeaderBoard Dictionary Addition"
    headers = [['icon-user', 'Name'], 'Total Followers', 'Total Suggestions', 'Total Resources', 'Total Comments'] 
    rows = [] 
    count = 1

    for user in followed:
        row = [] 
        name = [user['name'], ('/profile/' + user['urlCode'] + '/' + user['url'])] 
        numFollowers = len(getUserFollows(user.id)) 

        numSugs = 0
        for s in sugs:
            if s.owner == user.id:
                numSugs+= 1
        numRes = 0
        for r in res:
            if r.owner == user.id:
                numRes+= 1
        numComs = 0
        for com in coms:
            if com.owner == user.id:
                numComs+= 1

        row.append(name) 
        row.append(numFollowers) 
        row.append(numSugs) 
        row.append(numRes) 
        row.append(numComs) 
        
        rows.append(row) 
        count += 1 
        
    addBoardDict('Followed Persons Listing', 'peoplefollowed', headers, rows) 

def myRankingsBoard(sugs, res, coms):

    return ""
    
"Adding Dictionary to the leaderboard List of Boards"
def addBoardDict(title, hrefKey, headers, rows):

    boardDict = {'title':title} 
    boardDict['hrefKey'] = hrefKey 
    boardDict['headers'] = headers 
    boardDict['tablebody'] = rows 
    c.leaderboardList.append(boardDict) 


"Takes in the Listing key(title), the List containing the userRanking, and the originalList"
def addRanks(category, key, userRanks, origListLength, title, value):
            
    RankList = [category, ('#'+key)] 
    
    if userRanks == []:
        userRanks = '-' 
    else:
        userRanks = userRanks[0] + 1 

    RankList.append(str(userRanks) + ' / ' + (str(origListLength))) 
    RankList.append(title)
    RankList.append(str(value)) 
    
    "List contain title as [0] and then a List of stuff related to the Leaderboard"
    "The list contains [user ranking]"
    if c.userRankings:
        c.userRankings.append(RankList) 
    else:
        c.userRankings = [RankList] 
        
" Recursively gets all comments "
def getCommentList(disc):
    comList = []
    if 'children' in disc.keys():
        for comID in disc['children'].split(','):
            nextCom = getComment(int(comID))
            if nextCom:
                comList.append(nextCom)
                comList += getCommentList(nextCom)
    return comList        

"Takes in the controller method name for further analysis for computing/adding to c"
def GenerateRanks(code, url, page):

    c.w = getWorkshop(code, url) 

    c.leaderboardList = [] 
    
    # Grabbing all Active users
    userList = []
    userList = getActiveUsers()
    # Grabbing the Resources of the Workshop
    c.resList = getActiveResourcesByWorkshopID(c.w.id)
    # Grabbing the Suggestions of the Workshop
    c.suggestions = getActiveSuggestionsForWorkshop(code, url) 
    # Grabbing the Discussions of the Workshop
    c.discList = getActiveDiscussionsForWorkshop(code, url) 
    
    peoplefollowsBoard(page, userList) 
    
    SugRatingBoard(page, c.suggestions) 
    SugPopularityBoard(page, c.suggestions) 
    SugActivityBoard(page, c.suggestions)

    ResRatingBoard(page, c.resList)
    ResPopularityBoard(page, c.resList)
    ResActivityBoard(page, c.resList)

    DiscRatingBoard(page, c.discList)
    DiscPopularityBoard(page, c.discList)
    
    c.comList = []
    " Grabbing the Comments of the Workshop "
    " First build up the comList Using the Workshop general comments + all the suggestions comments + resource comments"
    Disc = getDiscussionByID(int(c.w['feedbackDiscussion_id'])) 
    c.comList += getCommentList(Disc) 
    for sug in c.suggestions:
        Disc = getDiscussionByID(int(sug['discussion_id'])) 
        c.comList += getCommentList(Disc)
    for res in c.resList:
        Disc = getDiscussionByID(int(res['discussion_id']))
        c.comList += getCommentList(Disc)
        
    CommentRatingBoard(page, c.comList)
    CommentPopularityBoard(page, c.comList)
    
def addexplanation(title, explanation):
    ExplainedBoard = [title, explanation]
    c.Explain.append(ExplainedBoard)
    
class LeaderboardController(BaseController):

    """ Renders the leaderboard page for a given workshop.  Takes in the issue URL as the id argument. """
    #@h.login_required
    def index(self, id1, id2):
        
        GenerateRanks(id1, id2, 'index')
        
        c.mainLeaderboard = 'yes'
        
        return render('/derived/leaderboard.bootstrap')


    def explain(self, id1, id2):
        
        code = id1
        url = id2
        c.w = getWorkshop(code, url)
        
        "Putting all leaderboard title with explanation as list into a list"
        c.Explain = []
        
        explanation = "The Overall Leaderboard Ranking list shows your best ranking for each category on the main leaderboard page of that workshop"
        addexplanation('Overall Rankings', explanation)
        explanation = "The Follows list is ranked by number of followers a user has, most to least"
        addexplanation('Follows', explanation)
        explanation = "Ranked by best average Suggestion Rating (total ratings sum/total ratings)"
        addexplanation('Suggestion Rating', explanation)   
        explanation = "Ranked by number of comments plus number of ratings recieved on that suggestions"
        addexplanation('Suggestion Popularity', explanation)
        explanation = "Ranked by number of comments and rating over the duration of time the suggestion has existed"
        addexplanation('Suggestion Activity', explanation)
        explanation = "Ranked by number of up votes versus number of up plus down votes on the resource"
        addexplanation('Resource Rating', explanation)
        explanation = "Ranked by Comments plus Votes on the resource"
        addexplanation('Resource Popularity', explanation)
        explanation = "Ranked by number of comments and rating over the duration of time the resource has existed"
        addexplanation('Resource Activity', explanation)
        explanation = "Ranked by number of up votes versus number of up plus down votes on the discussion"
        addexplanation('Discussion Rating', explanation)
        explanation = "Ranked by Comments plus Votes on the discussion"
        addexplanation('Discussion Popularity', explanation)
        explanation = "Ranked by number of up votes versus number of up plus down votes for the comment"
        addexplanation('Comment Rating', explanation)
        explanation = "Ranked by number of SubComments to a comment as well as votes on the comment"
        addexplanation('Comment Popularity', explanation)
        explanation = "List of your followed Person with that person's total numbers of input"
        addexplanation('Followed Persons Listing', explanation)
                                
        return render('/derived/leaderboard_explanation.bootstrap')
    
    def followedPersons(self, id1, id2):
        
        GenerateRanks(id1, id2, 'followedPersons')
        
        followedPersonsBoard(c.suggestions, c.resList, c.comList) 
        return render('/derived/leaderboard_followedPersons.bootstrap')

    def UserRankings(self, id1, id2):
        
        GenerateRanks(id1, id2, 'userRanks')
        
        myRankingsBoard(c.suggestions, c.resList, c.comList) 
        return render('/derived/leaderboard_UserRanks.bootstrap')