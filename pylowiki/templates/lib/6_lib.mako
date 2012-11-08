<%def name="userLink(user, **kwargs)">
   <%
      thisLink = "<a href='/profile/%s/%s/'" %(user['urlCode'], user['url'])
      if 'className' in kwargs:
         thisLink += 'class = "' + kwargs['className'] + '"'
      thisLink += '>'
      if 'title' in kwargs:
         thisLink += kwargs['title']
      else:
         thisLink += user['name']
      thisLink += "</a>"
   %>
   ${thisLink | n}
</%def>

<%def name="workshopLink(w, **kwargs)">
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
         imgStr = '<img src="/images/avatars/flash.profile" alt="%s" title="%s"' %(title, title)
      else:
         imgStr = '<img src="/images/avatar/%s/profile/%s.profile" alt="%s" title="%s"' %(directoryNumber, pictureHash, title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      
      imgStr += '>'
   %>
   ${imgStr | n}
</%def>
