<%!
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.workshop     as workshopLib
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
                        % for author in c.authors[:showNum]:
                            <td>
                                ${lib_6.userImage(author, className="avatar small-avatar")}
                            </td>
                        % endfor
                        <td>
                            <span class="grey">Authored by
                            % for author in c.authors[:showNum]:
                                % if author != c.authors[0] and len(c.authors) >= 3:
                                    ,
                                % endif
                                % if author == c.authors[-1]:
                                    and
                                % endif
                                ${lib_6.userLink(author)}
                                ${lib_6.userGreetingMsg(author)}
                            % endfor
                            % if remaining >= 1:
                                , and <a href="#allAuthors" data-toggle="tab">${remaining} more.</a>
                            % endif
                            </span>
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
    <%
        if 'views' in item:
            numViews = str(item['views'])
        else:
            numViews = "0"
    %>
    Published on ${item.date} <i class="icon-eye-open"></i> Views ${numViews}
</%def>

<%def name="showUpdateList()">
    % if c.updates:
        Progress Reports:<br />
        <ul>
        % for update in c.updates:
            <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/updateShow/${update['urlCode']}">${update.date} ${update['title']}</a></li>
        % endfor
        </ul>
    % endif
</%def>
                        

<%def name="showDescription()">
    <div class="initiative-info">
        ${m.html(c.initiative['description'], render_flags=m.HTML_SKIP_HTML) | n}
    </div>
</%def>

<%def name="showFunding_Summary()">
    <div class="initiative-info">
        ${m.html(c.initiative['funding_summary'], render_flags=m.HTML_SKIP_HTML) | n}
    </div>
</%def>


<%def name="showBackground()">
    <div class="initiative-info">
        ${m.html(c.initiative['background'], render_flags=m.HTML_SKIP_HTML) | n}
    </div>
</%def>

<%def name="showProposal()">
    <div class="initiative-info">
        ${m.html(c.initiative['proposal'], render_flags=m.HTML_SKIP_HTML) | n}
    </div>
</%def>

<%def name="watchButton(i, **kwargs)">
    % if 'user' in session:
        % if c.isFollowing or 'following' in kwargs:
            <button class="btn btn-civ pull-right followButton following" data-URL-list="initiative_${i['urlCode']}_${i['url']}" rel="tooltip" data-placement="bottom" data-original-title="this initiative" id="initiativeBookmark">
            <span><i class="icon-bookmark btn-height icon-light"></i><strong> Bookmarked </strong></span>
            </button>
        % else:
            <button class="btn pull-right followButton" data-URL-list="initiative_${i['urlCode']}_${i['url']}" rel="tooltip" data-placement="bottom" data-original-title="this initiative" id="initiativeBookmark">
             <span><i class="icon-bookmark med-green"></i><strong> Bookmark </strong></span>
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
            else:
                printStr = '<a href="#signupLoginModal" data-toggle="modal"'

            printStr += ' title="Click to add a resource to this initiative" class="btn btn-success btn-mini pull-right right-space"><i class="icon icon-plus"></i></a>'
        
    %>
    ${printStr | n}
</%def>

<%def name="listResources()">
    % if len(c.resources) <= 0:
        <div class="alert alert-info">
            There are no resources yet! Be the first to add one.
        </div>
    % else:
        % for item in c.resources:
            <% 
                iconClass = ""
                if item['type'] == 'link' or item['type'] == 'general':
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
            <div class="row-fluid bottom-space-med">
                <div class="span1">
                        <i class="${iconClass} icon-3x"></i>
                </div><!-- span1 -->
                <div class="span11">
                    <h5 class="no-bottom no-top">
                    <% itemTitle = '<a href="%s" class="listed-item-title">%s</a>' %(rURL, lib_6.ellipsisIZE(item['title'], 150)) %>
                    ${itemTitle | n}
                    </h5>
                    <a href="${item['link']}" target="_blank">${lib_6.ellipsisIZE(item['link'], 150)}</a>
                </div><!-- span10 -->
            </div><!-- row-fluid -->
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
            <div class="span10">
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
                        <div class="row-fluid" ng-controller="followerController">
                            <div class="span3">Email when:</div>
                            <div class="span3">
                                x
                            </div><!-- span3 -->
                            <div class="span3">
                                x
                            </div><!-- span3 -->
                            <div class="span3">
                                <a class="btn pull-right" href="/initiative/${item['urlCode']}/${item['url']}/edit"><strong>Edit Initiative</strong></a> &nbsp;
                            </div><!-- span3 -->
                        </div><!-- row-fluid -->
                    % endif
                % endif
            % endif
        </div><!-- media-body -->
    </div><!-- media -->
