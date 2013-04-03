<%!
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.listener         as listenerLib
    import pylowiki.lib.db.facilitator      as facilitatorLib
    import pylowiki.lib.db.workshop         as workshopLib
    import pylowiki.lib.db.mainImage        as mainImageLib
    import pylowiki.lib.db.discussion       as discussionLib
%> 

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="profileInfo()">
    <div class="section-wrapper">
        <div class="browse">
	        <form action="/profile/${c.user['urlCode']}/${c.user['url']}/info/edit/handler" id="infoEdit" enctype="multipart/form-data" method="post" class="form-horizontal">
    		    <h4 class="section-header" style="text-align: center"><br />Update Your Profile Information</h4><br />
                <fieldset>
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
             <div class="control-group">
                <label for="image" class="control-label">Image:</label>
                <div class="controls">
                    <span id="image" class="help-inline">
                        Change and manage your profile picture at <a href="http://www.gravatar.com" target="_blank">Gravatar</a>
                    </span>
                </div>
             </div>
        	    <div class="control-group">
				    <label for="greetingMsg" class="control-label">Enter a greeting message for visitors to your profile:</label>
				    <div class="controls">
                        <textarea name="greetingMsg" rows=4 cols=50>${c.user['greetingMsg']}</textarea>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLink" class="control-label">Enter the URL to your website:</label>
    			    <div class="controls">
                        <input type="text" name="websiteLink" value="${c.user['websiteLink']}">
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLinkMsg" class="control-label">Enter a description of your website:</label>
				    <div class="controls">
                        <textarea name="websiteDesc" rows=4 cols=50>${c.user['websiteDesc']}</textarea>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
		        </fieldset>
                <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>
	        </form>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="profileMessages()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" class="centered"><br />Messages</h4>
            <table class="table table-condensed table-hover">
                <thead>
                    <th>Sender</th>
                    <th>Message</th>
                </thead>
                % for message in c.messages:
                    <tr>
                        <%
                            if message['sender'] == u'0':
                                sender = 'Civinomics'
                            else:
                                sender = userLib.getUserByCode(message['sender'])
                        %>
                        <td>
                            % if sender == 'Civinomics':
                                <img src="/images/handdove_medium.png" title="Civinomics" alt="Civinomics">
                                <p>Civinomics</p>
                            % else:
                                ${lib_6.userImage(sender, className="avatar")}
                                <p>${lib_6.userLink(sender)}</p>
                            % endif
                        </td>
                        <td> 
                            % if 'extraInfo' in message.keys():
                                % if message['extraInfo'] in ['listenerInvite', 'facilitationInvite']:
                                    <% 
                                        workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                                        if message['extraInfo'] == 'listenerInvite':
                                            formStr = """<form method="post" name="inviteListener" id="inviteListener" action="/profile/%s/%s/listener/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                            action = 'be a listener for'
                                        else:
                                            formStr = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                            action = 'facilitate'
                                    %>
                                    % if message['read'] == u'1':
                                        <div class="media">
                                            ${lib_6.workshopImage(workshop, linkClass="pull-left")}
                                            <div class="media-body">
                                                <h4 class="media-heading centered">${message['title']}</h4>
                                                <p>${lib_6.userLink(sender)} invites you to facilitate <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a></p>
                                                <p>${message['text']}</p>
                                                <p>(You have already responded)</p>
                                                <p class="pull-right"><small>${message.date} (PST)</small></p>
                                            </div>
                                        </div>
                                    % else:
                                        ${formStr | n}
                                            <input type="hidden" name="workshopCode" value="${workshop['urlCode']}">
                                            <input type="hidden" name="workshopURL" value="${workshop['url']}">
                                            <input type="hidden" name="messageCode" value="${message['urlCode']}">
                                            <div class="media">
                                                ${lib_6.workshopImage(workshop, linkClass="pull-left")}
                                                <div class="media-body">
                                                    <h4 class="media-heading centered">${message['title']}</h4>
                                                    <p>${lib_6.userLink(sender)} invites you to ${action} <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a></p>
                                                    <p>${message['text']}</p>
                                                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-success" title="Accept the invitation to ${action} the workshop">Accept</button>
                                                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to ${action} the workshop">Decline</button>
                                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                                </div>
                                            </div>
                                        </form>
                                    % endif
                                % endif
                            % endif
                        </td>
                    </tr>
                % endfor
            </table>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="changePassword()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Change Your Password</h4><br />
            <form action="/profile/${c.user['urlCode']}/${c.user['url']}/password/update/handler" enctype="multipart/form-data" method="post" class="form-horizontal">
		    <fieldset>
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
        </div><!-- browse -->
    </div><!-- section-wrapper-->
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
          <% user = userLib.getUserByID(event.owner) %>
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
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Administrate Member</h3><br />
            % if c.user['disabled'] == '1':
                <% eAction = 'Enable' %>
            % else:
                <% eAction = 'Disable' %>
            % endif
            <form method="post" name="enableUser" id="enableUser" class="form-horizontal" action="/profile/${c.user['urlCode']}/${c.user['url']}/enable/handler">
            <strong>${eAction} Member</strong><br />
            <fieldset>
                <div class="control-group">
                    <label for="enable" class="control-label">Reason for ${eAction}</label>
                    <div class="controls">
                        <input type="text" name="enableUserReason">
                        <input type="radio" name="verifyEnableUser" value="0"> Verify ${eAction}
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
            <form method="post" name="userPrivs" id="userPrivs" class="form-horizontal" action="/profile/${c.user['urlCode']}/${c.user['url']}/privs/handler">
            <strong>Change Access Level From ${oldTitle} To ${newTitle}</strong><br />
            <fieldset>
            <div class="control-group">
                <label for="setPrivs" class="control-label">Reason for Change</label>
                <div class="controls">
                    <input type="text" name="accessChangeReason">
                    <input type="radio" name="accessChangeVerify" value="0"> Verify Change
                    &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Change Access</button>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            </fieldset>
            </form>
            <br /><br />
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="pendingListenerInvitations()">
    <div class="well">
        <strong>Invitations to be a Workshop Listener</strong><br />
        <% fNum = len(c.pendingListeners) %>
        <% wNum = 0 %>
        % for l in c.pendingListeners:
            % if wNum % 6 == 0 or wNum == 0: ## begin a new row
                <ul class="unstyled civ-block-list">
            % elif wNum % 6 == 5: ## end a row
                </ul>
                <ul class="unstyled civ-block-list">
            % endif
            <li>
            <% workshop = workshopLib.getWorkshopByCode(l['workshopCode']) %>
            <form method="post" name="inviteListener" id="inviteListener" action="/profile/${c.user['urlCode']}/${c.user['url']}/listener/response/handler/">
            <input type="hidden" name="workshopCode" value="${workshop['urlCode']}">
            <input type="hidden" name="workshopURL" value="${workshop['url']}">
            <% mainImage = mainImageLib.getMainImage(workshop) %>
            % if mainImage['pictureHash'] == 'supDawg':
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/slide/slideshow/supDawg.slideshow" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
            % else:
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/mainImage/${mainImage['directoryNum']}/orig/${mainImage['pictureHash']}.jpg" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
            % endif
            <br /> <br />
            <button type="submit" name="acceptInvite" class="btn btn-mini btn-success" title="Accept the invitation to be a listener of this workshop">Accept</button>
            <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to be a listener of this workshop">Decline</button>
            </form>
            <li>
            <% 
            wNum = wNum + 1
            if wNum == 6:
              wNum = 0
            %>
        % endfor
        </ul>
    </div><!-- well -->
</%def>

