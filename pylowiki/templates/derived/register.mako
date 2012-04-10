<%inherit file="/base/base.mako" />

<h1>${c.heading}</h1>

${h.form(h.url(controller='register', action='register_handler'), method='post')}

<table ><tr><td>
    Choose a username:   
</td><td>
    <input type="text" id="username" name="username" class="text tiny" />
</td></tr>
<tr><td>
    Choose a password:
</td><td>
    <input type="password" id="passowrd" name="password" class="text tiny" />
</td></tr>
<tr><td>
    Re-enter password:
</td><td>
    <input type="password" id="passowrd2" name="password2" class="text tiny" />
</td></tr>
<tr><td>
    Email address:
</td><td>
    <input type="text" id="email" name="email" class="text tiny" />
</td></tr>
<tr><td>
    <input type="text" id="sremark"  name="sremark" class="text tiny" />
    Submit:
</td><td>
    <input type="submit" id="register" name="register" class="tiny" value="Register" />
</td></tr></table>

${h.end_form()}
