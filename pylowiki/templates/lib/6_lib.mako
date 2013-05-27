<%!
   from pylowiki.lib.db.geoInfo import getGeoInfo
   from pylowiki.lib.db.tag import getCategoryTagCount
   
   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.idea          as ideaLib
   import pylowiki.lib.db.resource      as resourceLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.rating        as ratingLib
   import pylowiki.lib.db.mainImage     as mainImageLib
   
   from hashlib import md5
   import logging, os
   log = logging.getLogger(__name__)
%>

<%def name="validateSession()">
   <%
      if 'user' in session:
         if not c.authuser:
            session.delete()
   %>
</%def>

<%def name="upDownVote(thing)">
   <div class="voteWrapper">
      % if thing['disabled'] == '1' or thing.objType == 'revision':
         </div> <!-- /.voteWrapper -->
         <% return %>
      % endif
      <% rating = int(thing['ups']) - int(thing['downs']) %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'])  and not self.isReadOnly():
         <% 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  commentClass = 'voted upVote'
                  voteImg = '"/images/icons/glyphicons/upVoted.png"'
               else:
                  commentClass = 'upVote'
                  voteImg = '"/images/icons/glyphicons/upVote.png"'
            else:
               commentClass = 'upVote'
               voteImg = '"/images/icons/glyphicons/upVote.png"'
         %>
         % if thing.objType != 'comment':
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${commentClass}">
         % else:
         <a href="/rate/${thing.objType}/${thing['urlCode']}/1" class="${commentClass}">
         % endif
            <img src=${voteImg | n} class="vote-icon">
         </a>
         <br />
         <div class="centered chevron-score">${rating}</div>
         <%
            if rated:
               if rated['amount'] == '-1':
                  commentClass = 'voted downVote'
                  voteImg = '"/images/icons/glyphicons/downVoted.png"'
               else:
                  commentClass = 'downVote'
                  voteImg = '"/images/icons/glyphicons/downVote.png"'
            else:
               commentClass = 'downVote'
               voteImg = '"/images/icons/glyphicons/downVote.png"'
         %>
         % if thing.objType != 'comment':
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="${commentClass}">
         % else:
         <a href="/rate/${thing.objType}/${thing['urlCode']}/-1" class="${commentClass}">
         % endif
            <img src=${voteImg | n} class="vote-icon">
         </a>
      % else:
         <a href="#" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to make your vote count" id="nulvote" class="nullvote">
         <img src="/images/icons/glyphicons/upVote.png" class="vote-icon">
         </a>
         <br />
         <div class="centered chevron-score"> ${rating} </div>
         <a href="#" rel="tooltip" data-placement="bottom" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         <img src="/images/icons/glyphicons/downVote.png" class="vote-icon">
         </a>
         <br />
      % endif
   </div>
</%def>

<%def name="isReadOnly()">
   <%
      if (c.conf['read_only.value'] == 'true') or (c.conf['read_only.value'] == 'True'):
         return True
      else:
         return False
   %>
</%def>

<%def name="createNew(thing)">
   <%
      if isReadOnly():
         readOnlyMessage(thing)
         return
      if c.w['allowResources'] == '0' and thing == 'resources' and not (c.privs['admin'] or c.privs['facilitator']):
         return
      if c.w['allowIdeas'] == '0' and thing == 'ideas' and not (c.privs['admin'] or c.privs['facilitator']):
         return

      printStr = ''
      
      if c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:      
        printStr = '<a id="addButton" href="/workshop/%s/%s/add/' %(c.w['urlCode'], c.w['url'])
        if thing == 'discussion':
            printStr += 'discussion" title="Click to add a general conversation topic to this workshop"'
        elif thing == 'resources':
            printStr += 'resource" title="Click to add a resource to this workshop"'
        elif thing == 'ideas':
            printStr += 'idea" title="Click to add an idea to this workshop"'
        printStr += ' class="pull-right btn btn-large btn-success" type="button">'
        if thing == 'discussion':
            printStr += 'Add a conversation'
        elif thing == 'ideas':
            printStr += 'Add an idea'
        elif thing == 'resources':
            printStr += 'Add a resource'
        printStr += '</a>'
      else:
        printStr = '<a href="/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/login/' + thing + '" title="Login to participate in this workshop." class="pull-right btn btn-large btn-success" type="button" id="addButton">Login to Participate</a>'

   %>
   ${printStr | n}

