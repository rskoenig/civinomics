<%inherit file="/base/base.mako" />

<h2 style="color: #E7B01E;">Revision ${c.r.id} was made on ${c.r.event.date} by ${c.r.event.user.name}</h2>

<span style="color: #E7B01E;">Would you like to <a href="/revert/${c.r.id}">revert</a> to this revision?</span>

<br><br>


<div style="width: 100%; overflow:auto; padding: 1px; background-color: white;color: black;">
${c.diff}
</div>

<br>

${c.content}
