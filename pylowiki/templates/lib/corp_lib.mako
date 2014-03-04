<%def name='list_studies(studies)'>
    % if len(studies) == 0:
        <p>There does not seem to be anything here!</p>
    % else:
        % for study in studies:
            <div class="span12 well">
                <a class="thumbnail plain span2" href="/corp/caseStudies/${study['url']}">
                    <img src="/images/corp/casestudies/${study['url']}/${study['image']}">  
                </a>
                <div class="span10">
                    <strong><a href="/corp/caseStudies/${study['url']}">${study['title']}</a></strong>
                    <p>
                        ${study['description']}
                    </p>
                    <p><strong>${study['date']}</strong></p>
                </div>
            </div>
        % endfor
    %endif
</%def>

<%def name='list_results(reports)'>
    % if len(reports) == 0:
        <p>There does not seem to be anything here!</p>
    % else:
        % for report in reports:
            <div class="span8 news">   
                <h4><a href="/downloads/polling/${report['url']}">${report['title']}</a></h3>
                <strong>${report['partner']}</strong>
                <p>${report['date']}</p>
            </div>
        % endfor
    %endif
</%def>

<%def name="list_clientLogos(clients)">
    <ul class="thumbnails plain">
    %for client in clients:
        <li class="client">
            <a href="/corp/caseStudies/${client['url']}">
                <img src="/images/corp/casestudies/clientLogos/${client['logo']}">
            </a>
        </li>
    % endfor
</%def>

<%def name='list_news(articles)'>
    % for article in articles:
        <div class="span10 news">   
            <h4><a style="color: #333333;" href="${article['link']}" target="_blank">${article['title']}</a></h3>
            <strong>${article['source']}</strong>
            <p>${article['date']}</p>
        </div>
    % endfor
</%def>

<%def name='list_team(team)'>
    % for member in team:
        <% memberClass = member['name'].replace(' ', '') %>
        <style type="text/css">
            .${memberClass}{
                background-image:url('/images/corp/team/${member['photo']}');
                background-size:cover;
                background-position:center;
                border-radius: 500px;
            }
            .${memberClass}:hover{
                background-image:url('/images/corp/team/${member['photoHover']}');
            }
        </style>
        <div class="row">   
            <div class="span3">
                <div class="avatar avatar-team ${memberClass}"></div>
            </div>
            <div class="span8">
                <h4>Citizen ${member['name']} - ${member['title']} </h4>
                <p>${member['bio']}</p>
            </div>
        </div><!--/.row-fluid-->
    % endfor
</%def>

