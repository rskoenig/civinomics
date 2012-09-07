
<%def name="add()">
    <h2 class="civ-col"><i class="icon-folder-open"></i> Add Discussion Topic</h2>
    <br />
    <form id="add_discussion" action = "${c.site_secure_url}/newDiscussion/${c.w['urlCode']}/${c.w['url']}" class="form-vertical" method = "post">
    <%
        linkValue = ''
        titleValue = ''
        commentValue = '' 
    %>
                    
    <div class="control-group">
        <label class="control-label"><strong>Discussion Title:</strong></label>
        <div class="controls docs-input-sizes">
            <input type="text" id="discussiontitle" name = "title" value="${titleValue}"/>
        </div><!-- controls -->
    </div><!-- control-group -->

    <div class="control-group">
        <label class="control-label"><strong>Additional Information:</strong></label>
        <label class="control-label">Additional text to introduce the subject being discussed</label>
        <div class="controls docs-input-sizes">
            <textarea id="discussiontext" name="text" rows=8 cols=50 onkeyup="previewAjax( 'resourcetext', 'resource-preview-div' )" class="markitup">${commentValue}</textarea>
            <div id="resource-preview-div"></div>
        </div><!-- controls -->
    </div><!-- control-group -->
    <div class="form-actions">
        <button type="submit" class="btn btn-success">Submit</button>
    </div><!-- form-action -->
    </fieldset>
    </form>
</%def>

<%def name="edit()">
    <h2 class="civ-col"><i class="icon-folder-open"></i> Edit Discussion Topic</h2>
    </br>
    <form id="edit_discussion" action = "${c.site_secure_url}/editDiscussionHandler/${c.discussion['urlCode']}/${c.discussion['url']}" class="form-vertical" method = "post">
    <% titleValue = c.discussion['title'] %>
    <% commentValue = c.discussion['text'] %>

    <div class="control-group">
        <label class="control-label"><strong>Discussion Title:</strong></label>
        <div class="controls docs-input-sizes">
            <input type="text" id="discussiontitle" name = "title" value="${titleValue}"/>
        </div><!-- controls -->
    </div><!-- control-group -->
    <div class="control-group">
        <label class="control-label"><strong>Additional Information:</strong></label>
        <label class="control-label">Additional text to introduce the subject being discussed</label>
        <div class="controls docs-input-sizes">
            <textarea id="discussiontext" name="text" rows=8 cols=50 onkeyup="previewAjax( 'resourcetext', 'resource-preview-div' )" class="markitup">${commentValue}</textarea>
            <div id="resource-preview-div"></div>
        </div><!-- controls -->
    </div><!-- control-group -->
    <div class="form-actions">
        <button type="submit" class="btn btn-success">Save Changes</button>
    </div><!-- form-actions -->
    </fieldset>
</form>

</%def>
