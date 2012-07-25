import logging, datetime, time, pickle

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylowiki.lib.db.suggestion import getActiveSuggestionsForWorkshop
from pylowiki.lib.db.workshop import getWorkshop
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.comment import getComment
from pylowiki.lib.db.resource import getActiveResourcesByWorkshopID
from pylowiki.lib.db.follow import getUserFollows, isFollowing
from pylowiki.lib.db.user import getActiveUsers, getUserByID
from pylowiki.lib.db.rating import getRatingByID

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

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total Comments', 'Total Ratings', 'Average Rating'] 
        rows = [] 
        count = 1 
        
        for s in sugPopularList:
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            totalComs = getDiscussionByID(int(s['discussion_id']))['numComments']
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            
            row.append(count) 
            row.append(name) 
            row.append(totalComs) 
            row.append(numRatings) 
            row.append(s['ratingAvg_overall'])
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Suggestion Popularity', 'sugPopular', headers, rows) 
    

    userSugPopularRank = [i for i,x in enumerate(sugPopularList) if x.owner == c.authuser.id]
    value = '-'
    if userSugPopularRank != []:
        value = str(getSuggestionPopularity(sugPopularList[userSugPopularRank[0]])) + ' Comments/Ratings' 
    addRanks('Suggestion Popularity', 'sugPopular', userSugPopularRank, len(sugPopularList), value) 

"Best Suggestion Rating LeaderBoard"
def SugRatingBoard(page, suggestions):
    
    "Sorted By Rating (Avg of all slider bar ratings)"
    sugRatingList = sorted(suggestions, key=lambda x: float(x['ratingAvg_%s' % 'overall']), reverse = True)
    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total Ratings', 'You Rated', 'Average Rating'] 
        rows = [] 
        count = 1  
           
        for s in sugRatingList:
            row = [] 
            name = [s['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/suggestion/' + s['urlCode'] + '/' + s['url'])] 
            numRatings = len(s['ratingIDs_overall'].split(',')) 
            userRate = '-' 
            sugRateDict = pickle.loads(str(c.authuser['ratedThings_suggestion_overall'])) 
            if s.id in sugRateDict.keys():
                userRate = getRatingByID(sugRateDict[s.id])['rating']
    
            row.append(count) 
            row.append(name) 
            row.append(numRatings) 
            row.append(userRate) 
            row.append(s['ratingAvg_overall'])
            
            rows.append(row) 
            count += 1 
            
        addBoardDict('Suggestion Rating', 'sugRating', headers, rows) 

    
    userSugRatingRank = [i for i,x in enumerate(sugRatingList) if x.owner == c.authuser.id]
    value = '-'
    if userSugRatingRank != []:
        value = str(sugRatingList[userSugRatingRank[0]]['ratingAvg_%s' % 'overall']) + ' Average Rating' 
    addRanks('Suggestion Rating', 'sugRating', userSugRatingRank, len(sugRatingList), value) 

def ResRatingBoard(page, resources):

    "Sorted by Ratings : ups/(ups + downs)"
    resRatingList = sorted(resources, key=lambda x: 0 if (int(x['ups'])+int(x['downs']) ==0) else (float(x['ups'])/(float(x['ups'])+float(x['downs']))), reverse = True)
 
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total Votes', 'You Rated', 'Overall Rating'] 
        rows = [] 
        count = 1     

        for r in resRatingList:
            row = [] 
            count = 1 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            userVote = '--' 
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

    
    userResRatingRank = [i for i,x in enumerate(resRatingList) if x.owner == c.authuser.id]
    value = '-'
    if userResRatingRank != []:
        PercentRating = '--'
        if int(resRatingList[userResRatingRank[0]]['ups']) > 0 or int(resRatingList[userResRatingRank[0]]['downs']) > 0:    
            PercentRating = int(5*round(((int(resRatingList[userResRatingRank[0]]['ups'])/(int(resRatingList[userResRatingRank[0]]['ups'])+int(resRatingList[userResRatingRank[0]]['downs'])))*100)/5))
        value = str(PercentRating) + ' Average Rating' 
    addRanks('Resource Rating', 'resRating', userResRatingRank, len(resRatingList), value) 

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

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total Comments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
        rows = [] 
        count = 1 
                
        for r in resPopularList:
            row = [] 
            count = 1 
            name = [r['title'], ('/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/resource/' + r['urlCode'] + '/' + r['url'])] 
            numRatings = int(r['ups']) + int(r['downs'])
            totalComs = getDiscussionByID(int(r['discussion_id']))['numComments']
            userVote = '--' 
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
    

    userResPopularRank = [i for i,x in enumerate(resPopularList) if x.owner == c.authuser.id]
    value = '-'
    if userResPopularRank != []:
        value = str(getResourcePopularity(getDiscussionByID(resPopularList[userResPopularRank[0]]['discussion_id']))) + ' Comments/Ratings' 
    addRanks('Resource Popularity', 'resPopular', userResPopularRank, len(resPopularList), value) 

