<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m
    
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showInfo()">
    <div>
    <h4>Introduction</h4>
    <p>
    This introduction was written and is maintained by the initiative author.
    You are encouraged to add links to additional information resources.
    </p>
    ${m.html(c.initiative['background'], render_flags=m.HTML_SKIP_HTML) | n}
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

<%def name="iResources()">
    Resources go here
</%def>

<%def name="listInitiative(item)">
    <div class="media profile-workshop">
        <a class="pull-left" href="/initiative/${item['urlCode']}/${item['url']}/show">
        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url("/images/slide/thumbnail/supDawg.thumbnail"); background-size: cover; background-position: center center;"></div>
        </a>
        <div class="media-body">
            <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
            % if 'user' in session:
                % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    <a href="/initiative/${item['urlCode']}/${item['url']}/edit">Edit</a>
                % endif
            % endif
        </div><!-- media-body -->
    </div><!-- media -->
</%def>

<%def name="editInitiative()">
    <% 
        tagList = workshopLib.getWorkshopTagCategories()
        initiativeTags = c.initiative['tags'].split('|')
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        scopeList = c.initiative['scope'].split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    <div class="spacer"></div>
    <div class="row-fluid">
        <span class="pull-left"><h4>Edit Initiative</h4></span>
        <span class="pull-right"><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/show">View Initiative</a></span>
    </div><!-- row-fluid -->
    <div class="spacer"></div>
    
    <form method="POST" action="/profile/${c.user['urlCode']}/${c.user['url']}/saveInitiativeHandler">
        <div class="row-fluid">
            <div class="span8">
                <fieldset>
                <label for="title" class="control-label" required>Initiative Title:</label>
                <input type="text" name="title" value="${c.initiative['title']}">
                <label for="description" class="control-label" required>Short Description:</label>
                <input type="text" name="description" value="${c.initiative['description']}">
                <label for="scope" class="control-label" required>This initiative is for:</label>
                <select name="scope" id="scope">
                <option value="postalCode" ${postalCodeSelected}> My Zip Code</option>
                <option value="city" ${citySelected}> My City</option>
                <option value="county" ${countySelected}> My County</option>
                </select>
                </fieldset>
                <label for="tag" class="control-label" required>Initiative category:</label>
                <select name="tag" id="tag">
                <option value="choose">Choose one</option>
                % for tag in tagList:
                    <% 
                        selected = ""
                        if tag in initiativeTags:
                            selected = "selected"
                    %>
                    <option value="${tag}" ${selected}/> ${tag}</option>
                % endfor
                </select>
                <label for="background" class="control-label" required>Background Info: <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                <textarea rows="10" id="data" name="data" class="span12"></textarea>
                <div class="background-edit-wrapper">
                </div><!-- background-edit-wrapper -->
                <div class="preview-information-wrapper" id="live_preview">
                </div><!-- preview-information-wrapper -->
            </div><!-- span8 -->
            <div class="span4">
            picture goes here
            </div><!-- span4 -->
        </div><!-- row-fluid -->
        <button type="submit" class="btn btn-warning pull-left" name="submit">Save Changes</button>
    </form>
</%def>