<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.tag          as tagLib
    import pylowiki.lib.db.generic      as genericLib
    import pylowiki.lib.utils           as utils
    import misaka as m

    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    
    import logging
    log = logging.getLogger(__name__)

    from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showAuthorSimple(item)">
    <%
        showNum = 3
        remaining = len(c.authors) - showNum
    %>
    <span class="grey">
    Added by:
    % for author in c.authors[:showNum]:
        % if author != c.authors[0] and len(c.authors) >= 3:
            ,
        % endif
        % if author == c.authors[-1] and len(c.authors) > 1:
            and
        % endif
        ${lib_6.userLink(author)}
    % endfor
    % if remaining >= 1:
        , and <a href="#allAuthors" data-toggle="tab">${remaining} more.</a>
    % endif
    </span>
    <span class="grey">${item['fuzzyTime']} ago</span>
</%def>

<%def name="showAuthor(item)">
    <div class="tabbable">
        <div class="tab-content">
            <div class="tab-pane active" id="abrv">
                <table>
                    <tr>
                        <%
                            showNum = 3
                            remaining = len(c.authors) - showNum
                        %>
                        <td>
                            <span class="grey">Added by: </span>
                            % for author in c.authors[:showNum]:
                                ${lib_6.userImage(author, className="avatar small-avatar")}
                            % endfor
                        </td>
                        <td>
                            <span class="grey">
                            % for author in c.authors[:showNum]:
                                % if author != c.authors[0] and len(c.authors) >= 3:
                                    ,
                                % endif
                                % if author == c.authors[-1] and len(c.authors) > 1:
                                    and
                                % endif
                                ${lib_6.userLink(author)}
                            % endfor
                            % if remaining >= 1:
                                , and <a href="#allAuthors" data-toggle="tab">${remaining} more.</a>
                            % endif
                            </span>
                            <span class="grey">${item['fuzzyTime']} ago</span>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="tab-pane" id="allAuthors">
                <span class="pull-right">
                    <a href="#abrv" data-toggle="tab">close</a>
                </span>
                <h4 class="initiative-title">
                    Authors
                </h4>
                <table>
                    % for author in c.authors:
                        <tr>
                            <td>
                                ${lib_6.userImage(author, className="avatar small-avatar")}
                            </td>
                            <td>
                                <span class="grey">
                                    ${lib_6.userLink(author)}
                                    ${lib_6.userGreetingMsg(author)}
                                </span>
                            </td>
                        </tr>
                    % endfor
                </table>            
            </div><!-- tab-pane -->
        </div><!-- tabcontent -->
    </div><!-- tabbable -->
</%def>

<%def name="showUpdateList()">
    % if len(c.updates) <= 0:
        <div class="alert alert-info top-space-md">
            There are no updates yet.
        </div>
    % else:
        % for update in c.updates:
            <ul>
                <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/updateShow/${update['urlCode']}">${update['title']} <span class="pull-right">${update.date}</span></a></li>
            </ul>
        % endfor
    % endif
</%def>
                        

<%def name="showDescription()">
    <!--<h2 class="no-top">Summary</h2>-->
    <div class="initiative-summary">
        ${m.html(c.summary) | n}
    </div>
</%def>

<%def name="showFunding_Summary()">
    <div class="initiative-info">
        ${m.html(c.initiative['funding_summary']) | n}
    </div>
</%def>


<%def name="showBackground()">
    <div class="initiative-info">
        ${m.html(c.initiative['background']) | n}
    </div>
</%def>

<%def name="showProposal()">
    <div class="initiative-info">
        ${m.html(c.initiative['proposal']) | n}
    </div>
</%def>

<%def name="watchButton(i, **kwargs)">
    % if 'user' in session:
        % if c.isFollowing or 'following' in kwargs:
            <button class="btn btn-success followButton following" data-URL-list="initiative_${i['urlCode']}_${i['url']}" id="initiativeBookmark">
            <span><i class="icon-bookmark"></i><strong> Following </strong></span>
            </button>
        % else:
            <button class="btn btn-default followButton" data-URL-list="initiative_${i['urlCode']}_${i['url']}" id="initiativeBookmark">
             <span><i class="icon-bookmark med-green"></i><strong> Follow </strong></span>
            </button>
        % endif
    % endif
</%def>

<%def name="addResourceButton()">
    <% 
        printStr = ''
        if c.initiative.objType == 'initiative':
            if 'user' in session:
                printStr = '<a id="addButton" href="/initiative/%s/%s/resourceEdit/new"' %(c.initiative['urlCode'], c.initiative['url'])
            elif not c.privs['provisional']:
                printStr = '<a href="#signupLoginModal" data-toggle="modal"'

            printStr += ' title="Click to add a resource to this initiative" class="btn btn-default btn-sm pull-right"><i class="icon icon-plus"></i></a>'
            
            if 'user' in session and c.privs['provisional']:
                printStr = ''
        
    %>
    ${printStr | n}
