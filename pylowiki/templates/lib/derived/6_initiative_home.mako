<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showInfo()">
    <div>
    % if c.information and 'data' in c.information:
        <p>
        This introduction was written and is maintained by the initiative author.
        You are encouraged to add links to additional information resources.
        </p>
        ${m.html(c.information['data'], render_flags=m.HTML_SKIP_HTML) | n}
    % endif
    </div>
</%def>

<%def name="watchButton()">
    % if 'user' in session:
        % if c.isFollowing:
            <button class="btn round btn-civ pull-right followButton following" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark">
            <span><i class="icon-bookmark icon-white pull-left"></i> Bookmarked </span>
            </button>
        % else:
            <button class="btn round pull-right followButton" data-URL-list="workshop_${c.w['urlCode']}_${c.w['url']}" rel="tooltip" data-placement="bottom" data-original-title="this workshop" id="workshopBookmark">
             <span><i class="icon-bookmark pull-left"></i> Bookmark </span>
            </button>
        % endif
    % endif
</%def>

<%def name="newInitiative()">
    <% tagList = workshopLib.getWorkshopTagCategories() %>
    <h4 class="section-header smaller">New Initiative</h4>
    <form method="POST" action="/profile/${c.user['urlCode']}/${c.user['url']}/saveInitiativeHandler">
        <div class="row-fluid">
            <div class="span8">
                <fieldset>
                <label for="title" class="control-label" required>Initiative Title:</label>
                <input type="text" name="title" value="">
                <label for="description" class="control-label" required>Short Description:</label>
                <input type="text" name="description" value="">
                <label for="scope" class="control-label" required>This initiative is for:</label>
                <input type="radio" name="scope" value="zipcode"> My Zip Code<br />
                <input type="radio" name="scope" value="city" checked> My City<br />
                <input type="radio" name="scope" value="county"> My County<br />
                
            </div><!-- span8 -->
            <div class="span4">
                <label for="categoryTags" class="control-label" required>Category Tags:</label>
                % for tag in tagList:
                    <label class="checkbox"><input type="checkbox" name="categoryTags" value="${tag}" /> ${tag}</label>
                % endfor
            </div><!-- span4 -->
        </div><!-- row-fluid -->
        <div class="spacer"></div>
        <div class="row-fluid">
            <fieldset>
            <label for="title" class="control-label" required>Background Info: <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
               <textarea rows="10" id="data" name="data" class="span12"></textarea>
               <div class="background-edit-wrapper">
               </div><!-- background-edit-wrapper -->
            </form>
            <div class="preview-information-wrapper" id="live_preview">
               hi
            </div><!-- preview-information-wrapper -->
            </fieldset>
        </div><!-- row-fluid -->
        <button type="submit" class="btn btn-warning pull-left" name="submit">Save Changes</button>
    </form>
</%def>