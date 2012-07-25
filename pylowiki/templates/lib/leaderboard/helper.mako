<%def name="Explaination()">
    <div class="civ-col">
        % for explaination in c.Explain:
            <h3 class="civ-col">${explaination[0]}</h2>
            <div class="civ-col-inner">
                ${explaination[1]}
            </div> <!-- /.civ-col-inner -->
        % endfor
    </div> <!-- /.civ-col -->
</%def>

<%def name="Menu()">
    <div class="well">
        <div class="civ-col-inner">
            <div class="row">
                <button class="btn btn-warning" href="leaderboard" >Main LeaderBoard</button>
            </div>
            <div class="row">
                <button class="btn btn-warning" href='#' >My Rankings</button>
            </div>
            <div class="row">
                <button class="btn btn-warning" href="leaderboard_followedPersons" >Followed Persons</button>
            </div>
        </div>
        <ul class="nav nav-pills nav-stacked">
            <li><a href="leaderboard_followedPersons">Followed Persons&nbsp&nbsp&nbsp&nbsp&nbsp</a></li>
            <li><a href='#'>Followed Suggestions</a></li>
            <li><a href='#'>Followed Resources&nbsp&nbsp</a></li>
        </ul>
        <select id="select0">
            <option>City</option>
            <option>County</option>
            <option>Country</option>
        </select>
        <select id="select1">
            <option>Santa Cruz</option>
            <option>San Fransisco</option>
            <option>San Jose</option>
        </select>
   </div>
</%def>

<%def name="Overall_Leaderboard()">
    <div class="civ-col">
        <h2 class="civ-col">Overall Leaderboard Rankings</h2>
        <div class="civ-col-inner">
            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Rank</th>
                        <th>Metric of Ranking</th>
                    </tr>
                </thead>
                <tbody>
                    <% itemCount = 1 %>
                    % for item in c.userRankings:
                        <td>
                            <a href=${item[1]}>${item[0]}
                        </td>
                        <td>${item[2]}</td>
                        % if itemCount == len(c.userRankings):
                            <td id=${c.leaderboardList[0]['hrefKey']}>${item[3]}</td>
                        % else:
                            <td>${item[3]}</td>
                            <% itemCount += 1 %>
                        % endif
                    </tr>
                    % endfor
                </tbody>
            </table>
        </div> <!-- /.civ-col-inner -->
    </div> <!-- /.civ-col -->
    </br>
</%def>

<%def name="DisplayLeaderboards()">
    <% hrefCount = 1 %>
    % for board in c.leaderboardList:
        <div class="civ-col">
            <h2 class="civ-col">${board['title']}</h2>
            <div class="civ-col-inner">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                        % for header in board['headers']:
                            <th>
                            % if isinstance(header, list):
                                <i class=${header[0]}></i> ${header[1]}
                            %else:
                                ${header}
                            % endif
                            </th>
                        % endfor
                        </tr>
                    </thead>
                    <tbody>
                        <% rowCount = 1 %>
                        % for row in board['tablebody']:
                            % if rowCount > 5:
                                <% break %>
                            % else:
                                <% rowCount += 1 %>
                            % endif
                            % for item in row:
                                <td>
                                % if isinstance(item, list):
                                    <a href=${item[1]}>
                                    % if isinstance(item[0], list):
                                        <img src=${item[0][0]} width="20">&nbsp&nbsp${item[0][1]}
                                    % else:
                                        ${item[0]}
                                    % endif:
                                    </a>
                                % else:
                                    % if isinstance(item, dict):
                                        <img src=${item['img']} width="15">
                                    % else:
                                        ${item}
                                    % endif
                                % endif
                                </td>
                            % endfor
                            </tr>
                        % endfor
                    </tbody>
                </table>
                <p align="right">
                    % if hrefCount == len(c.leaderboardList):
                        <a href='#'>Back to Top</a>
                    % else:
                        <a href='#' id=${c.leaderboardList[hrefCount]['hrefKey']}>Back to Top</a>
                        <% hrefCount += 1 %>
                    % endif
                </p>
                </br>
            </div> <!-- /.civ-col-inner -->
        </div> <!-- /.civ-col -->
    % endfor
</%def>

<%def name="UserPhoto()">
    % if c.authuser['pictureHash'] == 'flash':
        <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}"><img src="/images/avatars/flash.profile" width="160" ></a>
    % else:
        <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
            <img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile" width="160">
        </a>
    % endif
    <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
        <center>${c.authuser['name']}</center>
    </a>
</%def>
