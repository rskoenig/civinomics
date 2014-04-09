<%def name='list_studies(studies)'>
    % if len(studies) == 0:
        <p>There does not seem to be anything here!</p>
    % else:
        % for study in studies:
            <div class="span12 well" style="margin-left:0;">
                <div class="span2">
                    <a href="/corp/caseStudies/${study['url']}">
                        <div class="i-photo" style="background-image:url('/images/corp/casestudies/${study['url']}/${study['image']}');"/></div> 
                    </a>
                </div>
                <div class="span10">
                    <h4 class="no-top"><a class="no-highlight"href="/corp/surveys/${study['url']}">${study['title']}</a></h4>
                    <p>
                        ${study['description']}
                    </p>

                    <table id="metrics">
                        <tr>
                        % if 'respondents' in study:
                          <td style="padding-left: 0px;">
                            <span class="workshop-metrics">Respondents</span><br>
                              <strong ng-cloak>${study['respondents']}</strong>
                          </td>
                        % endif
                          <td>
                            <span class="workshop-metrics">Publication Date</span><br>
                              <strong ng-cloak>${study['date']}</strong>
                          </td>
                        % if 'clientLogo' in study:
                            <td>
                                <span class="workshop-metrics">Client</span><br>
                                <img style="width: 80px;" src="/images/corp/casestudies/${study['url']}/${study['clientLogo']}">
                            </td>
                        % endif
                        % if 'partnerLogo' in study:
                            <td>
                                <span class="workshop-metrics">Partners</span><br>
                                <img style="width: 80px;" src="/images/corp/casestudies/${study['url']}/${study['partnerLogo']}">
                            </td>
                        % endif
                        % if 'sponsorLogo' in study:
                            <td>
                                <span class="workshop-metrics">Sponsor</span><br>
                                <img style="width: 80px;" src="/images/corp/casestudies/${study['url']}/${study['sponsorLogo']}">
                            </td>
                        % endif
                        </tr>
                      </table>
                    

                    
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
            .${memberClass}.hidden{
                background-image:url('/images/corp/team/${member['photoHover']}');
            }
        </style>
        <div class="row">   
            <div class="span3">
                <div class="avatar avatar-team ${memberClass}"></div>
                <div class="hidden ${memberClass}"></div>
            </div>
            <div class="span8">
                <h4>Citizen ${member['name']} - ${member['title']} </h4>
                <p>${member['bio']}</p>
            </div>
        </div><!--/.row-fluid-->
    % endfor
</%def>

<%def name='pressRelease_techCommuters()'>
    <p>SANTA CRUZ EXPORTING LOCAL TECH TALENT.</p>
    <p><em>Santa Cruz tech commuters would be willing to forgo an average of 9 percent of their existing salary to work locally.</em></p>
    <p> Santa Cruz residents who work in the technology industry and commute to Silicon Valley would rather work locally, and in most cases for less money, according to a recent survey conducted by Civinomics, in partnership with South Swell Ventures.</p>
    <p>The survey was conducted between February 21st and March 14th, 2014.  Of those interviewed, the average compensation interviewees would accept in order to work locally was ninety one percent of what they are currently making. Eighty eight percent of those surveyed spend at least an hour and a half total travel time to get to their jobs over the hill. When asked why they choose to continue living in Santa Cruz, sixty seven percent answered that lifestyle was the most important reason.</p>
    <p>When asked specifically “Why do you choose to work over the hill”, the most common responses were “salary and stock compensation” (32%) and “specific job availability” (32%). The average salary of the respondents was $153,000, and sixty one percent of those interviewed stated that they worked in a technical position, with 38 percent identifying themselves as software engineers.</p>
    <p>The survey was conducted in two parts, with half of respondents being randomly selected while boarding company buses at multiple stops, and the other half being referred through a verified link via email. The latter group of respondents are primarily single car commuters who had heard about the survey through local events and co-workers.</p>
    <p>Of those interviewed at company bus stops, only 46 percent answered that they would be willing to work for less at a Santa Cruz company, compared to 78 percent of those commuting by car.  Bus commuters skewed younger than car commuters, with the average age of bus commuters being 40 and the average age of car commuters being 45.  A majority of both groups said they have considered exploring job opportunities in Santa Cruz.</p>
    <p>The survey found that tech commuters were primarily in age groups between 25 - 55 (80%), with sixty seven percent owning a home and forty six percent with children age 17 or younger at home.</p>
    <p>“The results are pretty clear, Santa Cruz has a lot of talented people who would rather be working here,” says Robert Singleton, cofounder of Civinomics and survey collector. “Access to talent is a major incentive for tech companies to start in and relocate to Santa Cruz. The opportunity for tech growth is ripe.”</p>

    <h3>Results</h3>

    <div class="alert alert-info"><strong>To filter data</strong> click on a graph. You can apply multiple filters at once. To remove a filter, click the graph again or click the reset button at the top of each graph. The 102 respondent sample ensures statistical accuracy with a 95% confidence level and 10% margin of error. Filtering the results below may be helpful to discover correlations, but it will also lead to a smaller sample pool and <strong><em>decreasing levels of accuracy.</em></strong></div>
</%def>

<%def name="text_svBagBan()">
    <p class="lead">
        This opinion poll was conducted via door-door interviews by Civinomics staff and volunteers over a two week period. Respondents were randomly selected from the list of registered voters in the City of Scotts Valley. Data was tabulated via iPad. The results are statistically accurate with a 95% confidence level and 5% margin of error.
    </p>
</%def>

