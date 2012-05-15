<%inherit file="/base/base.mako" />

<h1>${c.heading}</h1>

${h.form(h.url(controller='attach', action='upload'),  method='post', multipart=True)}

${h.file('userfile')}

<br><br>

Optional remark: <input type="text" id="remark"  name="remark" class="text tiny" placeholder="optional remark" />
<input type="text" id="sremark"  name="sremark" class="text" />
${h.submit('upload','Upload')}

${h.end_form()}

<br><br>

<div>

<b>Use this form to upload attachments to the wiki.</b>

</div>
