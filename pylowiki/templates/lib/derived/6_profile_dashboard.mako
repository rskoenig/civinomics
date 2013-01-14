<%!
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.facilitator      as facilitatorLib
    import pylowiki.lib.db.listener         as listenerLib
    import pylowiki.lib.db.workshop         as workshopLib
%> 

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

<%def name="profilePhoto()">
    <div class="section-wrapper">
        <div class="browse">
    	    <h4 style="text-align: center" class="section-header"><br />Update Your Profile Picture</h4>
            <form id="fileupload" action="/profile/${c.user['urlCode']}/${c.user['url']}/picture/upload/handler" enctype="multipart/form-data" method="post" class="form-horizontal">
                % if c.user['pictureHash'] != 'flash':
                    Current profile photo:
                    <img src="/images/avatar/${c.user['directoryNumber']}/profile/${c.user['pictureHash']}.profile" alt="${c.user['name']}" title="${c.user['name']}" width="120px">
                    <br /><br />            
                % endif
                <div class="row fileupload-buttonbar">
                    <div class="span1">
                    </div>
                    <div class="span10">
                        <!-- The fileinput-button span is used to style the file input field as button -->
                        <span class="btn btn-success fileinput-button">
                            <i class="icon-plus icon-white"></i>
                            <span>Upload new picture</span>
                            <input type="file" name="pictureFile">
                        </span>
                        </button>
                    </div><!-- span10 -->
                </div><!-- file upload button bar -->
                <!-- The loading indicator is shown during image processing -->
                <div class="fileupload-loading"></div>
                <br>
                <!-- The table listing the files available for upload/download -->
                <table class="table"><tbody class="files" data-toggle="modal-gallery" data-target="#modal-gallery"></tbody></table>
	        </form>
        </div><!-- browse -->
    </div><!-- section-wrapper -->
    <!-- modal-gallery is the modal dialog used for the image gallery -->
    <div id="modal-gallery" class="modal modal-gallery hide fade">
        <div class="modal-header">
            <a class="close" data-dismiss="modal">&times;</a>
            <h3 class="modal-title"></h3>
        </div><!-- modal-header -->
        <div class="modal-body"><div class="modal-image"></div></div>
        <div class="modal-footer">
            <a class="btn modal-download" target="_blank">
                <i class="icon-download"></i>
                <span>Download</span>
            </a>
            <a class="btn btn-success modal-play modal-slideshow" data-slideshow="5000">
                <i class="icon-play icon-white"></i>
                <span>Slideshow</span>
            </a>
            <a class="btn btn-info modal-prev">
                <i class="icon-arrow-left icon-white"></i>
                <span>Previous</span>
            </a>
            <a class="btn btn-primary modal-next">
                <span>Next</span>
                <i class="icon-arrow-right icon-white"></i>
            </a>
        </div><!-- modal-footer -->
    </div><!-- modal-gallery -->
    <script id="template-upload" type="text/x-tmpl">
    {% for (var i=0, file; file=o.files[i]; i++) { %}
        <tr class="template-upload fade">
            <td class="preview"><span class="fade"></span></td>
            <td class="name"><span>{%=file.name%}</span></td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            {% if (file.error) { %}
                <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
            {% } else if (o.files.valid && !i) { %}
                <td>
                    <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>
                </td>
                <td class="start">{% if (!o.options.autoUpload) { %}
                    <button class="btn btn-primary">
                        <i class="icon-upload icon-white"></i>
                        <span>{%=locale.fileupload.start%}</span>
                    </button>
                {% } %}</td>
            {% } else { %}
                <td colspan="2"></td>
            {% } %}
            <td class="cancel">{% if (!i) { %}
                <button class="btn btn-warning">
                    <i class="icon-ban-circle icon-white"></i>
                    <span>{%=locale.fileupload.cancel%}</span>
                </button>
            {% } %}</td>
        </tr>
    {% } %}
    </script>
    <!-- The template to display files available for download -->
    <script id="template-download" type="text/x-tmpl">
    {% for (var i=0, file; file=o.files[i]; i++) { %}
        <tr class="template-download fade">
            {% if (file.error) { %}
                <td></td>
                <td class="name"><span>{%=file.name%}</span></td>
                <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
                <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
            {% } else { %}
                <td class="preview">{% if (file.thumbnail_url) { %}
                    <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>
                {% } %}</td>
                <td class="name">
                    <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&'gallery'%}" download="{%=file.name%}">{%=file.name%}</a>
                </td>
                <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
                <td colspan="2"></td>
            {% } %}
            <td class="delete">
                <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                    <i class="icon-trash icon-white"></i>
                    <span>{%=locale.fileupload.destroy%}</span>
                </button>
                <input type="checkbox" name="delete" value="1">
            </td>
        </tr>
    {% } %}
    </script>
</%def>

<%def name="profileMessages()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Notifications & Invitations</h4>
            % if c.pendingFacilitators and c.authuser.id == c.user.id:
                ${pendingFacilitateInvitations()}
            % elif c.pendingListeners and c.authuser.id == c.user.id:
                ${pendingListenerInvitations()}
            % else:
                No messages today!
            % endif
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
    <form method="post" name="userPrivs" id="userPrivs" class="form-horizontal" action="/profile/${c.user['urlCode']}/${c.user['url']}/privs/">
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
</%def>

<%def name="pendingFacilitateInvitations()">
    <div class="well">
        <strong>Invitations to CoFacilitate Workshops</strong><br />
        <% fNum = len(c.pendingFacilitators) %>
        <% wNum = 0 %>
        % for f in c.pendingFacilitators:
            % if wNum % 6 == 0 or wNum == 0: ## begin a new row
                <ul class="unstyled civ-block-list">
            % elif wNum % 6 == 5: ## end a row
                </ul>
                <ul class="unstyled civ-block-list">
            % endif
            <li>
            <% workshop = workshopLib.getWorkshopByID(f['workshopID']) %>
            <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/${c.user['urlCode']}/${c.user['url']}/facilitate/response/handler/">
            <input type="hidden" name="workshopCode" value="${workshop['urlCode']}">
            <input type="hidden" name="workshopURL" value="${workshop['url']}">
            % if workshop['mainImage_hash'] == 'supDawg':
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
            % else:
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
            % endif
            <br /> <br />
            <button type="submit" name="acceptInvite" class="btn btn-mini btn-success" title="Accept the invitation to cofacilitate the workshop">Accept</button>
            <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to cofcilitate the workshop">Decline</button>
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
            % if workshop['mainImage_hash'] == 'supDawg':
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}">${workshop['title']}</a>
            % else:
                <a href="/workshops/${workshop['urlCode']}/${workshop['url']}"><img src="/images/${workshop['mainImage_identifier']}/${workshop['mainImage_directoryNum']}/thumbnail/${workshop['mainImage_hash']}.thumbnail" alt="mtn" class="block" style = "margin: 5px; width: 120px; height: 80px;"/><br>
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

