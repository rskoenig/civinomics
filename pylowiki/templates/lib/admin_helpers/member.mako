<%!
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.user import getUserByID
%>  

<%def name="editProfileInfo()">
    <form action="/profile/editSubmit" enctype="multipart/form-data" method="post" class="form-horizontal">
        <input type=hidden name="memberCode" value="${c.user['urlCode']}" >
        <input type=hidden name="memberURL" value="${c.user['url']}" >
        <fieldset>
            <legend>Basic Information</legend>
            <div class="control-group">
                <label for="first-name" class="control-label">First name:</label>
                <div class="controls">
                    <input type="text" id="first-name" name="first_name" placeholder="${c.user['firstName']}">
                    <span class="help-inline"><span class="label label-important">Required</span></span>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            <div class="control-group">
                <label for="last-name" class="control-label">Last name:</label>
                <div class="controls">
                    <input type="text" id="last-name" name="last_name" placeholder="${c.user['lastName']}">
                    <span class="help-inline"><span class="label label-important">Required</span></span>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            <div class="control-group">
                <label for="email" class="control-label">Email:</label>
                <div class="controls">
                    <input type="text" id="email" name="email" placeholder="${c.user['email']}">
                    <span class="help-inline"><span class="label label-important">Required</span></span>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
        <fieldset>
            <legend>Upload a profile photo</legend>
            <div class="control-group">
                <div class="controls">
                    ${h.file("pictureFile")}
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
        <fieldset>
            <legend>About me</legend>
            <div class="control-group">
                <label for="tagline" class="control-label">Tagline:</label>
                <div class="controls">
                    % if 'tagline' in c.user.keys():
                        <input type="text" id="tagline" name="tagline" placeholder="${c.user['tagline']}">
                    % else:
                        <input type="text" id="tagline" name="tagline" placeholder="In 140 characters or fewer ... ">
                    % endif
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
        <fieldset>
            <div class="form-actions">
                <button class="btn btn-success" type="submit">
                <i class="icon-ok-circle icon-white"></i>
                Save changes
                </button>
                <a class="btn btn-danger" onclick="javascript:history.go(-1)">
                <i class="icon-ban-circle icon-white"></i>
                Cancel
                </a>
            </div> <!-- /.form-actions -->
        </fieldset>
    </form>	
</%def>

<%def name="displayProfilePicture()">
        % if c.user['pictureHash'] == 'flash':
                <img src="/images/avatars/flash.profile" alt="${c.user['name']}" title="${c.user['name']}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % else:
            <img src="/images/avatar/${c.user['directoryNumber']}/profile/${c.user['pictureHash']}.profile" alt="${c.user['name']}" title="${c.user['name']}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
        % endif
        </li>
        </ul>
</%def>

<%def name="user()">
    <div class="page-header">
        <h1><a href="/profile/${c.user['urlCode']}/${c.user['url']}">${c.title}</a></h1>
    </div>     
    <br /><br />
</%def>

<%def name="memberEvents()">
    % if c.events:
       <% numEvents = len(c.events) %>
       <% eString = "Events" %>
       % if numEvents == 1:
          <% eString = "Event" %>
       % endif
       <strong>${numEvents} ${eString}:</strong>
       <br /><br />
       % for event in c.events:
          <% user = getUserByID(event.owner) %>
          ${event['title']} ${event.date}
          % if user:
              by ${user['name']}
          % endif
          <br />
          Reason: ${event['data']}
          <br /><br />
       %endfor
    % endif
</%def>

<%def name="memberAccessControls()">
    <p>
    <strong class="gray">Administrate Member</strong>
    <br /><br />
    % if c.user['disabled'] == '1':
       <% eAction = 'Enable' %>
    % else:
       <% eAction = 'Disable' %>
    % endif
    <br /><br />
    <strong>${eAction} Member</strong><br /><br />
    <form method="post" name="enableUser" id="enableUser" action="/profile/${c.user['urlCode']}/${c.user['url']}/enable/">
       Reason for Member ${eAction}: <input type=text name=enableUserReason> <br /><br />
       <input type=radio name="verifyEnableUser" value="0"> Verify ${eAction}
       &nbsp;&nbsp;<button type="submit" class="btn btn-warning">${eAction} Member</button>
    </form>
    <br /><br />
    <strong>Change Access Level</strong><br /><br />
    Current Access Level: ${c.user['accessLevel']}
    <form method="post" name="userPrivs" id="userPrivs" action="/profile/${c.user['urlCode']}/${c.user['url']}/privs/">
     Reason for Member Access Level Change: <input type=text name=changeAccessReason><br /><br /> 
     % if c.user['accessLevel'] == '0':
        <input type=radio name="setPrivsFacil" value="100"> Facilitator &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsAdmin" value="200"> Admin
     % elif c.user['accessLevel'] == '100':
        <input type=radio name="setPrivsUser" value="0"> User &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsAdmin" value="200"> Admin
     % else:
        <input type=radio name="setPrivsUser" value="0"> User &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsFacil" value="100"> Facilitator
     % endif
     &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Set Privs</button>
     </form>
    <br /><br />
</%def>


<%def name="memberAccount()">
    % if c.account:
       <strong>Member Account</strong><br /><br />
       Total hosting for account: ${c.account['numHost']}<br /> 
       <% numWorkshops = len(c.workshops) %>
       Total workshops hosted for account: ${numWorkshops}<br /> 
       % if c.workshops:
          % for w in c.workshops:
             &nbsp; &nbsp; &nbsp; &bull; &nbsp;<a href="/workshop/${w['urlCode']}/${w['url']}">${w['title']}</a>
             <br />
          % endfor
       % endif
       Total hosted remaining for account: ${c.account['numRemaining']}<br /> 
       <br /><br /> 
       <form method="post" name="userAccount" id="userAccount" action="/profile/${c.user['urlCode']}/${c.user['url']}/account/">
       Change number of objects which may be hosted: 
       <select name="numHost">
       % for i in range(1, 11):
        <option>${i}</option>
       % endfor
       </select>
       <br /><br />
       <button type="submit" class="btn btn-warning">Update Account</button>
       </form> 
    % else:
       <strong>Create User Account</strong><br /><br />
       <form method="post" name="userAccount" id="userAccount" action="/profile/${c.user['urlCode']}/${c.user['url']}/account/">
       Number of objects which may be hosted: 
       <select name="numHost">
       % for i in range(1, 11):
        <option>${i}</option>
       % endfor
       </select>
       <br /><br />
       <button type="submit" class="btn btn-warning">Add Account</button>
       </form> 
    % endif
</%def>
