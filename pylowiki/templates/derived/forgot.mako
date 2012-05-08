<%inherit file="/base/base.mako" />

<h1>${c.heading}</h1>

${h.form(h.url(controller='login', action='forgot_handler'), method='post')}

    Email: <input type="email" id="email" name="email" class="text tiny" placeholder="address for account" />
    <input type="text" id="sremark"  name="sremark" class="text" />
    ${h.submit('register', 'Send new password')}

${h.end_form()}
