<%!
    from pylowiki.lib.db.surveySlide import getSurveySlideByID
%>

<%def name='draw_avatar()'>
    % if c.authuser['pictureHash'] == 'flash':
        <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
            <img src="images/avatars/flash.profile">
        </a>
    % else:
        <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
            <img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile">
        </a>
    % endif
    <br />
    <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
        <strong>${c.authuser['name']}</strong>
    </a>
    <br>
    <a href="/account/edit">Edit my profile</a>
</%def>

<%def name='upcomingWorkshops()'>
    <ul class="thumbnails">
        <li class="span3">
            <div class="thumbnail" style="background-color:#D1CCC3;">
                <img src="/images/corp/muni.png">
                <div class="caption">
                    <h5 style="text-align:center;">MUNI</h5>
                    <p>
                        San Francisco's transportation agency is chronically under-funded and desperately needs a new gameplan.
                    </p>
                </div>
            </div>
        </li>
        <li class="span3">
            <div class="thumbnail" style="background-color:#C4D198;">
                <img src="/images/corp/tech.png">
                <div class="caption">
                    <h5 style="text-align:center;">SF Tech Economy</h5>
                    <p>
                        How much should the city give and get from the valley's biggest tech corporations?
                    </p>
                </div>
            </div>
        </li>
        <li class="span3">
            <div class="thumbnail" style="background-color:#D1CCC3;">
                <img src="/images/corp/soda.png">
                <div class="caption">
                    <h5 style="text-align:center;">Soda Tax</h5>
                    <p>
                        Will consider various regulations on sugary beverages as a means of improving public health.
                    </p>
                </div>
            </div>
        </li>
    </ul>
</%def>

<%def name='featured_survey(survey)'>
    ## Non standard color
    <h1> Featured Survey </h1>
    <br />
    % if survey:
        <% slideIDs = map(int, survey['slides'].split(',')) %>
        <div class="offset1">
            <ul class="thumbnails">
                <li class="span7">
                    <div class="thumbnail">
                        <% firstSlide = getSurveySlideByID(slideIDs[0]) %>
                        <a class="thumbnail" href="/survey/${survey['urlCode']}/${survey['url']}/page/${firstSlide['hash']}">
                            <img src="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${firstSlide['image']}">
                        </a>
                        <div class="caption">
                            <h5> ${survey['title']} </h5>
                            <p>
                                Estimated time: ${survey['estimatedTime']} minutes
                            </p>
                            <p>
                                ${survey['description']}
                            </p>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    % else:
        <p>There doesn't seem to be anything here!</p>
    % endif
</%def>

<%def name='list_surveys(surveys)'>
    <h2 style="text-align:center;"> Other Surveys </h2>
    <br />
    % if len(surveys) == 0:
        <p>There doesn't seem to be anything here!</p>
    % else:
    <div class="offset1">
        <ul class="thumbnails">
        % for survey in surveys:
            <%
                slides = survey['slides'].split(',') 
                firstSlide = getSurveySlideByID(int(slides[0]))
            %>
            <li class="span4">
                <div class="thumbnail">
                    <a class="thumbnail" href="/surveys/${survey['urlCode']}/${survey['url']}/page/${firstSlide['hash']}">
                        <img src="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${firstSlide['image']}">
                    </a>
                    <div class="caption">
                        <h5> ${survey['title']} </h5>
                        <p>
                            Estimated time: ${survey['estimatedTime']} minutes
                        </p>
                        <p>
                            ${survey['description']}
                        </p>
                    </div>
                </div>
            </li>
        % endfor
        </ul>
    </div>
    %endif
</%def>


<%def name="showMessage()">
    <div class="alert alert-${c.message['type']}">
        <button data-dismiss="alert" class="close">×</button>
        <strong>${c.message['title']}</strong> ${c.message['content']}
    </div>
</%def>