</%def>

<%def name="readOnlyMessage(thing)">
   <p> Read-only: cannot add a ${thing}. </p>
</%def>

<%def name="userLink(user, **kwargs)">
   <%
      if type(user) == type(1L):
         user = userLib.getUserByID(user)
      elif type(user) == type(u''):
         user = userLib.getUserByCode(user)
      if user.objType == 'facilitator':
         user = userLib.getUserByID(user.owner)
      if user.objType == 'listener':
         user = userLib.getUserByCode(user['userCode'])
      if 'raw' in kwargs:
         if kwargs['raw']:
            return '/profile/%s/%s/' %(user['urlCode'], user['url'])
      thisLink = "<a href='/profile/%s/%s/'" %(user['urlCode'], user['url'])
      if 'className' in kwargs:
         thisLink += ' class = "' + kwargs['className'] + '"'
      thisLink += '>'
      if 'title' in kwargs:
         thisTitle = kwargs['title']
      else:
         thisTitle = user['name']
      if 'maxChars' in kwargs:
         thisTitle = ellipsisIZE(thisTitle, kwargs['maxChars'])
      thisLink += thisTitle
      if 'image' in kwargs:
         if kwargs['image'] == True:
            thisLink += userImage(user)
      thisLink += "</a>"
   %>
   ${thisLink | n}
</%def>

<%def name="workshopLink(w, **kwargs)">
   <%
   if 'embed' in kwargs:
      if kwargs['embed'] == True:
         if 'raw' in kwargs:
            if kwargs['raw'] == True:
               return "/workshop/%s/%s" %(w['urlCode'], w['url'])
         return 'href = "/workshop/%s/%s"' %(w['urlCode'], w['url'])
   %>
   href="/workshops/${w['urlCode']}/${w['url']}"
</%def>

