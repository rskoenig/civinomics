<%!
    from pylowiki.lib.db.user import getUserByID
%> 

<%def name="profileInfo()">
    <div class="well">
	<form action="/profile/${c.user['urlCode']}/${c.user['url']}/editHandler" enctype="multipart/form-data" method="post" class="form-horizontal">
		<fieldset>
			<h3>Update Your Member Information</h3><br />
			<div class="control-group">
				<label for="member-name" class="control-label">Name:</label>
				<div class="controls">
					<input type="text" id="member-name" name="member_name" value="${c.user['name']}">
					<span class="help-inline"><span class="label label-important">Required</span></span>
				</div> <!-- /.controls -->
			</div> <!-- /.control-group -->
			<div class="control-group">
				<label for="email" class="control-label">Email:</label>
				<div class="controls">
					<input type="text" id="email" name="email" value="${c.user['email']}">
					<span class="help-inline"><span class="label label-important">Required</span> (not displayed)</span>
				</div> <!-- /.controls -->
			</div> <!-- /.control-group -->
            % if c.user['pictureHash'] != 'flash':
    		    <div class="control-group">
				    <label for="email" class="control-label">Current profile photo:</label>
				    <div class="controls">
                        <img src="/images/avatar/${c.user['directoryNumber']}/profile/${c.user['pictureHash']}.profile" alt="${c.user['name']}" title="${c.user['name']}" width="120px">
    			    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
                <% newPhoto = "new" %>
            % else:
                <% newPhoto = "" %>
            % endif
			<div class="control-group">
    			<label for="pictureFile" class="control-label">Upload a ${newPhoto} profile photo:</label>
				<div class="controls">
					${h.file("pictureFile")}
				</div> <!-- /.controls -->
			</div> <!-- /.control-group -->
            % if c.user['memberType'] == 'individual':
			    <div class="control-group">
				    <label for="tagline" class="control-label">Give us a short description of yourself:</label>
				    <div class="controls">
					    % if 'tagline' in c.user.keys():
						    <input type="text" id="tagline" name="tagline" value="${c.user['tagline']}">
					    % else:
						    <input type="text" id="tagline" name="tagline" placeholder="In 140 characters or fewer ... ">
					    % endif
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
            % else:
    		    <div class="control-group">
				    <label for="orgWelcomeMsg" class="control-label">Enter a welcome message for visitors to your profile:</label>
				    <div class="controls">
					    <% 
                            welcomeMsg = ''
                            if 'orgWelcomeMsg' in c.user.keys():
                                welcomeMsg = c.user['orgWelcomeMsg']
                        %>
                        <textarea name="orgWelcomeMsg" rows=4 cols=50>${welcomeMsg}</textarea>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLink" class="control-label">Enter the URL to your organization website:</label>
				    <div class="controls">
					    <% 
                            orgLink = ''
                            if 'orgLink' in c.user.keys():
                                orgLink = c.user['orgLink']
                        %>
                        <input type=text name="orgLink" value="${orgLink}">
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLinkMsg" class="control-label">Enter a description of your organization website:</label>
				    <div class="controls">
					    <% 
                            orgLinkMsg = ''
                            if 'orgLinkMsg' in c.user.keys():
                                orgLinkMsg = c.user['orgLinkMsg']
                        %>
                        <textarea name="orgLinkMsg" rows=4 cols=50>${orgLinkMsg}</textarea>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
            % endif
		</fieldset>
        <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>
	</form>
    </div><!-- well -->
</%def>

<%def name="changePassword()">
    <div class="well">
    <form action="/profile/${c.user['urlCode']}/${c.user['url']}/passwordHandler" enctype="multipart/form-data" method="post" class="form-horizontal">
		<fieldset>
            <h3>Change Your Password</h3><br />
            <div class="control-group">
                <label for="oldPassword" class="control-label">Old Password:</label>
                <div class="controls">
                    <input type="password" id="oldPassword" name="oldPassword">
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            <div class="control-group">
                <label for="newPassword" class="control-label">New Password:</label>
                <div class="controls">
                    <input type="password" id="newPassword" name="newPassword">
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            <div class="control-group">
                <label for="reNewPassword" class="control-label">Repeat New Password:</label>
                <div class="controls">
                    <input type="password" id="reNewPassword" name="reNewPassword">
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
        <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>
    </form>
    </div><!-- well -->
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

<%def name="memberAdmin()">
    <h3>Administrate Member</h3><br />
    % if c.user['disabled'] == '1':
       <% eAction = 'Enable' %>
    % else:
       <% eAction = 'Disable' %>
    % endif
    <form method="post" name="enableUser" id="enableUser" class="form-horizontal" action="/profile/${c.user['urlCode']}/${c.user['url']}/enable/">
        <strong>${eAction} Member</strong><br />
        <fieldset>
            <div class="control-group">
                <label for="enable" class="control-label">Reason for ${eAction}</label>
                <div class="controls">
                    <input type=text name=enableUserReason>
                    <input type=radio name="verifyEnableUser" value="0"> Verify ${eAction}
                    &nbsp;&nbsp;<button type="submit" class="btn btn-warning">${eAction} Member</button>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
    </form>
    <br /><br />
    <% 
        if c.user['accessLevel'] == '0':
            newAccess = "200"
            newTitle = "Admin"
            oldTitle = "User"
        else:
            newAccess = "0"
            newTitle = "User"
            oldTitle = "Admin"
    %>
    <form method="post" name="userPrivs" id="userPrivs" class="form-horizontal" action="/profile/${c.user['urlCode']}/${c.user['url']}/privs/">
        <strong>Change Access Level From ${oldTitle} To ${newTitle}</strong><br />
        <fieldset>
            <div class="control-group">
                <label for="setPrivs" class="control-label">Reason for Change</label>
                <div class="controls">
                        <input type=text name=accessChangeReason>
                        <input type=radio name="accessChangeVerify" value="0"> Verify Change
                        &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Change Access</button>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
        </fieldset>
     </form>
    <br /><br />
</%def>
