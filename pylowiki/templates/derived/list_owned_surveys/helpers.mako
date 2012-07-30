<%!
    from pylowiki.lib.db.surveySlide import getSurveySlideByID
    from pylowiki.lib.db.surveyAnswer import getAllAnswersForSurvey
    from pylowiki.lib.db.user import getUserByID
    
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showSurvey(survey, surveyNumber)">
    <div class="accordion-heading">
        <a href="#collapse${surveyNumber}" data-parent="#accordion" data-toggle="collapse" class="accordion-toggle">
            % if int(survey['active']) == 0:
                <span class="label label-info">Inactive</span>
            % else:
                <span class="label label-success">Active</span>
            % endif
            ${survey['title']}
        </a>
    </div>
    <div class="accordion-body collapse" id="collapse${surveyNumber}">
        <div class="accordion-inner">
            <div class="btn-group">
                <a href = "/survey/${survey['urlCode']}/${survey['url']}/edit" class="btn">Edit
                    ##<button class="btn" href="/survey/${survey['urlCode']}/${survey['url']}/edit">Edit</button>
                </a>
                % if survey['hash'] == 'flash':
                    <a href = "/survey/${survey['urlCode']}/${survey['url']}/upload" class="btn btn-warning">
                        Upload
                    </a>
                % else:
                    <a href = "/survey/${survey['urlCode']}/${survey['url']}/upload" class="btn">
                        Upload
                    </a>
                % endif
                % if survey['hash'] != 'flash':
                    <%
                        slides = map(int, survey['slides'].split(','))
                        firstSlide = getSurveySlideByID(slides[0])
                    %>
                    <a href = "/survey/${survey['urlCode']}/${survey['url']}/page/${firstSlide['hash']}" class="btn">
                        View
                    </a>
                % endif
                <% results = getAllAnswersForSurvey(survey) %>
                % if len(results) > 0:
                    <a href="/viewResults/${survey['urlCode']}/${survey['url']}" class="btn">Results</a>
                % endif
            </div>
            <br />
            <table class="table table-striped">
                <tbody>
                    <tr>
                        <td>Name: </td>
                        <td>${survey['title']}</td>
                    </tr>
                    <tr>
                        <td>Description: </td>
                        <td>${survey['description']}</td>
                    </tr>
                    <tr>
                        <td>Date created: </td>
                        <td>${survey.date} PST</td>
                    </tr>
                    <tr>
                        <td>Public or Private: </td>
                        <td>${survey['publicOrPrivate']}</td>
                    </tr>
                    <tr>
                        <td>Survey file: </td>
                        % if survey['hash'] == 'flash':
                            <td>No file uploaded!</td>
                        % else:
                            <td>
                                <a href = "/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['origFileName']}">
                                    ${survey['origFileName']}
                                </a>
                            </td>
                        % endif
                    </tr>
                    <%
                        ids = map(int, survey['facilitators'].split(','))
                        if len(ids) > 1:
                            ids = ids[1:]
                        
                        facilitators = []
                        facilitators.append(getUserByID(survey.owner))
                        if len(ids) > 0:
                            for id in ids:
                                u = getUserByID(id)
                                if u:
                                    facilitators.append(u)
                    %>
                    % for facilitator in facilitators:
                        <tr>
                            <td>Facilitator: </td>
                            <td>${facilitator['name']}</td>
                        </tr>
                    % endfor
                    <tr>
                        <td>Postal codes:</td>
                        <td>${survey['publicPostalList']}</td>
                    </tr>
                    <tr>
                        <td>Estimated Time:</td>
                        <td>${survey['estimatedTime']} minutes</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</%def>
