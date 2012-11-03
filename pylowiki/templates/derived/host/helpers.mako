<%!
    from pylowiki.lib.db.workshop import getWorkshopsByOwner
    from pylowiki.lib.db.user import isAdmin
    from pylowiki.lib.db.account import getUserAccounts
    import textwrap
%>

<%def name="displayHostPicture()">
        <% 
            if c.revision:
                pictureHash = c.revision['pictureHash']
                name = c.revision['data']
                directoryNumber = c.revision['directoryNumber']
            else:
                pictureHash = 'flash'
                if 'pictureHash' in c.account:
                    pictureHash = c.account['pictureHash']
                name = c.account['orgName']
                if pictureHash != 'flash':
                  directoryNumber = c.account['directoryNumber']
         %>

        % if pictureHash == 'flash':
            <img src="/images/avatars/flash.profile" alt="${name}" title="${name}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % else:
            <img src="/images/avatar/${directoryNumber}/profile/${pictureHash}.profile" alt="${name}" title="${name}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % endif
        </li>
        </ul>
</%def>

<%def name="summary()">
    <% 
        if c.revision:
            orgName = c.revision['data']
            orgMessage = c.revision['orgMessage']
            orgLink = c.revision['oorgLink']
        else:
            orgName = c.account['orgName']
            orgMessage = c.account['orgMessage']
            orgLink = c.account['orgLink']
            
        endif
    %>
    <div class="civ-col-inner">
    % if orgLink and orgLink != '':
        <h1><a href="${orgLink}">${orgName}</a></h1>
    % else:
        <h1>${orgName}</h1>
    % endif
    <p>
      ${orgMessage}
    </p>
    % if c.revisions:
         <strong>Edit log:</strong><br />
         % for rev in c.revisions:
              <a href="/profile/${c.user['urlCode']}/${c.user['url']}/revision/${rev['urlCode']}">${rev.date}</a><br />  
         % endfor
    % endif
  </div> <!-- /.civ-col-inner -->
</%def>