<%def name="workshopImage(w, **kwargs)">
    <%
      mainImage = mainImageLib.getMainImage(w)
      if 'raw' in kwargs:
         if kwargs['raw'] == True:
            if mainImage['pictureHash'] == 'supDawg':
               return "/images/slide/thumbnail/supDawg.thumbnail"
            else:
               return "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
               
      imgStr = '<a href="'
      imgStr += workshopLink(w, embed=True, raw=True)
      if 'linkClass' in kwargs:
         imgStr += '" class="%s"' %(kwargs['linkClass'])
      imgStr += '">'
      if mainImage['pictureHash'] == 'supDawg':
         picturePath = "/images/slide/thumbnail/supDawg.thumbnail"
      else:
         picturePath = "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
      title = w['title']
      imgStr += '<img src="%s" alt="%s" title="%s"' %(picturePath, title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      
      imgStr += '></a>'
   %>
   ${imgStr | n}
</%def>

<%def name="commentLinkAppender(**kwargs)">
    ## Small refactoring of the resource/discussion/idea link generation when a comment is involved
    <%
        appendedLink = ''
        if 'id' not in kwargs and 'commentCode' not in kwargs:
            return appendedLink
        if 'id' in kwargs:
            appendedLink = '#%s' % kwargs['id']
        elif 'commentCode' in kwargs:
            appendedLink = '?comment=%s' % kwargs['commentCode']
        return appendedLink
    %>
</%def>

<%def name="resourceLink(r, w, **kwargs)">
   <%
        if 'directLink' in kwargs:
            if kwargs['directLink'] == True:
                resourceStr = 'href="%s' %(r['link'])
            else:
                resourceStr = 'href="/workshop/%s/%s/resource/%s/%s' %(w["urlCode"], w["url"], r["urlCode"], r["url"])
        else:
            resourceStr = 'href="/workshop/%s/%s/resource/%s/%s' %(w["urlCode"], w["url"], r["urlCode"], r["url"])
        
        resourceStr += commentLinkAppender(**kwargs)
        resourceStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
   %>
   ${resourceStr | n}
</%def>

<%def name="suggestionLink(s, w, **kwargs)">
   <%
        resourceStr = 'href="/workshop/%s/%s/suggestion/%s/%s' %(w["urlCode"], w["url"], s["urlCode"], s["url"])
        resourceStr += commentLinkAppender(**kwargs)
        resourceStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
   %>
   ${resourceStr | n}
</%def>

<%def name="ideaLink(i, w, **kwargs)">
   <%
        ideaStr = 'href="/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        ideaStr += commentLinkAppender(**kwargs)
        ideaStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return ideaStr
   %>
   ${ideaStr | n}
</%def>

<%def name="discussionLink(d, w, **kwargs)">
    <%
        resourceStr = 'href="/workshop/%s/%s/discussion/%s/%s' %(w["urlCode"], w["url"], d["urlCode"], d["url"])
        resourceStr += commentLinkAppender(**kwargs)
        resourceStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
    %>
    ${resourceStr | n}
</%def>

<%def name="commentLink(comment, w, **kwargs)">
   <% 
        linkStr = 'href="/workshop/%s/%s/comment/%s"' %(w["urlCode"], w["url"], comment["urlCode"])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return linkStr
   %>
   ${linkStr | n}
</%def>

<%def name="thingLinkRouter(thing, workshop, **kwargs)">
    <%
        if thing.objType == 'revision':
            objType = thing['objType']
        else:
            objType = thing.objType
        if objType == 'discussion':
            return discussionLink(thing, workshop, **kwargs)
        elif objType == 'suggestion':
            return suggestionLink(thing, workshop, **kwargs)
        elif objType == 'resource':
            return resourceLink(thing, workshop, **kwargs)
        elif objType == 'idea':
            return ideaLink(thing, workshop, **kwargs)
        elif objType == 'comment':
            if thing.objType == 'revision':
                return commentLink(thing, workshop, **kwargs)
            if 'ideaCode' in thing.keys():
                idea = ideaLib.getIdea(thing['ideaCode'])
                if not idea:
                    return False
                return ideaLink(idea, workshop, **kwargs)
            elif 'resourceCode' in thing.keys():
                resource = resourceLib.getResourceByCode(thing['resourceCode'])
                if not resource:
                    return False
                return resourceLink(resource, workshop, **kwargs)
            else:
                discussion = discussionLib.getDiscussion(thing['discussionCode'])
                if not discussion:
                    return False
                return discussionLink(discussion, workshop, **kwargs)
    %>
</%def>

<%def name="userImage(user, **kwargs)">
   <%
      if type(user) == type(1L):
         user = userLib.getUserByID(user)
      imgStr = ''
      if user.objType == 'facilitator':
         user = userLib.getUserByID(user.owner)
      if user.objType == 'listener':
         user = userLib.getUserByCode(user['userCode'])
      imgStr += '<a href="'
      imgStr += userLink(user, raw=True)
      imgStr += '"'
      if 'linkClass' in kwargs:
         imgStr += ' class="%s"' %(kwargs['linkClass'])
      if 'rel' in kwargs:
         imgStr += ' rel="%s"' %(kwargs['rel'])
      imgStr += '>'
      if 'revision' in kwargs:
         revision = kwargs['revision']
         title = revision['data']
      else:
         title = user['name']
      if 'className' in kwargs:
         if 'avatar-large' in kwargs['className']:
            imgStr += '<img src="http://www.gravatar.com/avatar/%s?r=pg&d=identicon&s=200" alt="%s" title="%s"' %(md5(user['email']).hexdigest(), title, title)
         else:
            imgStr += '<img src="http://www.gravatar.com/avatar/%s?r=pg&d=identicon" alt="%s" title="%s"' %(md5(user['email']).hexdigest(), title, title)
      else:   
         imgStr += '<img src="http://www.gravatar.com/avatar/%s?r=pg&d=identicon" alt="%s" title="%s"' %(md5(user['email']).hexdigest(), title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      if 'placement' in kwargs:
         imgStr += ' data-placement="%s"' % kwargs['placement']
      
      imgStr += '></a>'
   %>
   ${imgStr | n}
</%def>

<%def name="geoBreadcrumbs()">
    <%
        outOfScope = False
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]
    %>
    % if 'user' in session:
        <ul class="nav nav-pills pull-left geo-breadcrumbs">
            % for scopeLevel in scopeMapping:
                <%
                    activeClass = ''
                        
                    if c.scope['level'] == scopeLevel[0]:
                        if scopeLevel[0] != 'earth':
                            scopeKey = '%sURL' % scopeLevel[0] 
                            userScope = c.authuser_geo[scopeKey]
                        else:
                            userScope = 'earth'
                        if c.scope['name'] == userScope:
                            activeClass = 'active'
                        else:
                            outOfScope = True
                %>
                <li class="${activeClass}">
                    <a ${self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) | n}>${scopeLevel[1]}</a>
                    % if scopeLevel[0] != 'postalCode':
                        <span class="divider">/</span>
                    % endif
                </li>
            % endfor
        </ul>
    % endif
    <% 
        return outOfScope
    %>