</%def>

<%def name="editInitiative()">
    <% 
        tagList = workshopLib.getWorkshopTagCategories()
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.initiative:
            iScope = c.initiative['scope']
        else:
            iScope = "0|0|0|0|0|0|0|0|0|0"
        scopeList = iScope.split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"

    %>
    % if c.saveMessage and c.saveMessage != '':
        <div class="alert ${c.saveMessageClass}">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        ${c.saveMessage}
        </div>
    % endif
    <div class="row-fluid edit-initiative" id="basics">
        <div class="span12">
        <form method="POST" name="edit_initiative_summary" id="edit_initiative_summary" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler" ng-controller="initiativeCtrl" ng-init="cost = '${c.initiative['cost']}'">
            <div class="row-fluid">
                <h3 class="initiative-title edit no-top">1. Basics</h3>
            </div><!-- row-fluid -->
            <br>
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Initiative Title:</strong></label>
                    <input type="text" name="title" class="span12" ng-model="initiativeTitle" value="{{initiativeTitle}}" ng-click="clearTitle()" ng-cloak>
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        Keep it short and descriptive. 10 words or less.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <div class="row-fluid">
                <div class="span6">
                    <label for="title" class="control-label" required><strong>Geographic Region:</strong></label>
                    ${geoSelect()}
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The region or legal jurisdiction associated with your initiative.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <div class="row-fluid">
                <div class="span6">
                    <label for="tag" class="control-label" required><strong>Initiative category:</strong></label>
                    <div class="span3"></div>
                    <div class="span8 no-left">
                        <select name="tag" id="tag">
                        % if c.initiative['public'] == '0':
                            <option value="">Choose one</option>
                        % endif
                        % for tag in tagList:
                            <% 
                                selected = ""
                                if c.initiative['tags'] == tag:
                                    selected = "selected"
                            %>
                            <option value="${tag}" ${selected}/> ${tag}</option>
                        % endfor
                        </select>
                    </div><!-- span8 -->
                </div><!-- span6 -->
                <div class="span6">
                    <div class="alert alert-info">
                        The topic area associated with your initiative.
                    </div><!-- alert -->
                </div><!-- span6 -->
            </div><!-- row-fluid -->
            <div class="row-fluid" id="summary">
                <h3 class="initiative-title edit">2. Summary</h3>
            </div><!-- row-fluid -->
            <br>
            <div class="row-fluid">
                <div class="span6">
                    <label for="description" class="control-label" required><strong>Summary:</strong></label>
                    <textarea rows="8" type="text" name="description" class="span12">${c.initiative['description']}</textarea>
                </div>
                <div class="span6">
                    <div class="alert alert-info">
                        Used in search listings and displayed at the top of your initiative.
                    </div>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span6">
                    <label for="funding_summary" class="control-label" required><strong>Estimate Net Fiscal Impact:</strong></label>
                    <textarea rows="8" type="text" name="funding_summary" class="span12">${c.initiative['funding_summary']}</textarea>
                </div>
                <div class="span6">
                    <label class="control-label"></label>
                    <div class="alert alert-info">
                        What are the costs and benefits of your intiative? What will you have to spend money on? What will the fiscal impacts be for the associated region? For example, if your intiative will lead to increased tax revenues for your City, mention that here.
                    </div>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span6">
                    <label for="description" class="control-label" required><strong>Cost Estimate:</strong></label>
                    <div class="input-prepend input-append">
                      <span class="add-on">$</span>
                      <input type="text" name="cost" value="{{cost}}" ng-model="cost" ng-pattern="costRegex">
                      <span class="add-on">.00</span>
                    </div>
                    <span class="error help-text" ng-show="edit_initiative_summary.cost.$error.pattern" ng-cloak>Invalid cost value</span>
                </div>
                <div class="span6">
                    <label class="control-label"></label>
                    <div class="alert alert-info">
                        Acceptable formats include: 500,000  or  500000.
                    </div>
                </div>
            </div>
            <div class="row-fluid" id="detail">
                <h3 class="initiative-title edit">3. Detail</h3>
            </div><!-- row-fluid -->

            <div class="row-fluid">
                <div class="span3">
                    <label for="background" class="control-label" required><strong>Background:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span9">
                    <div class="alert alert-info">
                        What are the conditions that make this initaitive needed? Cite statistics and existing policies or programs in the effected region wherever possible.
                    </div>
                </div>
            </div>
            <textarea rows="10" id="background" name="background" class="span12">${c.initiative['background']}</textarea>

            <div class="row-fluid">
                <div class="span3">
                    <label for="proposal" class="control-label" required><strong>Proposal:</strong></label>
                    ${lib_6.formattingGuide()}
                </div>
                <div class="span9">
                    <div class="alert alert-info">
                        What are the details of your initiative? How will it work? What will it do? What won't it do? Address the financial impacts as well.
                    </div>
                </div>
            </div>
            <textarea rows="10" id="proposal" name="proposal" class="span12">${c.initiative['proposal']}</textarea>
            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>
        </form>
        <div class="row-fluid" id="photo">
            <h3 class="initiative-title edit">4. Photo</h3>
        </div><!-- row-fluid -->
        <form id="fileupload" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: 'fileupload-processing'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">
            <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">
                <!-- The fileinput-button span is used to style the file input field as button -->
                %if 'directoryNum_photos' in c.initiative and 'pictureHash_photos' in c.initiative:
                    <% thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos']) %>
                    <span class="pull-left">Current Initiative Picture
                    <div class="spacer"></div>
                    <img src="${thumbnail_url}">
                    </span>
                % else:
                    <span class="pull-left">Upload a Picture (Required)</span>
                % endif
                <span class="btn btn-success btn-large fileinput-button pull-right"  data-toggle="collapse" data-target="#fileinput-button-div">
                <i class="icon-plus icon-white"></i>
                <span>Picture</span>
                <input type="file" name="files[]">
                </span>
                <!-- The loading indicator is shown during file processing -->
                <div class="fileupload-loading"></div>
                <!-- The global progress information -->
            </div><!-- row-fluid -->
            <div class="row-fluid">
                <div class="span10 offset1 fade" data-ng-class="{true: 'in'}[!!active()]">
                    <!-- The global progress bar -->
                    <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                    <!-- The extended global progress information -->
                    <div class="progress-extended">&nbsp;</div>
                </div><!-- span10 -->
            </div><!-- row-fluid -->
            <!-- The table listing the files available for upload/download -->
            <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">
                <tbody><tr data-ng-repeat="file in queue">
                    <td data-ng-switch="" on="!!file.thumbnail_url">
                        <div class="preview" data-ng-switch-when="true">
                            <script type="text/javascript">
                                function setAction(imageHash) {
                                    actionURL = "/profile/${c.user['urlCode']}/${c.user['url']}/photo/" + imageHash + "/update/handler";
                                    document.getElementById('fileupload').action = actionURL;
                                }
                            </script>
                            <div class="row-fluid">
                                <img src="{{file.thumbnail_url}}">
                                New Picture Uploaded and Saved
                                <a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/editHandler" class="btn btn-warning btn-large pull-right" name="submit_photo">Save Changes</a>
                            </div><!-- row-fluid -->
                            </form>

                        </div><!-- preview -->
                        <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>
                            </td>
                            <td>
                                <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>
                            </td>
                            <td>
                                <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">
                                <i class="icon-upload icon-white"></i>
                                <span>Save</span>
                                </button>
                                <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">
                                <i class="icon-ban-circle icon-white"></i>
                                <span>Cancel</span>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </form>

        ${coAuthorInvite()}
    </div><!-- span12 -->
