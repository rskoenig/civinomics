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
<%namespace name="ng_lib" file="/lib/ng_lib.mako" />
<%namespace file="/lib/derived/6_initiative_home.mako" name="ihelpers" />

<%def name="iMenu()">

    % if c.iPrivs and c.editInitiative and c.initiative.objType != 'initiativeUnpublished':
        <ul class="nav nav-pills nav-stacked" style="width: 100%;">
            <li><a ng-click="scrollTo('basics')">1. Basics</a></li>
            <li><a ng-click="scrollTo('summary')">2. Info</a></li>
            <li><a ng-click="scrollTo('photo')">3. Photo</a></li>
            <li><a ng-click="scrollTo('coauthors')">4. Coauthors</a></li>
            <!--
            <li><a href="#iStats" data-toggle="tab">Stats</a></li>
            <li><a href="#iUpdates" data-toggle="tab">Updates</a></li>
            <li><a href="#iPhotos" data-toggle="tab">Photos</a></li>
            -->
        </ul>
    % elif c.editUpdate or c.update or c.resource or c.editResource:
        <!-- direct linking to sections of the page not working due to angular '/' injection after '#' -->
        <ul class="nav nav-pills nav-stacked i-menu" style="width: 100%;">
            <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}#summary">Info</a></li>
            <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}#updates">Updates</a></li>
            <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}#resources">Resources</a></li>
            <li><a href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}#comments">Comments</a></li>
        </ul>
    % else:
        <ul class="nav nav-pills nav-stacked i-menu" style="width: 100%;">
            <li><a ng-click="scrollTo('summary')">Info</a></li>
            <li><a ng-click="scrollTo('updates')">Updates</a></li>
            <li><a ng-click="scrollTo('comments')">Comments</a></li>
        </ul>
    % endif

</%def>

<%def name="iTags()">
    <h4> 
        <a href="${c.scopeHref}"><img class="thumbnail span flag small-flag border right-space" style="margin-bottom: 0;" src="${c.scopeFlag}"></a> <a class="no-highlight overlay" href="${c.scopeHref}"></a>
        % if c.initiative['tags']:
            <span class="white"> / </span>
        % endif
        ${lib_6.showTags(c.initiative)}
        % if c.initiative['workshopCode']:
            <a class="no-highlight overlay" href="/workshop/${c.initiative['workshopCode']}/${c.initiative['workshop_url']}"> / ${c.initiative['workshop_title']}</a>
        % endif
        
    </h4>
</%def>

