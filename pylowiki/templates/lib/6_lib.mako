<%!
   from pylowiki.lib.db.geoInfo import getGeoInfo
   
   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.idea          as ideaLib
   import pylowiki.lib.db.resource      as resourceLib
   import pylowiki.lib.db.user          as userLib
   
   from hashlib import md5
   import logging
   log = logging.getLogger(__name__)
%>

<%def name="upDownVote(thing)">
   <div class="voteWrapper">
      <% rating = int(thing['ups']) - int(thing['downs']) %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'])  and not self.isReadOnly():
         % if thing.objType != 'comment':
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="vote upVote">
         % else:
         <a href="/rate/${thing.objType}/${thing['urlCode']}/1" class="vote upVote">
         % endif
            <i class="icon-chevron-up"></i>
         </a>
         <br />
         <div class="centered">${rating}</div>
         % if thing.objType != 'comment':
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="vote downVote">
         % else:
         <a href="/rate/${thing.objType}/${thing['urlCode']}/-1" class="vote downVote">
         % endif
            <i class="icon-chevron-down"></i>
         </a>
      % else:
         <div> ${rating} </div>
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
      if c.privs['participant'] or c.privs['facilitator'] or c.privs['admin']:
         if thing == 'discussion':
            printStr = '<a href="/workshop/%s/%s/add/discussion" title="Click to add a general discussion topic to this workshop" class="pull-right">Add Discussion Topic</a>' %(c.w['urlCode'], c.w['url'])
         elif thing == 'resources':
            printStr = '<a href="/workshop/%s/%s/add/resource" title="Click to add a resource to this workshop" class="pull-right">Add Resource</a>' %(c.w['urlCode'], c.w['url'])
         elif thing == 'ideas':
            printStr = '<a href="/workshop/%s/%s/add/idea" title="Click to add an idea to this workshop" class="pull-right">Add Idea</a>' %(c.w['urlCode'], c.w['url'])
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
         thisLink += 'class = "' + kwargs['className'] + '"'
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
               
      imgStr += '<a href="'
      imgStr += workshopLink(w, embed=True, raw=True)
      if 'linkClass' in kwargs:
         imgStr += '" class="%s"' %(kwargs['linkClass'])
      imgStr += '">'
      if workshop['mainImage_hash'] == 'supDawg':
         picturePath = "/images/${w['mainImage_identifier']}/thumbnail/${w['mainImage_hash']}.thumbnail"
      else:
         picturePath = "/images/${w['mainImage_identifier']}/${w['mainImage_directoryNum']}/thumbnail/${w['mainImage_hash']}.thumbnail"
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
        if thing.objType == 'discussion':
            return discussionLink(thing, workshop, **kwargs)
        elif thing.objType == 'suggestion':
            return suggestionLink(thing, workshop, **kwargs)
        elif thing.objType == 'resource':
            return resourceLink(thing, workshop, **kwargs)
        elif thing.objType == 'idea':
            return ideaLink(thing, workshop, **kwargs)
        elif thing.objType == 'comment':
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
    % if 'user' in session:
    <ul class="nav nav-pills pull-left">
        % if c.scope == 'earth':
            <li class="active"> <a href="/workshops/">Earth</a><span class="divider">/</span></li>
        % else:
            <li> <a href="/workshops/">Earth</a><span class="divider">/</span></li>
        % endif
        
        % if c.scope == 'country':
            <li class="active"> <a href="${c.authuser_geo['countryURL']}">${c.authuser_geo['countryTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a href="${c.authuser_geo['countryURL']}">${c.authuser_geo['countryTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'state':
            <li class="active"> <a href="${c.authuser_geo['stateURL']}">${c.authuser_geo['stateTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a href="${c.authuser_geo['stateURL']}">${c.authuser_geo['stateTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'county':
            <li class="active"> <a href="${c.authuser_geo['countyURL']}">${c.authuser_geo['countyTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a href="${c.authuser_geo['countyURL']}">${c.authuser_geo['countyTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'city':
            <li class="active"> <a href="${c.authuser_geo['cityURL']}">${c.authuser_geo['cityTitle']}</a> <span class="divider">/</span> </li>
        % else:
            <li> <a href="${c.authuser_geo['cityURL']}">${c.authuser_geo['cityTitle']}</a> <span class="divider">/</span> </li>
        % endif
        
        % if c.scope == 'postalCode':
            <li class="active"> <a href="${c.authuser_geo['postalURL']}">${c.authuser_geo['postalCode']}</a></li>
        % else:
            <li> <a href="${c.authuser_geo['postalURL']}">${c.authuser_geo['postalCode']}</a></li>
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
        
        geoLinkStr += '<a href="%s" class="geoLink">%s</a>' %(userGeo['cityURL'], userGeo['cityTitle'])
        geoLinkStr += ', '
        geoLinkStr += '<a href="%s" class="geoLink">%s</a>' %(userGeo['stateURL'], userGeo['stateTitle'])
        if 'comment' not in kwargs:
            geoLinkStr += ', '
            geoLinkStr += '<a href="%s" class="geoLink">%s</a>' %(userGeo['countryURL'], userGeo['countryTitle'])
    %>
    ${geoLinkStr | n}
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
   ${resourceStr}
</%def>

<%def name="disableThing(thing, **kwargs)">
    <%
        disableStr = 'href = "/disable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return disableStr
    %>
    ${disableStr | n}
</%def>

<%def name="enableThing(thing, **kwargs)">
    <%
        enableStr = 'href = "/enable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return enableStr
    %>
    ${enableStr | n}
</%def>

<%def name="deleteThing(thing, **kwargs)">
    <%
        deleteStr = 'href = "/delete/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return deleteStr
    %>
    ${deleteStr | n}
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