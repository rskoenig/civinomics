from pylons import request, response, session, tmpl_context as c, url, config
import pylowiki.lib.db.discussion 		as discussionLib
import pylowiki.lib.db.comment 			as commentLib
import pylowiki.lib.db.user         	as userLib
import pylowiki.lib.utils				as utils
import pylowiki.lib.fuzzyTime			as fuzzyTime
import misaka as m

def jsonifyAnyObj(list):
	myRatings = {}
	if 'ratings' in session:
		myRatings = session['ratings']

	result = []

	for item in list:
		entry = {}
		# item attributes
		entry['title'] = ''
		if 'title' in item:
			entry['title'] = item['title']
		entry['objType'] = item.objType
		if item.objType == 'discussion':
			if item['discType'] == 'update':
				entry['objType'] = 'update'
		entry['urlCode'] = item['urlCode']
		entry['url'] = ''
		if 'url' in item:
			entry['url'] = item['url']
		entry['date'] = item.date.strftime('%Y-%m-%d at %H:%M:%S')
		entry['fuzzyTime'] = fuzzyTime.timeSince(item.date)
		if 'views' in item:
			entry['views'] = str(item['views'])
		else:
			entry['views'] = '0'

		# attributes that vary accross items
		entry['text'] = '0'
		if 'text' in item:
			entry['text'] = item['text']
		elif 'description' in item:
			entry['text'] = item['description']
		entry['html'] = m.html(entry['text'], render_flags=m.HTML_SKIP_HTML)
		if 'link' in item:
			entry['link'] = item['link']
		else:
			entry['link'] = '0'
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
		if item.objType == 'comment':
			entry['href'] = '?comment=' + item['urlCode']
		else:
		    entry['href'] = '/' + item.objType + '/' + item['urlCode'] + '/' + item['url']

		if 'workshopCode' in item:
		    entry['parentHref'] = '/workshop/' + item['workshopCode'] + '/' + item['workshop_url']
		    entry['href'] = entry['parentHref'] + entry['href']
		elif 'initiativeCode' in item:
		    entry['parentHref'] = '/initiative/' + item['initiativeCode'] + '/' + item['initiative_url']
		    if entry['objType'] == 'update':
		        entry['href'] = entry['parentHref'] + '/updateShow/' + item['urlCode']
		    else:
		        entry['href'] = entry['parentHref'] + entry['href']

		# modifications for children of workshops and initiatives
		entry['parentTitle'] = ''
		entry['parentObjType'] = ''
		if 'workshopCode' in item:
		    entry['parentTitle'] = item['workshop_title']
		    entry['parentObjType'] = 'workshop'
		elif 'initiativeCode' in item:
		    entry['parentTitle'] = item['initiative_title']
		    entry['parentObjType'] = 'initiative'

		# photo
		if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
			entry['mainPhoto'] = "/images/photos/%s/photo/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
			entry['thumbnail'] = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos'])
		else:
			entry['mainPhoto'] = '0'
			entry['thumbnail'] = '0'

		#tags
		tags = []
		tagList = []
		if 'tags' in item:
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
		entry['voteCount'] = int(item['ups']) + int(item['downs'])
		entry['ups'] = int(item['ups'])
		entry['downs'] = int(item['downs'])
		entry['netVotes'] = int(item['ups']) - int(item['downs'])

		# comments
		if entry['objType'] != 'comment':
			discussion = discussionLib.getDiscussionForThing(item)
			entry['discussion'] = discussion['urlCode']
			entry['numComments'] = 0
			if 'numComments' in item:
				entry['numComments'] = item['numComments']

		# author data
		# CCN - need to find a way to optimize this lookup
		author = userLib.getUserByID(item.owner)
		entry['authorName'] = author['name']
		entry['authorPhoto'] = utils._userImageSource(author)
		entry['authorCode'] = author['urlCode']
		entry['authorURL'] = author['url']
		entry['authorHref'] = '/profile/' + author['urlCode'] + '/' + author['url']

		entry['parentTitle'] = ''
		entry['parentObjType'] = ''
		entry['article'] = 'a'
		if entry['objType'] == 'idea' or entry['objType'] == 'update' or entry['objType'] == 'initiative':
			entry['article'] = 'an'

		# modifications for children of workshops and initiatives
		if 'workshopCode' in item:
			entry['parentTitle'] = item['workshop_title']
			entry['parentObjType'] = 'workshop'
		elif 'initiativeCode' in item:
			entry['parentTitle'] = item['initiative_title']
			entry['parentObjType'] = 'initiative'

		result.append(entry)

	return result