</div>
</%def>

<%def name="initiativeModerationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
    %>
    <div class="btn-group">
        % if thing['disabled'] == '0' and thing.objType != 'initiativeUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
        % endif
        % if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'initiativeUnpublished':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">unpublish</a>
        % elif thing.objType == 'initiativeUnpublished' and thing['unpublished_by'] != 'parent':
            % if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${publishID}">publish</a>
            % endif
        % endif
        % if c.revisions:
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (${len(c.revisions)})</a>
        % endif

        % if userLib.isAdmin(c.authuser.id):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
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
        <div id="revisions" class="collapse">
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
            <fieldset>
                <label>Resource title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>
                <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>
                <span ng-show="addResourceTitleShow"><div class="alert alert-danger" ng-cloak>{{addResourceTitleResponse}}</div></span>
            </fieldset>
            <fieldset>
                <label>Resource URL</label>
                <input type="url" class="input-block-level" name="link" ng-model="link" placeholder="http://" required>
                <span ng-show="addResourceURLShow"><div class="alert alert-danger" ng-cloak>{{addResourceURLResponse}}</div></span>
            </fieldset>
            <fieldset>
                <label><strong>Additional information</strong><br>
                <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>
                <textarea name="text" rows="3" class="input-block-level" ng-model="text"></textarea>
                <span class="help-block"> (Any additional information you want to include.  This is optional.) </span>
            </fieldset>
            <span ng-show="addResourceShow">{{addResourceResponse}}</span>
            <fieldset>
                <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>
            </fieldset>
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
            <fieldset>
                <label>Progress Report Title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>
                <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>
                <span ng-show="addUpdateTitleShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTitleResponse}}</div></span>
            </fieldset>
            <fieldset>
                <label><strong>Progress Report Text</strong>
                <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>
                <textarea name="text" rows="3" class="input-block-level" ng-model="text" required></textarea>
                <span ng-show="addUpdateTextShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTextResponse}}</div></span>
                <span class="help-block"> (A description of the progress made on implementing the initiative since the last progress report.) </span>
            </fieldset>
            <fieldset>
                <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>
            </fieldset>
        </form>
    % endif