<%def name="iControlPanel()">
    <div style="position:fixed; width: inherit; max-width: 280px;">
        % if c.iPrivs and c.editInitiative and c.initiative.objType != 'initiativeUnpublished':
            <div class="section-wrapper overview well initiative-well action-panel" style="background-color: whitesmoke;">
                <div class="row">
                    <div class="col-xs-12">
                    % if c.initiative['public'] == '0' and c.complete:
                        <form method="POST" name="publish" id="publish" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/edit">
                            <button type="submit" class="btn btn-lg btn-success btn-block" name="public" value="publish">Publish</button>
                        </form>
                        <div class="alert alert-warning top-space">You have added all of the required information. Click 'Publish' to make your initiative publicly discoverable.</div>
                    % elif c.initiative['public'] == '0':
                        <button class="btn btn-lg btn-warning btn-block" disabled>Publish</button>
                        <br>
                        <div class="alert alert-warning top-space">You must complete all required information and upload a picture before you can publish.</div>

                    % else:
                        <form method="POST" name="publish" id="publish" action="/unpublish/initiative/${c.initiative['urlCode']}">
                            <button type="submit" class="btn btn-lg btn-warning btn-block" name="public" value="unpublish">Unpublish</button>
                        </form>
                        <div class="alert alert-warning top-space" style="margin-bottom: 0;">Unpublished initiatives don't show up in searches or on public listings.</div>
                    % endif
                    </div>
                </div>

                <div class="row centered i-social-buttons">
                    <hr class="narrow">
                    <a class="btn btn-default" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/show"><strong>View Initiative</strong></a>
                </div>

            </div>
        % elif not c.editInitiative and c.initiative.objType == 'initiative':
            <div class="section-wrapper overview well initiative-well action-panel" style="overflow:visible;">
                % if c.initiative.objType != 'revision':
                        % if c.initiative['public'] == '0':
                            <div class="row">
                                <div class="col-xs-12">
                                    % if c.initiative['public'] == '0':
                                        <form method="POST" name="publish" id="publish" action="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/edit">
                                            <button type="submit" class="btn btn-lg btn-success btn-block" name="public" value="publish">Publish</button>
                                        </form>
                                    % endif
                                    <div class="alert alert-warning top-space">This initiative is not yet published. It does not show up in searches or on public listings.</div>
                                </div>
                            </div>
                        % elif c.authuser and c.authuser['memberType'] == 'organization':
                            <h4 class="text-center gray">Position</h4>
                            <hr class="narrow">
                            <!-- this is the second call to positionsCtrl on the initative page - would be better to use a service -->
                            <div ng-init="code = '${c.initiative['urlCode']}'; objType = 'initiative'"></div>
                            <div ng-controller="positionsCtrl">
                                ${lib_6.orgPosition(c.initiative)}
                            </div>
                        % else:
                            <h4 class="text-center gray">Vote</h4>
                            <hr class="narrow">
                            <div class="row">
                                <div class="col-xs-10 col-xs-offset-1">
                                    <div ng-init="inPage = true;">
                                        <div ng-controller="yesNoVoteCtrl">
                                            ${ng_lib.yesNoVoteBlock()}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        % endif
                    <!--
                    <hr class="narrow">
                    <div>
                    <table id="metrics">
                        <tr>
                          <td class="clickable" style="padding-left: 0px;" ng-click="toggleAdopted()">
                            <span class="workshop-metrics">Comments</span><br>
                              <strong ng-cloak>${c.numComments}</strong>
                          </td>
                          <td class="clickable" ng-click="toggleIdeas()">
                            <span class="workshop-metrics">Views</span><br>
                              <strong ng-cloak>${c.initiative['views']}</strong>
                          </td>
                        </tr>
                      </table>
                    </div>
                    -->
                    <div class="row centered i-social-buttons">
                        <hr class="narrow">
                        <span>
                            % if c.initiative['public'] == '1':
                               
                                ${lib_6.facebookDialogShare2(shareOnWall=True, sendMessage=True, btn=True)}

                                % if c.initiativeHome and c.initiative.objType != 'revision':
                                    ${ihelpers.watchButton(c.initiative)}
                                % endif

                                % if c.iPrivs:
                                    <a class="btn btn-default" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/updateEdit/new"><strong>Add Update</strong></a>
                                % endif
                                <!-- % if c.initiative['public'] == '1':
                                    <a href="/workshop/${c.initiative['urlCode']}/${c.initiative['url']}/rss" target="_blank"><i class="icon-rss icon-2x"></i></a>
                                #%endif -->
                            % endif
                            
                            % if c.initiative.objType != 'revision':
                                % if c.iPrivs:
                                    <a class="btn btn-default" href="/initiative/${c.initiative['urlCode']}/${c.initiative['url']}/edit"><strong>Edit Initiative</strong></a>
                                % endif
                            % else:
                                <a class="btn btn-default" href="/initiative/${c.initiative['initiativeCode']}/${c.initiative['initiative_url']}/show"><strong>View Current Version</strong></a>
                            % endif

                        </span>
                    </div>
                    <!--
                    <div class="row">
                        <div class="span10 offset2">
                            <label class="checkbox grey">
                            <input type="checkbox" class="shareVote" name="shareVote" value="shareVote"> Show how I voted when sharing
                            </label>
                        </div>
                    </div>
                    -->
                    <!-- 
                    <h4 class="section-header smaller section-header-inner">Fund It</h4>
                    <br>
                    <div>$136,000 of ${c.initiative['cost']}</div>
                    <div class="progress">
                      <div class="bar bar-primary" style="width: 35%;"></div>
                    </div>
                    <small class="pull-right grey" style="margin-top: -20px;">43 funders</small><br>
                    <div class="row centered">
                        <button class="btn-large btn-success btn">Fund Initiative</button>
                    </div>
                    -->
                % endif 
            </div><!-- section-wrapper -->
        % endif
    </div> <!-- position:fixed -->
</%def>
