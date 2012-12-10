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
