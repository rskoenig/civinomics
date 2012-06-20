<%inherit file="/base/base.mako"/>

<h1>${c.heading}</h1>

${h.form(h.url(controller='contact', action='handler'), method='put')}
<table>
<tr><td>To:</td><td> 
${h.mail_to(c.conf['contact.email'], encode = 'hex')}
</td></tr>
<tr><td>From:</td><td> 
<input type="email" id="from_email"  name="from_email" class="text tiny" placeholder="full email address" />
</tr></td>
<tr><td>Subject:</td><td> 
<input type="text" id="subject"  name="subject" class="text tiny" placeholder="message subject" />
</tr></td>
</table>
<center>
${h.textarea('message', rows=18)}
</center>
<!-- <input type="text" id="sremark"  name="sremark" /> -->
${h.submit('submit', 'Send Email', onClick='emailAlert()')}
${h.end_form()}
<center><font size='1px'>
${h.mail_to(c.conf['contact.email'], encode = 'hex')} will never sell your Personal Information or Email Address.  All Information is confidential and is <u>only</u> used to reply back.
</font></center>
		

