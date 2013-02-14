<%!
   from pylowiki.lib.db.geoInfo import getGeoInfo
   
   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.idea          as ideaLib
   import pylowiki.lib.db.resource      as resourceLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.rating        as ratingLib
   
   from hashlib import md5
   import logging
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
         return False
      printStr = ''
      
      if c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:      
        printStr = '<a href="/workshop/%s/%s/add/' %(c.w['urlCode'], c.w['url'])
        if thing == 'discussion':
            printStr += 'discussion" title="Click to add a general conversation topic to this workshop"'
        elif thing == 'resources':
            printStr += 'resource" title="Click to add a resource to this workshop"'
        elif thing == 'ideas':
            printStr += 'idea" title="Click to add an idea to this workshop"'
        printStr += ' class="pull-right btn btn-large btn-success" type="button">'
        if thing == 'discussion':
            printStr += 'Add conversation'
        elif thing == 'ideas':
            printStr += 'Add an idea'
        elif thing == 'resources':
            printStr += 'Add a resource'
        printStr += '</a>'
      else:
        printStr = '<a href="/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/login/' + thing + '" title="Login to participate in this workshop." class="pull-right btn btn-large btn-success" type="button">Login to Participate</a>'

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
      if 'raw' in kwargs:
         if kwargs['raw'] == True:
            if w['mainImage_hash'] == 'supDawg':
               return "/images/%s/thumbnail/%s.thumbnail" %(w['mainImage_identifier'], w['mainImage_hash'])
            else:
               return "/images/%s/%s/thumbnail/%s.thumbnail" %(w['mainImage_identifier'], w['mainImage_directoryNum'], w['mainImage_hash'])
               
      imgStr = '<a href="'
      imgStr += workshopLink(w, embed=True, raw=True)
      if 'linkClass' in kwargs:
         imgStr += '" class="%s"' %(kwargs['linkClass'])
      imgStr += '">'
      if w['mainImage_hash'] == 'supDawg':
         picturePath = "/images/%s/thumbnail/%s.thumbnail" %(w['mainImage_identifier'], w['mainImage_hash'])
      else:
         picturePath = "/images/%s/%s/thumbnail/%s.thumbnail" %(w['mainImage_identifier'], w['mainImage_directoryNum'], w['mainImage_hash'])
      title = w['title']
      imgStr += '<img src="%s" alt="%s" title="%s"' %(picturePath, title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      
      imgStr += '></a>'
   %>
   ${imgStr | n}
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
      if 'id' in kwargs:
         resourceStr += '#%s' % kwargs['id']
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
      if 'id' in kwargs:
         resourceStr += '#%s' % kwargs['id']
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
      if 'id' in kwargs:
         ideaStr += '#%s' % kwargs['id']
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
      if 'id' in kwargs:
         resourceStr += '#%s' % kwargs['id']
      resourceStr += '"'
      if 'embed' in kwargs:
         if kwargs['embed'] == True:
            return resourceStr
   %>
   ${resourceStr | n}
</%def>

<%def name="threadLink(comment, w, thingType = None, **kwargs)">
   <% 
      if thingType == None:
         if 'ideaCode' in comment.keys():
            thingType = 'idea'
         elif 'resourceCode' in comment.keys():
            thingType = 'resource'
      d = discussionLib.getDiscussion(comment['discussionCode'])
      if d['discType'] == 'resource':
         d = resourceLib.getResourceByCode(d['resourceCode'])
      linkStr = 'href="/workshop/%s/%s/%s/%s/%s/thread/%s"' %(w["urlCode"], w["url"], thingType, d["urlCode"], d["url"], comment['urlCode'])
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
            #return threadLink(thing, workshop, **kwargs)
            if 'ideaCode' in thing.keys():
                return ideaLink(ideaLib.getIdea(thing['ideaCode']), workshop, **kwargs)
            elif 'resourceCode' in thing.keys():
                return resourceLink(resourceLib.getResourceByCode(thing['resourceCode']), workshop, **kwargs)
            else:
                return discussionLink(discussionLib.getDiscussion(thing['discussionCode']), workshop, **kwargs)
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
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
    %>
    % if 'user' in session:
    <ul class="nav nav-pills pull-left">
        % if c.scope == 'planet':
            <li class="active"> <a href="/workshops/geo/earth">Earth</a><span class="divider">/</span></li>
        % else:
            <li> <a href="/workshops/geo/earth">Earth</a><span class="divider">/</span></li>
        % endif
        
        % if c.scope == 'country':
            <li class="active"> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'country') | n}>${c.authuser_geo['countryTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'country') | n}>${c.authuser_geo['countryTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'state':
            <li class="active"> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'state') | n}>${c.authuser_geo['stateTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'state') | n}>${c.authuser_geo['stateTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'county':
            <li class="active"> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'county') | n}>${county}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'county') | n}>${county}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'city':
            <li class="active"> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'city') | n}>${city}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'city') | n}>${city}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'postalCode':
            <li class="active"> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'postalCode') | n}>${c.authuser_geo['postalCode']}</a></li>
        % else:
            <li> <a ${self._geoWorkshopLink(c.authuser_geo, depth = 'postalCode') | n}>${c.authuser_geo['postalCode']}</a></li>
        % endif
    </ul>
   % endif
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
        if depth is None:
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
            link += '%s/%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'], geoInfo['postalURL'])
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
                    <textarea name="text" rows="12" class="input-block-level">${thing['text']}</textarea>
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