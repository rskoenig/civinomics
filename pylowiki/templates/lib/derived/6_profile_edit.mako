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

<%def name="editProfile()">
    <%namespace file="/lib/derived/6_profile_edit.mako" name="helpersEdit" />
    <%
        tab1active = ""
        tab2active = ""
        tab3active = ""
        tab4active = ""
        tab5active = ""
        tab6active = ''
        prefactive = ''
        linkactive = ''
                    
        if c.tab == "tab1":
            tab1active = "active"
        elif c.tab == "tab2":
            tab2active = "active"
        elif c.tab == "tab3":
            tab3active = "active"
        elif c.tab == "tab4":
            tab4active = "active"
        elif c.tab == "tab5":
            tab5active = "active"
        elif c.tab == 'tab6':
            tab6active = 'tab6'
        else:
            tab1active = "active"
    
        msgString = ''
        if c.unreadMessageCount != 0:
            msgString = ' (' + str(c.unreadMessageCount) + ')'
    %>
    <div class="row">
        % if c.conf['read_only.value'] == 'true':
            <h1> Sorry, Civinomics is in read only mode right now </h1>
        % else:
            <div class="tabbable">
                <div class="col-sm-2">
                    ${lib_6.userImage(c.user, className="avatar avatar-large")}
                    <div>
                        <ul class="nav nav-pills nav-stacked workshop-menu">
                            <li class="${tab1active}"><a href="#tab1" data-toggle="tab">1. Info
                            </a></li>
                            <li class="${tab6active}"><a href="#tab6" data-toggle="tab">2. Picture
                            </a></li>
                            <li class="${tab4active}"><a href="#tab4" data-toggle="tab">3. Password
                            </a></li>
                            <li class="${prefactive}"><a href="#pref" data-toggle="tab">4. Preferences
                            </a></li>
                            <li class="${linkactive}"><a href="#link" data-toggle="tab">5. Sharing
                            </a></li>
                            % if c.admin:
                            <li class="${tab5active}"><a href="#tab5" data-toggle="tab">6. Administrate
                            Admin only - shhh!.</a></li>
                            % endif
                        </ul>
                    </div>
                </div> <!-- /.col-sm-2 -->
                <div class="col-sm-10">
                    <ul class="nav nav-tabs" id="editTabs">
                        <li class="active"><a href="#tab-edit" data-toggle="tab" class="green green-hover">Edit Profile</a></li>
                        <li class="pull-right"><a href="/profile/${c.user['urlCode']}/${c.user['url']}">Back to Profile</a></li>
                    </ul>
                    ${lib_6.fields_alert()}
                    % if c.conf['read_only.value'] == 'true':
                        <!-- read only -->
                    % else:
                        <div class="tab-content">
                            <div class="tab-pane ${tab1active}" id="tab1">
                                ${helpersEdit.profileInfo()}
                            </div><!-- tab1 -->
                            <div class="tab-pane ${tab4active}" id="tab4">
                                ${helpersEdit.changePassword()}
                            </div><!-- tab4 -->
                            <div class="tab-pane ${tab6active}" id="tab6">
                                ${helpersEdit.profilePicture()}
                            </div><!-- tab6 -->
                            <div class="tab-pane ${prefactive}" id="pref">
                                ${helpersEdit.preferences()}
                            </div><!-- preferences -->
                            <div class="tab-pane ${linkactive}" id="link">
                                ${helpersEdit.linkAccounts()}
                            </div><!-- sharing -->
                            % if c.admin:
                                <div class="tab-pane ${tab5active}" id="tab5">
                                    ${helpersEdit.memberAdmin()}
                                    ${helpersEdit.memberEvents()}
                                </div><!-- tab5 -->
                            % endif
                        </div><!-- tab-content -->
                    % endif
                </div> <!-- /.col-sm-9 -->
            </div><!-- tabbable -->
        % endif
    </div> <!-- /.row -->
</%def>

