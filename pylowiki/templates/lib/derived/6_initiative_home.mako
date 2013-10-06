<%!
    import pylowiki.lib.db.user         as userLib
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