</%def>

<%def name="outOfScope()">
    <%
        scopeName = c.scope['level']

        # More mapping for the postal code, this time to display Postal Code instead of just Postal.
        # The real fix for this is through use of message catalogs, which we will need to implement
        # when we support multiple languages in the interface, so for right now this kludge is
        # "good enough" 
        if scopeName == 'postalCode':
            scopeName = 'Postal Code'

        scopeName += " of "
        scopeName += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
    %>
    <div class="alert alert-info span6 offset3">
        <button type="button" class="close" data-dismiss="alert">x</button>
        This page is scoped for the ${scopeName}
    </div>
</%def>

<%def name="userGeoLink(user, **kwargs)">
    <%
        if type(user) == type(1L):
            user = userLib.getUserByID(user)
        userGeo = getGeoInfo(user.id)[0]
        geoLinkStr = ''
        
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'city'), userGeo['cityTitle'])
        geoLinkStr += ', '
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'state'), userGeo['stateTitle'])
        if 'comment' not in kwargs:
            geoLinkStr += ', '
            geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'country'), userGeo['countryTitle'])
    %>
    ${geoLinkStr | n}
</%def>

<%def name="_geoWorkshopLink(geoInfo, depth = None, **kwargs)">
    <%
        link = 'href="/workshops/geo/earth/'
        if depth is None or depth == 'earth':
            link += '"'
        elif depth == 'country':
            link += '%s"' % geoInfo['countryURL']
        elif depth == 'state':
            link += '%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'])
        elif depth == 'county':
            link += '%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'])
        elif depth == 'city':
            link += '%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'])
        elif depth == 'postalCode':
            link += '%s/%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'], geoInfo['postalCodeURL'])
        return link
    %>
</%def>

<%def name="disableThingLink(thing, **kwargs)">
    <%
        disableStr = '"/disable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return disableStr
                    return 'href = ' + disableStr
                return 'href = ' + disableStr
        disableStr = 'href = ' + disableStr
    %>
    ${disableStr | n}
</%def>

<%def name="enableThingLink(thing, **kwargs)">
    <%
        enableStr = '"/enable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return enableStr
                    return 'href = ' + enableStr
                return 'href = ' + enableStr
        enableStr = 'href = ' + enableStr
    %>
    ${enableStr | n}
</%def>

<%def name="immunifyThingLink(thing, **kwargs)">
    <%
        immunifyStr = '"/immunify/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return immunifyStr
                    return 'href = ' + immunifyStr
                return 'href = ' + immunifyStr
        immunifyStr = 'href = ' + immunifyStr
    %>
    ${immunifyStr | n}
</%def>

<%def name="deleteThingLink(thing, **kwargs)">
    <%
        deleteStr = '"/delete/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return deleteStr
                    return 'href = ' + deleteStr
                return 'href = ' + deleteStr
        deleteStr = 'href = ' + deleteStr
    %>
    ${deleteStr | n}
</%def>

<%def name="flagThingLink(thing, **kwargs)">
    <%
        flagStr = '"/flag/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return flagStr
                    return 'href = ' + flagStr
                return 'href = ' + flagStr
        flagStr = 'href = ' + flagStr
    %>
    ${flagStr | n}
</%def>

<%def name="editThingLink(thing, **kwargs)">
    <%
        editStr = "/edit/%s/%s" %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return editStr
                    return 'href = ' + editStr
                return 'href = ' + editStr
        editStr = 'href = ' + editStr
    %>
    ${editStr | n}
</%def>

