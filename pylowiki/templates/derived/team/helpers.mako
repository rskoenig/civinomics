<%def name='list_team(team)'>
    % for member in team:
        <div class="row">   
            <div class="span2">
                <ul class="thumbnails">
                  <li>
                      <img class="thumbnail" src="/images/corp/team/${member['photo']}" alt="">
                  </li>
                </ul>
            </div>
            <div class="span8">
                <h4> ${member['name']} - ${member['title']} </h4>
                <p>${member['bio']}</p>
            </div>
        </div><!--/.row-fluid-->
    % endfor
</%def>