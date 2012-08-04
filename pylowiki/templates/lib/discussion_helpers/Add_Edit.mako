
<%def name="add()">
    <div class="row-fluid">
        <div class="span10">
            <h2 class="civ-col">ADD DISCUSSION TO <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/">${c.title}</a></h2>
        </div>
    </div>
    </br>
    <div class="row">
        <div class="span2"></div>
        <div class="span4">
                <form id="add_discussion" action = "${c.site_secure_url}/newDiscussion/${c.w['urlCode']}/${c.w['url']}" class="form-vertical" method = "post">
                    <% linkValue = '' %>
                    <% titleValue = '' %>
                    <% commentValue = '' %>
                    
                    <div class="control-group">
                        <label class="control-label"><strong>Discussion Title:</strong></label>
                        ##<label class="control-label">Keep the title short and informative as possible.</label>
                        <div class="controls docs-input-sizes">
                            <input type="text" id="discussiontitle" name = "title" value="${titleValue}"/>
                        </div>
                    </div>

                    <div class="control-group">
                        <label class="control-label"><strong>Additional Information:</strong></label>
                        <label class="control-label">Additional text to introduce the subject being discussed</label>
                        <div class="controls docs-input-sizes">
                            <textarea id="discussiontext" name="text" rows=8 cols=50 onkeyup="previewAjax( 'resourcetext', 'resource-preview-div' )" class="markitup">${commentValue}</textarea>
                            <div id="resource-preview-div"></div>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success">Submit</button>
                    </div>
                </fieldset>
            </form>
        </div>
    </div>
</%def>

<%def name="edit()">
    <div class="row-fluid">
        <div class="span10">
            <h2 class="civ-col">EDIT DISCUSSION <a href="#"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/discussion/${c.discussion['urlCode']}/${c.discussion['url']}">${c.discussion['title']}</a> IN <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/">${c.w['title']}</a></h2>
        </div>
    </div>
    </br>
    <div class="row">
        <div class="span2"></div>
        <div class="span4">
                <form id="edit_discussion" action = "${c.site_secure_url}/editDiscussionHandler/${c.discussion['urlCode']}/${c.discussion['url']}" class="form-vertical" method = "post">
                    <% titleValue = c.discussion['title'] %>
                    <% commentValue = c.discussion['text'] %>
                    
                    <div class="control-group">
                        <label class="control-label"><strong>Discussion Title:</strong></label>
                        ##<label class="control-label">Keep the title short and informative as possible.</label>
                        <div class="controls docs-input-sizes">
                            <input type="text" id="discussiontitle" name = "title" value="${titleValue}"/>
                        </div>
                    </div>
                    <div class="control-group">
                        <label class="control-label"><strong>Additional Information:</strong></label>
                        <label class="control-label">Additional text to introduce the subject being discussed</label>
                        <div class="controls docs-input-sizes">
                            <textarea id="discussiontext" name="text" rows=8 cols=50 onkeyup="previewAjax( 'resourcetext', 'resource-preview-div' )" class="markitup">${commentValue}</textarea>
                            <div id="resource-preview-div"></div>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success">Submit</button>
                    </div>
                </fieldset>
            </form>

        </div>
    </div>
</%def>