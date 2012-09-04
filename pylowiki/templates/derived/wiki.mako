<%inherit file="/base/base.mako"/>

##This allows certain controllers to return_to previous url
<%namespace file="/lib/mako_lib.mako" import="return_to" />
<%namespace file="/derived/comments.mako" import="comments" />
${return_to()}

<% counter = 0 %>

${ h.form( url( controller = "wiki", action ='handler', id = c.url ), method='put' ) }

% for row in c.wikilist:
<div id="wiki-section-break">
<% numrows = len(row[1].split( "\r\n" )) %>
    <table style="width: 100%; padding: 0px; border-spacing: 0px; border: 0px; margin: 0px;"><tr><td>
    <div id = "section${counter}" ondblclick="toggle('textareadiv${counter}', 'edit${counter}')">${row[0]}</div>
    </td></tr></table>

    <div style="display:none; text-align:center;" id="textareadiv${counter}">
        <br />
        <textarea rows="${numrows}" id="textarea${counter}" name="textarea${counter}" onkeyup="previewAjax( 'textarea${counter}', 'section${counter}' )" class="markitup">${row[1]}</textarea>
        <div style="align:right;text-align:right;">
            Optional remark: <input type="text" id="remark${counter}"  name="remark${counter}" class="text tiny" placeholder="optional remark"/> 

<!-- <input type="submit" id="cancel" name="cancel" value="Cancel" class="tiny">
$<input type="submit" id="submit" value="Save" class="tiny"> -->
${h.submit('submit', 'Save')}
            <input type="text" id="sremark"  name="sremark" class="text" />
        </div>
    </div>

    <div style="align:right;text-align:right;"><a href="javascript: toggle('textareadiv${counter}', 'edit${counter}', 'edit')" id="edit${counter}" style="font-size: 12px;">edit</a></div>
</div>
<% counter += 1 %>
% endfor

${h.hidden("count",counter)}

${h.end_form()}

<div class="lastmodified"><br/>${c.url} <i>(last modified ${c.lastmoddate} by ${c.lastmoduser})</i></div>
${comments()}

${h.form(h.url(controller = 'wiki', action = 'readThisArticle'), method = 'post')}
    <input type = "submit" value = "I Read This +1" />
${h.end_form()}