def CommentRatingBoard(page, comList):

    " Sorted by Ratings : ups/(ups + downs) "
    comRatingList = sorted(comList, key=lambda x: 0 if (int(x['ups'])+int(x['downs']) ==0) else (float(x['ups'])/(float(x['ups'])+float(x['downs']))), reverse = True)

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total Votes', 'You Rated', 'Overall Rating'] 
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

    
    userComRatingRank = [i for i,x in enumerate(comRatingList) if x.owner == c.authuser.id]
    value = '-'
    if userComRatingRank != []:
        PercentRating = '--'
        if int(comRatingList[userComRatingRank[0]]['ups']) > 0 or int(comRatingList[userComRatingRank[0]]['downs']) > 0:    
            PercentRating = int(5*round(((int(comRatingList[userComRatingRank[0]]['ups'])/(int(comRatingList[userComRatingRank[0]]['ups'])+int(comRatingList[userComRatingRank[0]]['downs'])))*100)/5))
        value = str(PercentRating) + ' Average Rating' 
    addRanks('Comment Rating', 'comRating', userComRatingRank, len(comRatingList), value) 

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

    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', 'Name', 'Total SubComments', 'Total Votes', 'Your Vote', 'Overall Rating'] 
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
    

    userComPopularRank = [i for i,x in enumerate(comPopularList) if x.owner == c.authuser.id]
    value = '-'
    if userComPopularRank != []:
        value = str(getCommentPopularity(comPopularList[userComPopularRank[0]])) + ' SubComments/Ratings' 
    addRanks('Comment Popularity', 'comPopular', userComPopularRank, len(comPopularList), value) 

"User Most Followers leaderboard"
def peoplefollowsBoard(page, userList):

    followList = sorted(userList, key=lambda x: len(getUserFollows(x.id)), reverse = True)
    
    if page == 'index':
        "Setting up LeaderBoard Dictionary Addition"
        headers = ['Rank', ['icon-user', 'Name'], 'Total Followers', 'Followed'] 
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
        
    
    "Adding to the User's leaderboard"
    userFollowerRank = [i for i,x in enumerate(followList) if x.id == c.authuser.id]
    value = '-'
    if userFollowerRank != []:
        value = str(len(getUserFollows(followList[userFollowerRank[0]].id))) + ' Followers' 
    addRanks('Followers', 'Followers', userFollowerRank, len(followList), value) 

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

def GenerateLists(code, url):
    
    # Sorted By most Activity
    c.sugActiveList = sorted(suggestions, key=lambda x: MostActiveSuggestions(x))

    # Grabbing the Resources of the Workshop
    c.resActiveList = sorted(resList, key=lambda x: MostActiveResource(x))
    
    c.comLengthList = sorted(comList, key=lambda x: len(x['data']), reverse = True)
    
"Adding Dictionary to the leaderboard List of Boards"
def addBoardDict(title, hrefKey, headers, rows):

    boardDict = {'title':title} 
    boardDict['hrefKey'] = hrefKey 
    boardDict['headers'] = headers 
    boardDict['tablebody'] = rows 
    c.leaderboardList.append(boardDict) 


"Takes in the Listing key(title), the List containing the userRanking, and the originalList"
def addRanks(title, key, userRanks, origListLength, value):
    
    RankList = [title, ('#'+key)] 
    
    if userRanks == []:
        userRanks = '-' 
    else:
        userRanks = userRanks[0] + 1 

    RankList.append(str(userRanks) + ' / ' + (str(origListLength))) 
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
    peoplefollowsBoard(page, userList) 
    
    c.suggestions = []
    # Grabbing the Suggestions of the Workshop
    c.suggestions = getActiveSuggestionsForWorkshop(code, url) 
    SugRatingBoard(page, c.suggestions) 
    SugPopularityBoard(page, c.suggestions) 

    c.resList = []
    # Grabbing the Resources of the Workshop
    c.resList = getActiveResourcesByWorkshopID(c.w.id)
    ResRatingBoard(page, c.resList)
    ResPopularityBoard(page, c.resList)

    c.comList = []
    
    " Grabbing the Comments of the Workshop "
    " First build up the comList Using the Workshop general comments + all the suggestions comments "
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
    
def addExplaination(title, explaination):
    ExplainedBoard = [title, explaination]
    c.Explain.append(ExplainedBoard)
    
class LeaderboardController(BaseController):

    """ Renders the leaderboard page for a given workshop.  Takes in the issue URL as the id argument. """
    #@h.login_required
    def index(self, id1, id2):
        
        GenerateRanks(id1, id2, 'index')
        
        return render('/derived/leaderboard.bootstrap')


    def explain(self, id1, id2):
        
        code = id1
        url = id2
        c.w = getWorkshop(code, url)
        
        "Putting all leaderboard title with explaination as list into a list"
        c.Explain = []
        
        explaination = "The Overall Leaderboard Ranking list shows your best ranking for each category on the main leaderboard page of that workshop"
        addExplaination('Overall Rankings', explaination)
        explaination = "The Follows list is ranked by number of followers a user has, most to least"
        addExplaination('Follows', explaination)
        explaination = "Ranked by best average Suggestion Rating (total ratings sum/total ratings)"
        addExplaination('Suggestion Rating', explaination)   
        explaination = "Ranked by number of comments plus number of ratings recieved on that suggestions"
        addExplaination('Suggestion Popularity', explaination)
        explaination = "Ranked by number of up votes versus number of up plus down votes on the resource"
        addExplaination('Resource Rating', explaination)
        explaination = "Ranked by Comments plus Votes on the resource"
        addExplaination('Resource Popularity', explaination)
        explaination = "Ranked by number of up votes versus number of up plus down votes"
        addExplaination('Comment Rating', explaination)
        explaination = "Ranked by number of SubComments to a comment as well as votes on the comment"
        addExplaination('Comment Popularity', explaination)
        explaination = "List of your followed Person with that person's total numbers of input"
        addExplaination('Followed Persons Listing', explaination)
                                
        return render('/derived/leaderboard_explaination.bootstrap')
    
    def followedPersons(self, id1, id2):
        
        GenerateRanks(id1, id2, 'other')
        
        followedPersonsBoard(c.suggestions, c.resList, c.comList) 
        return render('/derived/leaderboard_followedPersons.bootstrap')