<%def name="flagThing(thing, **kwargs)">
    <% flagID = 'flag-%s' % thing['urlCode'] %>
    <div class="row-fluid collapse" id="${flagID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to flag this ${thing.objType}?</strong>
            <br />
            <a ${flagThingLink(thing)} class="btn btn-danger flagCommentButton">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${flagID}">No</a>
            <span id = "flagged_${thing['urlCode']}"></span>
        </div>
    </div>
</%def>

<%def name="editThing(thing, **kwargs)">
    <% editID = 'edit-%s' % thing['urlCode'] %>
    <div class="row-fluid collapse" id="${editID}">
        <div class="span11 offset1">
            <form action="${editThingLink(thing, embed=True, raw=True)}" method="post" class="form form-horizontal" id="edit-${thing.objType}">
                <label>edit</label>
                % if thing.objType == 'comment':
                    <textarea class="comment-reply span12" name="textarea${thing['urlCode']}">${thing['data']}</textarea>
                % elif thing.objType == 'idea':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                % elif thing.objType == 'discussion':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                    <% 
                        text = ''
                        if 'text' in thing.keys():
                            text = thing['text']
                    %>
                    <textarea name="text" rows="12" class="input-block-level">${text}</textarea>
                % elif thing.objType == 'resource':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                    <input type="text" class="input-block-level" name="link" value = "${thing['link']}">
                    <textarea name="text" rows="12" class="input-block-level">${thing['text']}</textarea>
                % endif
                <button type="submit" class="btn" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
</%def>

