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

<%def name='list_studies(studies)'>
    % if len(studies) == 0:
        <p>There does not seem to be anything here!</p>
    % else:
    <div>
        <ul class="thumbnails">
        % for study in studies:
            <li class="span4">
                <div class="thumbnail">
                    <a class="thumbnail inner" href="/corp/caseStudies/${study['url']}">
                        <img src="/images/corp/casestudies/${study['url']}/${study['image']}">
                        
                    </a>
                    <div class="caption">
                        <h5> ${study['title']} </h5>
                        <p>
                            ${study['description']}
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