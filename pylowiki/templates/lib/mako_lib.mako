<%def name="return_to()">

    <% 
    session['return_to'] = request.path_info 
    session.save()
    %>

</%def>

<%def name="gravatar( email, size, float='none' )">
    <%from hashlib import md5%>
    <% gravatar = md5(email).hexdigest() %>
    <img src="http://www.gravatar.com/avatar/${gravatar}.jpg?s=${size}&d=http%3A%2F%2F${request.environ.get("HTTP_HOST")}%2Fimages%2Fpylo.jpg" style="width: ${size}px; float: ${float}; padding-right: 5px; vertical-align: middle;">
</%def>

<%def name="avatar( hash, size, float='none' )">
    <% avatarURL = "/images/avatars/%s.thumbnail" %(hash) %>
    <img src = "${avatarURL}" style = "width: ${size}px; float: ${float}; padding-right: 5px; vertical-align: middle;">
</%def>

<%def name="setLastPage(pageNum, survey, slide)">
    <% 
        if slide['surveySection'] == 'before':
            key = '%s_%s_lastPage' %(survey['urlCode'], survey['url'])
            if key in session:
                if int(session[key]) < pageNum:
                    session[key] = pageNum
            else:
                session[key] = pageNum
            session.save()
    %>
</%def>

<%def name="setCurrentSurveyPage(survey, slide)">
    <% 
        if slide.id in map(int, survey['slides'].split(',')):
            key = '%s_%s_currentPage' %(survey['urlCode'], survey['url'])
            session[key] = int(slide['slideNum'])
            session.save()
    %>
</%def>