<%def name="profileInfo()">
    <div class="section-wrapper">
        <div class="browse">
	        <form id="infoEdit" name="infoEdit" class="form-horizontal edit-profile">
    		    <h4 class="section-header smaller">Update Your Profile Information</h4>
                <fieldset>
			    <div ng-class=" {'form-group': true, 'error': infoEdit.member_name.$error.pattern} ">
				    <div class="col-xs-12">
                        <label for="member-name" class="control-label">Your Name:</label>
					    <input type="text" id="member-name" class="col-sm-10 form-control" name="member_name" value="${c.user['name']}" ng-model="fullName" ng-init="fullName='${c.user['name']}'" ng-pattern="fullNameRegex" required>
                        <span class="error help-block" ng-show="infoEdit.member_name.$error.pattern">Use only letters, numbers, spaces, and _ (underscore)</span>
				    </div> <!-- /.col-xs-12 -->
			    </div> <!-- /.form-group -->
                <div class="form-group">
                    <div class="col-xs-12">
                        <label for="greetingMsg" class="control-label">Short bio:</label>
                        <input class="form-control" type="text" name="greetingMsg" ng-model="greetingMsg" ng-init="greetingMsg='${c.user['greetingMsg']}'" rows=4 class="col-sm-10">
                        <span class="help-block">Displayed with your posts (e.g. Thomas Jefferson, 3rd President of the United States; Founding Father; Principle Author, Declaration of Independence )</span>
                    </div> <!-- /.col-xs-12 -->
                </div> <!-- /.form-group -->
                <div class="form-group">
                    <div class="col-xs-12">
                        <label for="orgLink" class="control-label">Your website:</label>
                        <input type="text" class="col-sm-10 form-control" name="websiteLink" ng-model="websiteLink" ng-init="websiteLink='${c.user['websiteLink']}'">
                    </div> <!-- /.col-xs-12 -->
                </div> <!-- /.form-group -->
                <!--
                <div class="form-group">
                    <div class="col-xs-12">
                        <label for="orgLinkMsg" class="control-label">A description of your website:</label>
                        <textarea name="websiteDesc" ng-model="websiteDesc" ng-init="websiteDesc='${c.user['websiteDesc']}'" rows=4 class="col-sm-10 form-control"></textarea>
                    </div> 
                </div>
                -->
			    <div class="form-group">
				    <div class="col-xs-12">
                        <label for="email" class="control-label">Email:</label>
					    <input type="text" id="email" class="col-sm-10 form-control" name="email" ng-model="email" ng-init="email='${c.user['email']}'" required>
				    </div> <!-- /.col-xs-12 -->
			    </div> <!-- /.form-group -->
                <div ng-class=" {'form-group': true, 'error': infoEdit.postalCode.$error.pattern} ">
                    <div class="col-xs-12">
                        <label for="postalCode" class="control-label">Postal code:</label>
					    <input type="text" id="postalCode" class="col-sm-5 form-control" name="postalCode form-control" onBlur="geoCheckPostalCode()" ng-model="postalCode" ng-init="postalCode='${c.user['postalCode']}'" ng-pattern="postalCodeRegex" required>
                        <br />
                        <span class="error help-block" ng-show="infoEdit.postalCode.$error.pattern">Use only numbers.</span>
                        <span id="postalCodeResult"></span>
				    </div> <!-- /.col-xs-12 -->
			    </div> <!-- /.form-group -->

                <div class="form-group">
                    <div class="col-xs-12">
                        <% 
                            memberType = 'Individual'
                            if c.user['memberType'] == 'organization':
                                memberType = 'Organization'
                        %>
                        <label for="member-name" class="control-label">Membership Type:</label> ${memberType}<br>

                        % if c.user['memberType'] != 'organization' and not c.privs['provisional']:

                            <div class="panel-group" id="accordion">
                                <a data-toggle="collapse" data-parent="#accordion" href="#changeToOrg" class="btn btn-default top-space-md" data-toggle="modal">Change to Organization</a>

                                <div id="changeToOrg" class="panel-collapse collapse">
                                  <div class="panel-body">
                                    <p>Organizations are special types of members:</p>
                                    <ul>
                                        <li>Organizations can post featured position statements.</li>
                                        <!--<li>Members can post topics or ideas about an organization that other members can vote on.</li>-->
                                        <li>Organization get easy to remember Civinomics addresses: civinomics.com/YourOrganization</li>
                                        <li>Organizations are listed as a separate category in search results</li>
                                        <li>Organizations can't vote, sorry.</li>
                                    </ul>
                                    <a href="/profile/${c.user['urlCode']}/${c.user['url']}/organization/upgrade/handler" class="btn btn-primary">Change to Organization</a>
                                  </div>
                                </div>
                            </div>


                            <div id="upgradeOrg" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="upgradeOrgLabel" aria-hidden="true">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                                    <h3 id="myModalLabel">Change to Organization</h3>
                                </div>
                                <div class="modal-body">
                                    
                                </div>
                                <div class="modal-footer">
                                    <button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>
                                    
                                </div>
                            </div>
                        % endif
                    </div>
                </div> <!-- /.form-group -->

                <div class="form-actions save-profile" ng-class="{'light-yellow':infoEdit.$dirty && submitStatus == -1, 'light-blue':!infoEdit.$dirty && submitStatus == -1, 'light-green':submitStatus == 0, 'light-red':submitStatus == 1}">
                    <input type="submit" class="btn btn-warning btn-lg" ng-class="{'disabled':!infoEdit.$dirty}" value="Save changes" ng-click="submitProfileEdit()"></input>
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
                % if 'facebookAuthId' in c.user.keys():
                    <div class="form-group">
                        <label class="control-label" for="avatarType">
                            ${lib_6.userImage(c.user, className="avatar avatar-small", forceSource="facebook")}
                        </label>
                        <div class="col-xs-12 chooseAvatar">
                            <label class="radio">
                                <input type="radio" value="facebook" name="avatarType" id="avatarType" ng-click="uploadImage = false" ng-model="imageSource">
                                    Use your facebook image
                                </input>
                            </label>
                        </div>
                    </div>
                % endif
                
                <div class="form-group">
                    <div class="col-xs-12 chooseAvatar">
                        <label class="col-sm-3" for="avatarType">
                            ${lib_6.userImage(c.user, className="avatar avatar-small", forceSource="gravatar")}
                        </label>
                        <label class="radio col-sm-9">
                            <input type="radio" value="gravatar" name="avatarType" id="avatarType" ng-click="uploadImage = false" ng-model="imageSource">
                                Use your 
                                <a href="http://gravatar.com" target="_blank">gravatar</a> 
                                image
                            </input>
                        </label>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-xs-12 chooseAvatar">
                        <label class="col-sm-3" for="avatarType">
                            ${lib_6.userImage(c.user, className="avatar avatar-small", forceSource="civ")}
                        </label>
                        <label class="col-sm-9 radio">
                            <input type="radio" value="civ" name="avatarType" id="avatarType" ng-click="uploadImage = true" ng-model="imageSource">
                                Use your uploaded image
                            </input>
                        </label>
                    </div>
                </div>
                <div class="form-actions save-profile" ng-class="{'light-yellow':setImageSourceForm.$dirty && submitStatus == -1, 'light-blue':!setImageSourceForm.$dirty && submitStatus == -1, 'light-green':submitStatus == 0, 'light-red':submitStatus == 1}">
                    <input type="submit" class="btn btn-warning btn-lg" ng-class="{'disabled':!setImageSourceForm.$dirty}" value="Save changes" ng-click="setImageSource()"></input>
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
                <div id="fileupload-button-div" class="row fileupload-buttonbar collapse in">
                    <div class="col-sm-10 col-sm-offset-1">
                        <!-- The fileinput-button span is used to style the file input field as button -->
                        <span class="btn btn-success btn-lg fileinput-button span6 offset3" data-toggle="collapse" data-target="#fileupload-button-div">
                            <i class="icon-plus icon-white"></i>
                            <span>Select your picture</span>
                            <input type="file" name="files[]">
                        </span>
                        <!-- The loading indicator is shown during file processing -->
                        <div class="fileupload-loading"></div>
                    </div>
                    <!-- The global progress information -->
                </div>
                <div class="row">
                    <div class="col-sm-10 col-sm-offset-1 fade" data-ng-class="{true: 'in'}[!!active()]">
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
                                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"> New profile photo uploaded.</a>
                            </div>
                            <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>
                        </td>
                        <td>
                            <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary btn-lg start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">
                                <i class="icon-upload icon-white"></i>
                                <span>Start</span>
                            </button>
                            <button type="button" class="btn btn-warning btn-lg cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel" data-toggle="collapse" data-target="#fileupload-button-div">
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

