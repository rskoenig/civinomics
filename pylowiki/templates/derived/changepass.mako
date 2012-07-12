<%inherit file="/base/base.mako" />

<h1>${c.heading}</h1>

${h.form(h.url(controller='login', action='changepass_handler'), method='post')}

<table class="padding"><tr><td>
    New password:
</td><td>
    <input type="password" id="password1" name="password1" class="text tiny" placeholder="new password"/>
</td></tr>
<tr><td>
    Re-enter password:
</td><td>
    <input type="password" id="password2" name="password2" class="text tiny" placeholder="confirm password"/>
    <input type="submit" id="changepass" name="changepass" class="tiny" value="change password" />
    
<input type="text" id="sremark"  name="sremark" class="text" />
</td></tr></table>

${h.end_form()}