</%def>

<%def name="geoSelect()">
    <!-- need to get the c.initiative['scope'] and update the selects accordingly -->
    <% 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = c.states
            countyMessage = "Leave 'State' blank if your initiative applies to the entire country."
        endif
    %>
    <div class="row-fluid"><span id="planetSelect">
        <div class="span3">Planet:</div>
        <div class="span8">
            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">
                <option value="0">Earth</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->     
    <div class="row-fluid"><span id="countrySelect">
        <div class="span3">Country:</div>
        <div class="span8">
            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">
                <option value="0">Select a country</option>
                <option value="United States" ${countrySelected}>United States</option>
            </select>
        </div><!-- span8 -->
    </span><!-- countrySelect -->
    </div><!-- row-fluid -->
    <div class="row-fluid"><span id="stateSelect">
        % if c.country != "0":
            <div class="span3">State:</div><div class="span8">
            <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">
            <option value="0">Select a state</option>
            % for state in states:
                % if state != 'District of Columbia':
                    % if c.state == state['StateFullName']:
                        <% stateSelected = "selected" %>
                    % else:
                        <% stateSelected = "" %>
                    % endif
                    <option value="${state['StateFullName']}" ${stateSelected}>${state['StateFullName']}</option>
                % endif
            % endfor
            </select>
            </div><!-- span8 -->
        % else:
            Leave 'Country' blank if your initiative applies to the entire planet.
        % endif
    </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="countySelect">
        % if c.state != "0":
            <% counties = getCountyList("united-states", c.state) %>
            <% cityMessage = "Leave blank 'County' blank if your initiative applies to the entire state." %>
            <div class="span3">County:</div><div class="span8">
            <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">
                <option value="0">Select a county</option>
                % for county in counties:
                    % if c.county == county['County'].title():
                        <% countySelected = "selected" %>
                    % else:
                        <% countySelected = "" %>
                    % endif
                    <option value="${county['County'].title()}" ${countySelected}>${county['County'].title()}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% cityMessage = "" %>
            ${countyMessage}
        % endif
    </span></div><!-- row -->
    <div class="row-fluid"><span id="citySelect">
        % if c.county != "0":
            <% cities = getCityList("united-states", c.state, c.county) %>
            <% postalMessage = "Leave 'City' blank if your initiative applies to the entire county." %>
            <div class="span3">City:</div><div class="span8">
            <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">
            <option value="0">Select a city</option>
                % for city in cities:
                    % if c.city == city['City'].title():
                        <% citySelected = "selected" %>
                    % else:
                        <% citySelected = "" %>
                    % endif
                    <option value="${city['City'].title()}" ${citySelected}>${city['City'].title()}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% postalMessage = "" %>
            ${cityMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="postalSelect">
        % if c.city != "0":
            <% postalCodes = getPostalList("united-states", c.state, c.county, c.city) %>
            <% underPostalMessage = "or leave blank if your initiative is specific to the entire city." %>
            <div class="span3">Zip Code:</div><div class="span8">
            <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">
            <option value="0">Select a zip code</option>
                % for pCode in postalCodes:
                    % if c.postal == str(pCode['ZipCode']):
                        <% postalSelected = "selected" %>
                    % else:
                        <% postalSelected = "" %>
                    % endif
                    <option value="${pCode['ZipCode']}" ${postalSelected}>${pCode['ZipCode']}</option>
                % endfor
            </select>
            </div><!-- span8 -->
        % else:
            <% underPostalMessage = "" %>
            ${postalMessage}
        % endif
        </span></div><!-- row-fluid -->
    <div class="row-fluid"><span id="underPostal">${underPostalMessage}</span><br /></div><!-- row -->
    <br/>
</%def>

<%def name="showCost(item)">
    <% 
        currency = '$'
        cost = int(item['cost']) 
        if cost <= -1:
            cost = cost * -1
            currency = '- $'
    %>
    <h4 class="initiative-title">
        <div class="span6 pull-left">
            Cost Estimate
        </div>
        <div class="span6">
            <table class="pull-right">
                <tr>
                    <td>${currency}</td>
                    <td>${locale.format("%d", cost, grouping=True)}</td>
                <tr>
            </table>
        </div>
    </h4>
</%def>

<%def name="coAuthorInvite()">
    <div class="row-fluid" id="coauthors">
        <h3 class="initiative-title edit">5. Coauthors</h3>
    </div><!-- row-fluid -->
    <strong>Invite CoAuthors:</strong>
    % if 'user' in session and c.authuser:
        <div ng-init="urlCode = '${c.initiative['urlCode']}'; url = '${c.initiative['url']}'; authuserCode = '${c.authuser['urlCode']}'">
            <div ng-controller="userLookupCtrl">
                <div class="row-fluid">
                    <form ng-submit="lookup()">
                        <div class="input-append">
                          <input type="text" ng-submit="lookup()" name="userValue" ng-model="userValue" placeholder="Type a user's name...">
                          <button type="submit" class="btn"><i class="icon-search"></i></button>
                        </div>
                    </form>
                        <table class="table-striped full-width" ng-if="!(users = '')" ng-cloak>
                            <tr ng-repeat="user in users | limitTo:10">
                                <td>
                                    <a href="/profile/{{user.urlCode}}/{{user.url}}">
                                        <img class="media-object avatar med-avatar" ng-src="{{user.photo}}" alt="{{user.name}}" title="{{user.name}}">
                                    </a>
                                </td>
                                <td class="span8 grey"><a class="green green-hover" href="/profile/{{user.urlCode}}/{{user.url}}">{{user.name}}</a> from <a href="{{user.cityURL}}">{{user.cityTitle}}</a>, <a href="{{user.stateURL}}">{{user.stateTitle}}</a></td>
                                <td>
                                    <button ng-click="submitInvite(user.urlCode)" class="btn btn-primary pull-right">Invite to Coauthor</button>
                                </td>
                            </tr>
                        </table>
                </div><!-- row-fluid -->
                <div ng-show="alertMsg != ''" class="alert alert-{{alertType}} {{alertDisplay}}">
                    <button type="button" class="close" ng-click="hideShowAlert()">&times;</button>
                    {{alertMsg}}
                </div>
                <br>
                <strong>Author and Coauthors:</strong>
                <!-- 
                <div class="centered" ng-show="loading" ng-cloak>
                    <i class="icon-spinner icon-spin icon-4x" style="color: #333333"></i>
                </div>
                <div class="row-fluid" ng-show="!loading"> -->
                    <table class="table-striped full-width">
                        <tr>
                            <td>
                                ${lib_6.userImage(c.user, className="avatar med-avatar")}
                            </td>
                            <td>
                                <a class="green green-hover" href="/profile/${c.user['urlCode']}/${c.user['url']}">${c.user['name']}</a>
                                <span class="grey">from <a href="${c.authorGeo['cityURL']}" class="orange oreange-hover">${c.authorGeo['cityTitle']}</a>, <a href="${c.authorGeo['stateURL']}" class="orange orange-hover">${c.authorGeo['stateTitle']}</a></span>
                            </td>
                            <td>
                                <span class="badge badge-inverse">Original Author</span>
                            </td>
                            <td></td>
                        </tr>
                        <tr ng-repeat="a in authors">
                            <td>
                                <a class="pull-left" href="/profile/{{a.urlCode}}/{{a.url}}">
                                    <img class="media-object avatar med-avatar" ng-src="{{a.photo}}" alt="{{a.name}}" title="{{a.name}}">
                                </a>
                            </td>
                            <td>
                                <a class="green green-hover" href="/profile/{{a.urlCode}}/{{a.url}}">{{a.name}}</a>
                                <span class="grey">from <a href="{{a.cityURL}}" class="orange oreange-hover">{{a.cityTitle}}</a>, <a href="{{a.stateURL}}" class="orange orange-hover">{{a.stateTitle}}</a></span>
                            </td>
                            <td>
                                <span ng-show="a.pending == '1'"  class="badge badge-info">Invitation Pending</span>
                            </td>
                            <td ng-show="a.urlCode != authuserCode" ng-cloak>
                                <button type="button" ng-click="removeCoA(a.urlCode)" class="btn btn-danger pull-right">Remove Coauthor</button>
                            </td>
                            <td>
                                <form class="no-bottom" ng-show="a.urlCode == authuserCode" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/{{a.urlCode}}/facilitate/resign/handler" ng-cloak>
                                    <input type="hidden" name="resign" value="resign">
                                    <button type="submit" class="btn btn-danger pull-right">Resign as Coauthor</button>
                                </form>
                            </td>
                        </tr>
                    </table>
                <!-- ng-loading </div> -->
            </div><!-- ng-controller -->
        </div><!-- ng-init -->
    %endif   
</%def>

