<%inherit file="/base/base.mako" />

<h1>${c.heading}</h1>

${h.form(h.url(controller='login', action='index'), method='post')}
    Email
    <input type="text" id="email" name="email" class="text tiny" placeholder="email"/>
    
    <br />
    Password
    <input type="password" id="passowrd" name="password" class="text tiny" placeholder="password"/>
    <input type="text" id="sremark" name="sremark" class="text tiny" />
    <input type="submit" id="login" name="login" class="tiny" value="Login" />

${h.end_form()}

<h3 class="utility">
    <a href="/login/forgot">Forgot</a> your password? 
</h3>

% if c.conf['public.reg'] == 'true':
<h3 class="utility">
    <a href="/register">Register</a> an account? 
</h3>
% endif