</%def>



<%def name="addUpdateButton()">
    % if c.iPrivs:
        <a class="btn btn-default btn-sm pull-right" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/updateEdit/new"><i class="icon icon-plus"></i></a>
    % endif
</%def>

<%def name="listResources()">
    % if len(c.resources) <= 0:
        <div class="alert alert-info top-space-md">
            There are no links yet! Be the first to add one.
        </div>
    % else:
        % for item in c.resources:
            <% 
                iconClass = ""
                if 'type' not in item:
                    iconClass="icon-link"
                elif item['type'] == 'link' or item['type'] == 'general':
                    iconClass="icon-link"
                elif item['type'] == 'photo':
                    iconClass="icon-picture"
                elif item['type'] == 'video':
                    iconClass="icon-youtube-play"
                elif item['type'] == 'rich':
                    iconClass="icon-file"
                endif
                rURL = "/initiative/" + c.initiative['urlCode'] + "/" + c.initiative['url'] + "/resource/" + item['urlCode'] + "/" + item['url']
            %>
            <div class="row bottom-space-med">
                <div class="col-sm-1">
                        <i class="${iconClass} icon-3x"></i>
                </div><!-- col-sm-1 -->
                <div class="col-sm-11">
                    <h5 class="no-bottom no-top">
                    <% itemTitle = '<a href="%s" class="listed-item-title">%s</a>' %(rURL, lib_6.ellipsisIZE(item['title'], 150)) %>
                    ${itemTitle | n}
                    </h5>
                    <a href="${item['link']}" target="_blank">${lib_6.ellipsisIZE(item['link'], 150)}</a>
                </div><!-- col-sm-10 -->
            </div><!-- row -->
        % endfor
    % endif
</%def>

<%def name="showResource()">
        <% 
            link = ""
            rURL = "/initiative/" + c.initiative['urlCode'] + "/" + c.initiative['url'] + "/resource/" + c.thing['urlCode'] + "/" + c.thing['url']
            title = '<a href="%s" class="listed-item-title">%s</a>' %(rURL, c.thing['title'])
            if c.thing.objType == 'resource':
                    link = '<small>(<a href=%s target=_blank>%s</a>)</small>' %(c.thing['link'], lib_6.ellipsisIZE(c.thing['link'], 75))
                    if 'type' in c.thing:
                        if c.thing['type'] == 'rich' or c.thing['type'] == 'video':
                            link = link + '<div class="spacer"></div>' + c.thing['info']
                        if c.thing['type'] == 'photo':
                            link = link + '<div class="spacer"></div><img src="' + c.thing['info'] + '">'
        %>
        <h4>${title | n}</h4>
        ${link | n}
        ${m.html(c.thing['text']) | n}
                % if c.revisions:
            <div class="spacer"></div>
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/initiative/${revision['initiativeCode']}/${revision['initiative_url']}/resource/${revision['urlCode']}/${revision['url']}">${revision.date}</a></li>
            % endfor
            </ul>
        % endif
        % if c.thing.objType == 'revision':
            This is a revision dated ${c.thing.date}<br />
        % endif
</%def>

<%def name="listInitiative(item, ltitle)">
    <div class="media profile-workshop">
        <a class="pull-left" href="/initiative/${item['urlCode']}/${item['url']}/show">
        % if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
            <% thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos']) %>
        % else:
            <% thumbnail_url = "/images/icons/generalInitiative.jpg" %>
        % endif
        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${thumbnail_url}); background-size: cover; background-position: center center;"></div>
        </a>
        <div class="media-body">
            <div class="col-sm-10">
                <a href="/initiative/${item['urlCode']}/${item['url']}/show" class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
                <br>
                <span class="grey">Initiative for</span> ${lib_6.showScope(item) | n}
                % if 'user' in session:
                    % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                        % if item['public'] == '0':
                            <span class="badge badge-warning">Not yet public</span>
                        % else:
                            <span class="badge badge-success">Public</span>
                        % endif
                    % endif
                % endif
            </div>
             % if ltitle == 'Bookmarked':
                <span>
                  ${watchButton(item, following = True)}
                </span>
            % else:
                % if 'user' in session:
                    % if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                        <div class="row" ng-controller="followerController">
                            <div class="col-sm-9"></div>
                            <div class="col-sm-3">
                                <a class="btn btn-default pull-right" href="/initiative/${item['urlCode']}/${item['url']}/edit"><strong>Edit Initiative</strong></a> &nbsp;
                            </div><!-- col-sm-3 -->
                        </div><!-- row -->
                    % endif
                % endif
            % endif
        </div><!-- media-body -->
    </div><!-- media -->
</%def>

