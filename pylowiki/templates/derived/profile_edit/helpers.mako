<%def name="profileInfo()">
	<form action="/profile/editSubmit" enctype="multipart/form-data" method="post" class="form-horizontal">
		<fieldset>
			<legend>Basic Information</legend>
			<div class="control-group">
				<label for="member-name" class="control-label">Name:</label>
				<div class="controls">
					<input type="text" id="member-name" name="member_name" value="${c.authuser['name']}">
					<span class="help-inline"><span class="label label-important">Required</span></span>
				</div> <!-- /.controls -->
			</div> <!-- /.control-group -->
			<div class="control-group">
				<label for="email" class="control-label">Email:</label>
				<div class="controls">
					<input type="text" id="email" name="email" value="${c.authuser['email']}">
					<span class="help-inline"><span class="label label-important">Required</span></span>
				</div> <!-- /.controls -->
			</div> <!-- /.control-group -->
		</fieldset>
        <fieldset>
            <legend>Change Password</legend>
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
					% if 'tagline' in c.authuser.keys():
						<input type="text" id="tagline" name="tagline" value="${c.authuser['tagline']}">
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