<%def name="changePassword()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Update Your Password</h4>
            <form action="/profile/${c.user['urlCode']}/${c.user['url']}/password/update/handler" enctype="multipart/form-data" method="post" class="form-horizontal">
		    <fieldset>
            <div class="form-group">
                <div class="col-xs-12">
                    <label for="oldPassword" class="control-label">Old Password:</label>
                    <input class="form-control" type="password" id="oldPassword" name="oldPassword">
                    <span class="help-inline"> If you reset your password, this is the random string you received via email.</span>
                </div> <!-- /.col-xs-12 -->
            </div> <!-- /.form-group -->
            <div class="form-group">
                <div class="col-xs-12">
                    <label for="newPassword" class="control-label">New Password:</label>
                    <input class="form-control" type="password" id="newPassword" name="newPassword">
                </div> <!-- /.col-xs-12 -->
            </div> <!-- /.form-group -->
            <div class="form-group">
                <div class="col-xs-12">
                    <label for="reNewPassword" class="control-label">Repeat New Password:</label>
                    <input class="form-control" type="password" id="reNewPassword" name="reNewPassword">
                </div> <!-- /.col-xs-12 -->
            </div> <!-- /.form-group -->
            <div class="form-group">
                <div class="col-xs-12">
                    <button type="submit" class="btn btn-warning btn-lg" name="submit">Save Changes</button>
                </div> <!-- /.col-xs-12 -->
            </div> <!-- /.form-group -->
            </fieldset>
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
            <div class="row">
                <div class="col-sm-3">Email when:</div>
                <div class="col-sm-6">
                    <form ng-init="code='${c.user['urlCode']}'; url='${c.user['url']}'" class="no-bottom form-inline">
                        New comments added to my items: <input type="checkbox" name="commentAlerts" value="comments" ng-click="emailOnComments()" ${commentsChecked}>
                        <span ng-show="emailOnCommentsShow">{{emailOnCommentsResponse}}</span>
                    </form>
                </div><!-- col-sm-6 -->
            </div><!-- row -->
        </div><!-- browse -->
    </div><!-- section-wrapper-->