<%def name="adminThing(thing, **kwargs)">
    <% 
        if thing.objType == 'revision':
            return
        adminID = 'admin-%s' % thing['urlCode']
    %>
    <div class="row-fluid collapse" id="${adminID}">
        <div class="span11 offset1 alert">
            <div class="tabbable"> <!-- Only required for left/right tabs -->
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#disable-${adminID}" data-toggle="tab">Disable</a></li>
                    <li><a href="#enable-${adminID}" data-toggle="tab">Enable</a></li>
                    <li><a href="#immunify-${adminID}" data-toggle="tab">Immunify</a></li>
                    % if c.privs['admin']:
                    <li><a href="#delete-${adminID}" data-toggle="tab">Delete</a></li>
                    % endif
                </ul>
                <div class="tab-content">
                    <div class="tab-pane active" id="disable-${adminID}">
                        <form class="form-inline" action = ${disableThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name="submit" class="btn disableButton" ${disableThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="disableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="enable-${adminID}">
                        <form class="form-inline" action = ${enableThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name = "submit" class="btn enableButton" ${enableThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="enableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="immunify-${adminID}">
                        <form class="form-inline" action = ${immunifyThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name = "submit" class="btn immunifyButton" ${immunifyThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="immunifyResponse-${thing['urlCode']}"></span>
                    </div>
                    % if c.privs['admin']:
                    <div class="tab-pane" id="delete-${adminID}">
                        <form class="form-inline" action = ${deleteThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button class="btn deleteButton" type="submit" name="submit" ${deleteThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="deleteResponse-${thing['urlCode']}"></span>
                    </div>
                    % endif
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="ellipsisIZE(string, numChars, **kwargs)">
    <%
        if numChars > len(string):
            return string
        else:
            return string[:numChars] + "..."
    %>
</%def>

<%def name="fields_alert()">
    % if 'alert' in session:
        <% 
            alert = session['alert']
            if 'type' not in alert.keys() or 'title' not in alert.keys() or 'content' not in alert.keys():
                # Something went wrong...clear and ignore the alert
                session.pop('alert')
                session.save()
                return
        %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">x</button>
            <strong>${alert['title']}</strong>
            ${alert['content']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
    % endif
</%def>

<%def name="revisionHistory(revisions, parent)">
    % if revisions:
        <div class="row-fluid">
            <div class="span6 offset1">
                <div class="accordion" id="revision-wrapper">
                    <div class="accordion-group no-border">
                        <div class="accordion-heading">
                            <a class="accordion-toggle green green-hover" data-toggle="collapse" data-parent="#revision-wrapper" href="#revisionsTable-${parent['urlCode']}">
                                Click to show revisions
                            </a>
                        </div>
                        <div id="revisionsTable-${parent['urlCode']}" class="accordion-body collapse">
                            <div class="accordion-inner no-border">
                                <table class="table table-hover table-condensed">
                                    <tr>
                                        <th>Revision</th>
                                        <th>Author</th>
                                    </tr>
                                    % for rev in revisions:
                                        <% linkStr = '<a %s>%s</a>' %(thingLinkRouter(rev, c.w, embed=True), rev.date) %>
                                        <tr>
                                            <td>${linkStr | n}</td>
                                            <td>${userLink(rev.owner)}</td>
                                        </tr>
                                    % endfor
                                </table>
                            </div>
                        </div>
                    </div>
            </div><!--/.span6 offset1-->
        </div> <!--/.row-fluid-->
    % endif
</%def>

<%def name="showItemInActivity(item, w, **kwargs)">
    <%
        thisUser = userLib.getUserByID(item.owner)
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'comment':'comment'}
        if 'expandable' in kwargs:
            if kwargs['expandable']:
                if item.objType == 'comment':
                    title = item['data']
                else:
                    title = item['title']
            else:
                if item.objType == 'comment':
                    title = ellipsisIZE(item['data'], 40)
                else:
                    title = ellipsisIZE(item['title'], 40)
        else:
            if item.objType == 'comment':
                title = ellipsisIZE(item['data'], 40)
            else:
                title = ellipsisIZE(item['title'], 40)
        
        activityStr = actionMapping[item.objType]
        if item.objType == 'comment':
            if 'ideaCode' in item.keys():
                activityStr += 'n'
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + '>'
            if 'ideaCode' in item.keys():
                activityStr += objTypeMapping['idea']
            elif 'resourceCode' in item.keys():
                activityStr += objTypeMapping['resource']
            elif 'discussionCode' in item.keys():
                activityStr += objTypeMapping['discussion']
            activityStr += '</a>, saying '
            if 'expandable' in kwargs:
                if kwargs['expandable']:
                    activityStr += ' <a ' + thingLinkRouter(item, w, embed = True, commentCode=item['urlCode']) + ' class="expandable">' + title + '</a>'
                else:
                    activityStr += ' <a ' + thingLinkRouter(item, w, embed = True, commentCode=item['urlCode']) + '>' + title + '</a>'
            else:
                activityStr += ' <a ' + thingLinkRouter(item, w, embed = True, commentCode=item['urlCode']) + '>' + title + '</a>'
        else:
            if 'expandable' in kwargs:
                if kwargs['expandable']:
                    activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + ' class="expandable">' + title + '</a>'
                else:
                    activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + '>' + title + '</a>'
            else:
                activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + '>' + title + '</a>'
    %>
    ${activityStr | n}
</%def>

<%def name="public_tags()">
  <% pTags = getCategoryTagCount() %>
    <div class="btn-group">
      <button class="btn dropdown-toggle" data-toggle="dropdown">
        Category
        <span class="caret"></span>
      </button>
      <ul class="dropdown-menu">
        % for pT in sorted(pTags.keys()):
          % if pTags[pT] > 0:
            <% fixedpT = pT.replace(" ", "_") %>
            <li><a href="/searchTags/${fixedpT}/" title="Click to view workshops with this tag">${pT}: ${pTags[pT]}</a></li>
          % endif
        % endfor
      </ul> <!-- /.unstyled -->
    </div>
</%def>

<%def name="member_tags()">
  <% mTags = getMemberTagCount() %>
  % if len(mTags.keys()) > 0:
    <ul class="unstyled">
      % for mT in sorted(mTags.keys()):
        <% fixedmT = mT.replace(" ", "_") %>
        <li><a href="/searchTags/${fixedmT}/" title="Click to view workshops with this tag">${mT}</a>: ${mTags[mT]}</li>
      % endfor
    </ul>
  % else:
    <p>No member tags.</p>
  % endif
</%def>

<%def name="fingerprintFile(path)">
    <%
        # Adds a fingerprint so we can cache-bust the browser if the file is modified
        prefix = 'pylowiki/public'
        modTime = os.stat(prefix + path).st_mtime
        return "%s?t=%s" %(path, modTime)
    %>
</%def>