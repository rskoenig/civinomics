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