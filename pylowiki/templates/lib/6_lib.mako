<%!
   from pylowiki.lib.db.user import getUserByID
%>

<%def name="upDownVote(thing)">
   <% rating = int(thing['ups']) - int(thing['downs']) %>
   % if 'user' in session and c.isScoped and not self.isReadOnly():
      <a href="/rate${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="vote upVote">
         <i class="icon-chevron-up"></i>
      </a>
         <div class="centered">${rating}</div>
      <a href="/rate${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="vote downVote">
         <i class="icon-chevron-down"></i>
      </a>
   % else:
      <div> ${rating} </div>
   % endif
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

      if c.isScoped or c.isFacilitator or c.isAdmin:
         if thing == 'discussion':
            printStr = '<a href="/workshop/%s/%s/addDiscussion" title="Click to add a general discussion topic to this workshop" class="pull-right">Add Discussion Topic</a>' %(c.w['urlCode'], c.w['url'])
         elif thing == 'resources':
            printStr = '<a href="/newResource/%s/%s" title="Click to add a resource to this workshop" class="pull-right">Add Resource</a>' %(c.w['urlCode'], c.w['url'])
   %>
   ${printStr | n}
</%def>

<%def name="readOnlyMessage(thing)">
   <p> Read-only: cannot add a ${thing}. </p>
</%def>

<%def name="userLink(user, **kwargs)">
   <%
      if user.objType == 'facilitator':
         user = getUserByID(user.owner)
      if 'raw' in kwargs:
         if kwargs['raw']:
            return '/profile/%s/%s/' %(user['urlCode'], user['url'])
      thisLink = "<a href='/profile/%s/%s/'" %(user['urlCode'], user['url'])
      if 'className' in kwargs:
         thisLink += 'class = "' + kwargs['className'] + '"'
      thisLink += '>'
      if 'title' in kwargs:
         thisLink += kwargs['title']
      else:
         thisLink += user['name']
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

<%def name="resourceLink(r, w, **kwargs)">
   <%
      resourceStr = 'href="/workshop/%s/%s/resource/%s/%s"' %(w["urlCode"], w["url"], r["urlCode"], r["url"])
      if 'embed' in kwargs:
         if kwargs['embed'] == True:
            return resourceStr
   %>
   ${resourceStr}
</%def>

<%def name="suggestionLink(s, w, **kwargs)">
   <%
      resourceStr = 'href="/workshop/%s/%s/suggestion/%s/%s"' %(w["urlCode"], w["url"], s["urlCode"], s["url"])
      if 'embed' in kwargs:
         if kwargs['embed'] == True:
            return resourceStr
   %>
   ${resourceStr}
</%def>

<%def name="discussionLink(d, w, **kwargs)">
   <%
      resourceStr = 'href="/workshop/%s/%s/discussion/%s/%s"' %(w["urlCode"], w["url"], d["urlCode"], d["url"])
      if 'embed' in kwargs:
         if kwargs['embed'] == True:
            return resourceStr
   %>
   ${resourceStr}
</%def>

<%def name="userImage(user, **kwargs)">
   <%
      imgStr = ''
      if user.objType == 'facilitator':
         user = getUserByID(user.owner)
      imgStr += '<a href="'
      imgStr += userLink(user, raw=True)
      imgStr += '">'
      if 'revision' in kwargs:
         revision = kwargs['revision']
         pictureHash = revision['pictureHash']
         title = revision['data']
         directoryNumber = revision['directoryNumber']
      else:
         pictureHash = user['pictureHash']
         title = user['name']
         if pictureHash != 'flash':
            directoryNumber = user['directoryNumber']
      if pictureHash == 'flash':
         imgStr += '<img src="/images/avatars/flash.profile" alt="%s" title="%s"' %(title, title)
      else:
         imgStr += '<img src="/images/avatar/%s/profile/%s.profile" alt="%s" title="%s"' %(directoryNumber, pictureHash, title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      
      imgStr += '></a>'
   %>
   ${imgStr | n}
</%def>

<%def name="geoBreadcrumbs()">
   <ul class="nav nav-pills pull-left">
      <li class="active"> <a href="#">Earth</a><span class="divider">/</span></li>
      <li> <a href="#">USA</a> <span class="divider">/</span> </li>
      <li> <a href="#">California</a> <span class="divider">/</span> </li>
      <li> <a href="#">Santa Cruz Co.</a> <span class="divider">/</span> </li>
      <li> <a href="#">Santa Cruz City</a> <span class="divider">/</span> </li>
      <li> <a href="#">95060</a></li>
   </ul>
</%def>