<%def name="initiativeModerationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision' or c.privs['provisional']:
            return
        flagID = 'flag-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group pull-right">
        % if thing['disabled'] == '0' and thing.objType != 'initiativeUnpublished':
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'initiativeUnpublished':
            <a class="btn btn-default  btn-sm accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">unpublish</a>
        % elif thing.objType == 'initiativeUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-default  btn-sm accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-default btn-sm accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif
    </div>
    
    % if thing['disabled'] == '0':
        % if thing.objType != 'initiativeUnpublished':
            ${lib_6.flagThing(thing)}
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
            % if thing.objType == 'initiativeUnpublished':
                ${lib_6.publishThing(thing)}
            % else:
                ${lib_6.unpublishThing(thing)}
            % endif
            % if userLib.isAdmin(c.authuser.id):
                ${lib_6.adminThing(thing)}
            % endif
        % endif
    % else:
        % if userLib.isAdmin(c.authuser.id):
            ${lib_6.adminThing(thing)}
        % endif
    % endif
    % if c.revisions:
        <div id="revisions" class="collapse text-right">
            <br>
            <br>
            <ul class="unstyled">
            % for revision in c.revisions:
                <li>Revision: <a href="/initiative/${revision['urlCode']}/${revision['url']}/show">${revision.date}</a></li>
            % endfor
            </ul>
        </div>
    % endif
</%def>

<%def name="editResource()">
    <%
        if not c.resource:
            resourceTitle = ""
            resourceLink = ""
            resourceText = ""
        else:
            resourceTitle = c.resource['title']
            resourceLink = c.resource['link']
            resourceText = c.resource['text']
            
    %>
    % if not c.resource:
        <form ng-controller="resourceController" ng-init="rType = 'initiative'; parentCode = '${c.initiative['urlCode']}'; parentURL = '${c.initiative['url']}'; addResourceURLResponse=''; addResourceResponse='';"  id="addResourceForm" name="addResourceForm" ng-submit="submitResourceForm(addResourceForm)">
            <div class="form-group">
                <label>Resource title</label>
                <input type="text" class="input-block-level form-control" name="title" ng-model="title" maxlength = "120" required>
                <span class="help-block">Try to keep your title informative, but concise.</span>
                <span ng-show="addResourceTitleShow"><div class="alert alert-danger" ng-cloak>{{addResourceTitleResponse}}</div></span>
            </div>
            <div class="form-group">
                <label>Resource URL</label>
                <input type="url" class="input-block-level form-control" name="link" ng-model="link" placeholder="http://" required>
                <span ng-show="addResourceURLShow"><div class="alert alert-danger" ng-cloak>{{addResourceURLResponse}}</div></span>
            </div>
            <div class="form-group">
                <label><strong>Additional information</strong>
                <a href="#" class="btn btn-xs btn-info left-space" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>
                <textarea name="text" rows="3" class="input-block-level form-control" ng-model="text"></textarea>
                <span class="help-block">Any additional information you want to include.  This is optional.</span>
            </div>
            <span ng-show="addResourceShow">{{addResourceResponse}}</span>
            <div class="form-group">
                <button class="btn btn-lg btn-success pull-right" type="submit" name="submit">Submit</button>
            </div>
        </form>
    % endif
</%def>

<%def name="editUpdate()">
    <%
        if not c.update:
            updateTitle = ""
            updateText = ""
            updateCode = "new"
        else:
            updateTitle = c.update['title']
            updateText = c.update['text']
            updateCode = c.update['urlCode']
            
    %>
    % if not c.update:
        <form ng-controller="updateController" ng-init="parentCode = '${c.initiative['urlCode']}'; parentURL = '${c.initiative['url']}'; updateCode = '${updateCode}'; addUpdateTitleResponse=''; addUpdateTextResponse=''; addUpdateResponse='';"  id="addUpdateForm" name="addUpdateForm" ng-submit="submitUpdateForm(addUpdateForm)">
            <div class="form-group">
                <label>Update Title</label>
                <input type="text" class="form-control input-block-level" name="title" ng-model="title" maxlength = "120" required>
                <span ng-show="addUpdateTitleShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTitleResponse}}</div></span>
            </div>
            <div class="form-group">
                <label>Update Text</label>
                <a href="#" class="btn btn-xs btn-info left-space" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a>
                <textarea name="text" rows="3" class="form-control input-block-level" ng-model="text" required></textarea>
                <span ng-show="addUpdateTextShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTextResponse}}</div></span>
            </div>
            <div class="form-group">
                <button class="btn btn-lg btn-success pull-right" type="submit" name="submit">Submit</button>
            </div>
        </form>
    % endif
</%def>

<%def name="showCost(item)">
    <% 
        currency = '$'
        cost = int(item['cost']) 
        if cost <= -1:
            cost = cost * -1
            currency = '- $'
    %>
    <div class="row">
        <h4 class="initiative-title">
            <div class="col-sm-6 pull-left grey">
                Cost Estimate
            </div>
            <div class="col-sm-6">
                <table class="pull-right">
                    <tr>
                        <td>${currency}</td>
                        <td>${locale.format("%d", cost, grouping=True)}</td>
                    <tr>
                </table>
            </div>
        </h4>
    </div>
</%def>