</%def>

<%def name="linkAccounts()">
    <% 
        facebookChecked = ''
        twitterChecked = ''
        if 'facebookAuthId' in c.user:
            facebookChecked = 'checked'
        if 'twitterAuthId' in c.user:
            twitterChecked = 'checked'
    %>
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Social Network Sharing</h4>
            <div class="row">
                <div class="col-sm-3">Facebook account:</div>
                <div class="col-sm-6">
                    % if facebookChecked == 'checked':
                        Email registered with facebook:
                        <input class="form-control" type="text" id="fbEmail" class="col-sm-10" name="fbEmail" ng-model="fbEmail" ng-init="fbEmail='${c.user['fbEmail']}'" required>
                    % else:
                        Account not connected with facebook.
                    % endif
                </div><!-- col-sm-6 -->
            </div><!-- row -->
            <div class="row">
                <div class="col-sm-3">Twitter account:</div>
                <div class="col-sm-6">
                    % if twitterChecked == 'checked':
                        Email registered with twitter:
                        <input class="form-control" type="text" id="email" class="col-sm-10" name="email" ng-model="email" ng-init="email='${c.user['email']}'" required>
                    % else:
                        Account not connected with twitter.
                    % endif
                </div><!-- col-sm-6 -->
            </div><!-- row -->
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
                <div class="form-group">
                    <label for="enable" class="control-label">Reason for ${eAction}</label>
                    <div class="col-xs-12">
                        <input class="form-control" type="text" name="enableUserReason">
                        <input type="radio" name="verifyEnableUser" value="0"> Verify ${eAction}
                        &nbsp;&nbsp;<button type="submit" class="btn btn-warning">${eAction} Member</button>
                    </div> <!-- /.col-xs-12 -->
                </div> <!-- /.form-group -->
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
            <div class="form-group">
                <label for="setPrivs" class="control-label">Reason for Change</label>
                <div class="col-xs-12">
                    <input class="form-control" type="text" name="accessChangeReason">
                    <input type="radio" name="accessChangeVerify" value="0"> Verify Change
                    &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Change Access</button>
                </div> <!-- /.col-xs-12 -->
            </div> <!-- /.form-group -->
            </fieldset>
            </form>
            <br /><br />
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>
