<%def name="Explanation()">
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
    <ul class="unstyled"
    <li><p><a href="leaderboard" class="btn btn-warning btn-mini" id='btn1'>Main LeaderBoard</a></p></li>
    % if c.suggestions:
        <li><p><a href='leaderboard_UserRanks' class="btn btn-mini btn-warning" id='btn2'>My Workshop Rankings</a></p></li>
    % endif
    <li><p><a href="leaderboard_followedPersons" class="btn btn-mini btn-warning" id='btn3'>Followed Persons</a></p></li>
    <li><p><a href="leaderboard_explanation" class="btn btn-mini btn-warning" id='btn4'>Leaderboards Explained</a></p></li>
    </ul>
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
                        <th>Title</th>
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
                        <td>
                        % if isinstance(item[3], list):
                            <a href=${item[3][1]}>${item[3][0]}
                        % else:
                            ${item[3]}
                        % endif
                        </td>
                        % if itemCount == len(c.userRankings):
                            <td id=${c.leaderboardList[0]['hrefKey']}>${item[4]}</td>
                        % else:
                            <td>${item[4]}</td>
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
                                % if c.mainLeaderboard == 'yes':
                                    <% break %>
                                % endif
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
    % if 'user' in session:
        % if c.authuser['pictureHash'] == 'flash':
            <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}"><img src="/images/avatars/flash.profile" class="thumbnail"></a>
        % else:
            <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
            <img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile" class="thumbnail"></a>
        % endif
    %endif
</%def>

