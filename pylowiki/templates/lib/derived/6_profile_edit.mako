<%!
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.listener         as listenerLib
    import pylowiki.lib.db.facilitator      as facilitatorLib
    import pylowiki.lib.db.workshop         as workshopLib
    import pylowiki.lib.db.mainImage        as mainImageLib
    import pylowiki.lib.db.discussion       as discussionLib
    import pylowiki.lib.db.comment          as commentLib
    import pylowiki.lib.db.event            as eventLib
    import pylowiki.lib.db.generic          as generic
%> 

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="profileInfo()">
    <div class="section-wrapper">
        <div class="browse">
	        <form id="infoEdit" name="infoEdit" class="form-horizontal edit-profile">
    		    <h4 class="section-header smaller">Update Your Profile Information</h4>
                <fieldset>
			    <div ng-class=" {'control-group': true, 'error': infoEdit.member_name.$error.pattern} ">
				    <label for="member-name" class="control-label">Your Name:</label>
				    <div class="controls">
					    <input type="text" id="member-name" class="span10" name="member_name" value="${c.user['name']}" ng-model="fullName" ng-init="fullName='${c.user['name']}'" ng-pattern="fullNameRegex" required>
                        <span class="error help-block" ng-show="infoEdit.member_name.$error.pattern">Use only letters, numbers, spaces, and _ (underscore)</span>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
			    <div class="control-group">
				    <label for="email" class="control-label">Email:</label>
				    <div class="controls">
					    <input type="text" id="email" class="span10" name="email" ng-model="email" ng-init="email='${c.user['email']}'" required>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
                <div ng-class=" {'control-group': true, 'error': infoEdit.postalCode.$error.pattern} ">
				    <label for="postalCode" class="control-label">Postal code:</label>
                    <div class="controls">
					    <input type="text" id="postalCode" class="span10" name="postalCode" onBlur="geoCheckPostalCode()" ng-model="postalCode" ng-init="postalCode='${c.user['postalCode']}'" ng-pattern="postalCodeRegex" required>
                        <br />
                        <span class="error help-block" ng-show="infoEdit.postalCode.$error.pattern">Use only numbers.</span>
                        <span id="postalCodeResult"></span>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
        	    <div class="control-group">
				    <label for="greetingMsg" class="control-label">Short bio:</label>
				    <div class="controls">
                        <input type="text" name="greetingMsg" ng-model="greetingMsg" ng-init="greetingMsg='${c.user['greetingMsg']}'" rows=4 class="span10">
                        <span class="help-block">Displayed with your posts<br>(example: Thomas Jefferson, Founding Father)</span>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLink" class="control-label">Your website:</label>
    			    <div class="controls">
                        <input type="text" class="span10" name="websiteLink" ng-model="websiteLink" ng-init="websiteLink='${c.user['websiteLink']}'">
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
       	        <div class="control-group">
				    <label for="orgLinkMsg" class="control-label">A description of your website:</label>
				    <div class="controls">
                        <textarea name="websiteDesc" ng-model="websiteDesc" ng-init="websiteDesc='${c.user['websiteDesc']}'" rows=4 class="span10"></textarea>
				    </div> <!-- /.controls -->
			    </div> <!-- /.control-group -->
                <div class="form-actions save-profile" ng-class="{'light-yellow':infoEdit.$dirty && submitStatus == -1, 'light-blue':!infoEdit.$dirty && submitStatus == -1, 'light-green':submitStatus == 0, 'light-red':submitStatus == 1}">
                    <input type="submit" class="btn btn-warning" ng-class="{'disabled':!infoEdit.$dirty}" value="Save changes" ng-click="submitProfileEdit()"></input>
                    <span class="help-inline" ng-show="!infoEdit.$dirty && submitStatus == -1" ng-cloak>No Changes</span>
                    <span class="help-inline" ng-show="infoEdit.$dirty && submitStatus == -1" ng-cloak>Unsaved Changes</span>
                    <span class="help-inline" ng-show="submitStatus == 0" ng-cloak>Successfully saved changes</span>
                    <span class="help-inline" ng-show="submitStatus == 1" ng-cloak>Error saving changes</span>
                </div>
                </fieldset>
	        </form>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="profilePicture()">
    ## ng-init here is hacky and unclean
     <div class="section-wrapper" ng-init="code='${c.user['urlCode']}'; url='${c.user['url']}'">
        <div class="browse">
            <h4 class="section-header smaller">Add or Change Your Pictures</h4>
            <form class="form-horizontal" id="setImageSourceForm" name="setImageSourceForm">
                <div class="control-group">
                    <label class="control-label" for="avatarType">
                        ${lib_6.userImage(c.user, className="avatar avatar-small", forceSource="gravatar")}
                    </label>
                    <div class="controls chooseAvatar">
                        <label class="radio">
                            <input type="radio" value="gravatar" name="avatarType" id="avatarType" ng-click="uploadImage = false" ng-model="imageSource">
                                Use your 
                                <a href="http://gravatar.com" target="_blank">gravatar</a> 
                                image
                            </input>
                        </label>
                    </div>
                </div>
                <div class="control-group">
                    <label class="control-label" for="avatarType">
                        ${lib_6.userImage(c.user, className="avatar avatar-small", forceSource="civ")}
                    </label>
                    <div class="controls chooseAvatar">
                        <label class="radio">
                            <input type="radio" value="civ" name="avatarType" id="avatarType" ng-click="uploadImage = true" ng-model="imageSource">
                                Use your uploaded image
                            </input>
                        </label>
                    </div>
                </div>
                <div class="form-actions save-profile" ng-class="{'light-yellow':setImageSourceForm.$dirty && submitStatus == -1, 'light-blue':!setImageSourceForm.$dirty && submitStatus == -1, 'light-green':submitStatus == 0, 'light-red':submitStatus == 1}">
                    <input type="submit" class="btn btn-warning" ng-class="{'disabled':!setImageSourceForm.$dirty}" value="Save changes" ng-click="setImageSource()"></input>
                    <span class="help-inline" ng-show="!setImageSourceForm.$dirty && submitStatus == -1" ng-cloak>No Changes</span>
                    <span class="help-inline" ng-show="setImageSourceForm.$dirty && submitStatus == -1" ng-cloak>Unsaved Changes</span>
                    <span class="help-inline" ng-show="submitStatus == 0" ng-cloak>Successfully saved changes</span>
                    <span class="help-inline" ng-show="submitStatus == 1" ng-cloak>Error saving changes</span>
                </div>
            </form>
            <form id="fileupload" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/picture/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="uploadImage">
                <!-- Redirect browsers with JavaScript disabled to the origin page -->
                <noscript>&lt;input type="hidden" name="redirect" value="http://blueimp.github.com/jQuery-File-Upload/"&gt;</noscript>
                <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
                <div class="row-fluid fileupload-buttonbar">
                    <div class="span10 offset1">
                        <!-- The fileinput-button span is used to style the file input field as button -->
                        <span class="btn btn-success fileinput-button span6 offset3">
                            <i class="icon-plus icon-white"></i>
                            <span>Select your picture</span>
                            <input type="file" name="files[]">
                        </span>
                        <!-- The loading indicator is shown during file processing -->
                        <div class="fileupload-loading"></div>
                    </div>
                    <!-- The global progress information -->
                </div>
                <div class="row-fluid">
                    <div class="span10 offset1 fade" data-ng-class="{true: 'in'}[!!active()]">
                        <!-- The global progress bar -->
                        <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                        <!-- The extended global progress information -->
                        <div class="progress-extended">&nbsp;</div>
                    </div>
                </div>
                <!-- The table listing the files available for upload/download -->
                <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">
                    <tbody><tr data-ng-repeat="file in queue">
                        <td data-ng-switch="" on="!!file.thumbnail_url">
                            <div class="preview" data-ng-switch-when="true">
                                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"></a>
                            </div>
                            <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>
                        </td>
                        <td>
                            <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">
                                <i class="icon-upload icon-white"></i>
                                <span>Start</span>
                            </button>
                            <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel">
                                <i class="icon-ban-circle icon-white"></i>
                                <span>Cancel</span>
                            </button>
                        </td>
                    </tr>
                </tbody></table>
            </form>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="profileMessages()">
    <table class="table table-condensed table-hover">
        <thead>
            <th>Sender</th>
            <th>Message</th>
        </thead>
        % for message in c.messages:
            <%
                rowClass = ''
                if message['read'] == u'0':
                    rowClass = 'warning unread-message'
            %>
            <tr class = "${rowClass}" data-code="${message['urlCode']}">
                <%
                    if message['sender'] == u'0':
                        sender = 'Civinomics'
                    else:
                        sender = userLib.getUserByCode(message['sender'])
                %>
                <td class="message-avatar">
                    % if sender == 'Civinomics':
                        <img src="/images/handdove_medium.png" title="Civinomics" alt="Civinomics">
                        <p>Civinomics</p>
                    % else:
                        ${lib_6.userImage(sender, className="avatar")}
                        <p>${lib_6.userLink(sender)}</p>
                    % endif
                </td>
                <td class="message-content"> 
                    % if 'extraInfo' in message.keys():
                        % if message['extraInfo'] in ['listenerInvite', 'facilitationInvite']:
                            <% 
                                workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                                if message['extraInfo'] == 'listenerInvite':
                                    formStr = """<form method="post" name="inviteListener" id="inviteListener" action="/profile/%s/%s/listener/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                    action = 'be a listener for'
                                    role = listenerLib.getListenerByCode(message['listenerCode'])
                                else:
                                    formStr = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                    action = 'facilitate'
                                    role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                            %>
                            % if message['read'] == u'1':
                                <%
                                    # Since this is tied to the individual message, we will only have one action
                                    # The query here should be rewritten to make use of map/reduce for a single query
                                    event = eventLib.getEventsWithAction(message, 'accepted')
                                    if not event:
                                        responseAction = 'declining'
                                    else:
                                        responseAction = 'accepting'
                                %>
                                <div class="media">
                                    ${lib_6.workshopImage(workshop, linkClass="pull-left message-workshop-image")}
                                    <div class="media-body">
                                        <h4 class="media-heading centered">${message['title']}</h4>
                                        <p>${lib_6.userLink(sender)} invites you to facilitate <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a></p>
                                        <p>${message['text']}</p>
                                        <p>(You have already responded by ${responseAction})</p>
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
                        % elif message['extraInfo'] in ['commentResponse']:
                            <%
                                comment = commentLib.getCommentByCode(message['commentCode'])
                                workshop = workshopLib.getWorkshopByCode(comment['workshopCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p><a ${lib_6.thingLinkRouter(comment, workshop, embed=True, commentCode=comment['urlCode']) | n} class="green green-hover">${comment['data']}</a></p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['disabled', 'enabled', 'deleted', 'adopted']:
                            <%
                                event = eventLib.getEventsWithAction(message, message['extraInfo'])
                                if not event:
                                    continue
                                event = event[0]
                                
                                # Mako was bugging out on me when I tried to do this with sets
                                codeTypes = ['commentCode', 'discussionCode', 'ideaCode', 'resourceCode']
                                thing = None
                                for codeType in codeTypes:
                                    if codeType in message.keys():
                                        thing = generic.getThing(message[codeType])
                                        break
                                if thing is None:
                                    continue
                                workshop = generic.getThing(thing['workshopCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p>It was ${event['action']} because: ${event['reason']}</p>
                                    <p>You posted:
                                    % if thing.objType == 'comment':
                                        <a ${lib_6.thingLinkRouter(thing, workshop, embed=True, commentCode=thing['urlCode']) | n} class="green green-hover">${thing['data']}</a>
                                    % else:
                                        <a ${lib_6.thingLinkRouter(thing, workshop, embed=True) | n} class="green green-hover">${thing['title']}</a>
                                    % endif
                                    </p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % endif
                    % endif
                </td>
            </tr>
        % endfor
    </table>
</%def>

<%def name="changePassword()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Change Your Password</h4>
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

<%def name="preferences()">
    <% 
        commentsChecked = ''
        if 'commentAlerts' in c.user and c.user['commentAlerts'] == '1':
            commentsChecked = 'checked'
    %>
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Preferences</h4>
            <div class="row-fluid">
                <div class="span3">Email when:</div>
                <div class="span6">
                    <form ng-init="code='${c.user['urlCode']}'; url='${c.user['url']}'" class="no-bottom form-inline">
                        New comments added to my items: <input type="checkbox" name="commentAlerts" value="comments" ng-click="emailOnComments()" ${commentsChecked}>
                        <span ng-show="emailOnCommentsShow">{{emailOnCommentsResponse}}</span>
                    </form>
                </div><!-- span6 -->
            </div><!-- row-fluid -->
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
