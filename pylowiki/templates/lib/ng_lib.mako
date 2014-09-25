<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="basic_listing()">
    <td class="avatar-cell"><div ng-if="item.thumbnail" class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div></td>
    <td><a href="{{item.href}}">{{item.title}}</a> | {{item.objType}} | deleted by: {{item.unpublishedBy}}</td>
</%def>

<%def name="meeting_listing()">
    <div class="media well search-listing">
        <div class="row">
            <div class="col-xs-2"><img class="thumbnail med-flag" src="{{item.flag}}"></div><div class="col-xs-9">{{item.scopeLevel}} of {{item.scopeName}}</div>
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-2">
                <strong>{{item.meetingDate}}</strong>
                <p><strong>{{item.meetingTime}}</strong></p>
            </div>
            <div class="col-xs-9">
                <a href="{{item.href}}">{{item.title}}</a>
                <p>Public Meeting of {{item.group}}</p>
                <p>{{item.location}}</p>
                <p ng-show="(item.agendaItemCount != '0')"><a href="{{item.href}}">View, vote and comment on agenda items.</a></p>
                <p ng-show="(item.agendaItemCount == '0' && item.agendaPostDate != '')">Agenda posted: {{item.agendaPostDate}}</p>
                <i class="icon-eye-open"></i> Views ({{item.views}})
            </div>
        </div><!-- row -->
    </div><!-- media-well -->
</%def>

<%def name="meeting_listing_small()">
    <div class="media well search-listing">
        <div class="row">
            <div class="col-xs-3">
            	<strong style="font-size:22px; text-align:center; margin-right:5px;">{{item.meetingDate.split("-")[2]+"-"+item.meetingDate.split("-")[0]+"-"+item.meetingDate.split("-")[1] | date: "MMM dd"}}</strong>
            </div>
            <div class="col-xs-9">
                <a href="{{item.href}}">{{item.title}}</a>
                <p>Public Meeting of {{item.group}}</p>
            </div>
        </div><!-- row -->
    </div><!-- media-well -->
</%def>

<%def name="agenda_item_listing()">
    <div style="margin-top: 30px;"></div>
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode; url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; canVote=item.canVote; canComment=item.canComment; revisions = item.revisions; revisionList = item.revisionList; canEdit = item.canEdit">
        <div class="row">
            <div class="col-xs-12">
                <h4 class="listed-item-title">{{item.title}}</h4>
                <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-12">
                <div class="btn-group">
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-default btn-xs" data-toggle="collapse" data-target="#edit-{{urlCode}}">Edit</button>
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-default btn-xs" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">trash</a>
                </div>
                <div id="edit-{{urlCode}}" class="collapse">
                    <form action="/agendaitem/{{urlCode}}/{{url}}/editHandler" method="POST">
                        <fieldset>
                            <label>Item Title</label>
                            <input type="text" name="agendaItemTitle" class="col-xs-6" value="{{item.title}}" class="col-xs-9" required>
                            <label>Item Text</label>
                            ${lib_6.formattingGuide()}<br>
                            <textarea rows="3" name="agendaItemText" class="col-xs-9 form-control" required>{{item.text}}</textarea>
                            <label class="checkbox">
                            <input type="checkbox" name="agendaItemVote" ng-show="(canVote == '')">
                            <input type="checkbox" name="agendaItemVote" checked ng-show="(canVote == 'checked')">
                            People can vote on this
                            </label>
                            <label class="checkbox">
                            <input type="checkbox" name="agendaItemComment" ng-show="(canComment == '')">
                            <input type="checkbox" name="agendaItemComment" checked ng-show="(canComment == 'checked')">
                            People can comment on this
                            </label>
                            <button class="btn btn-success" type="submit" class="btn">Save Item</button>
                        </fieldset>
                    </form>
                </div>
                <div id="unpublish-{{urlCode}}" class="collapse" >
                    <div class="alert">
                        <strong>Are you sure you want to send this meeting agenda item to the trash?</strong>
                        <br />
                        <a href="/unpublish/agendaitem/{{urlCode}}" class="btn btn-danger">Yes</a>
                        <a class="btn accordion-toggle" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">No</a>
                        <span id = "unpublish_{{urlCode}}"></span>
                    </div>
                </div>
                <div class="accordion" id="revisions">
                    <div ng-repeat="rev in revisionList">
                        <div class="accordion-group">
                            <div class="accordion-heading">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#revisions" href="#rev-{{rev.urlCode}}">
                                Revision: {{rev.date}}
                                </a>
                            </div><!-- accordian-heading -->
                            <div id="rev-{{rev.urlCode}}" class="accordion-body collapse">
                                <div class="accordion-inner">
                                    <h4>{{rev.title}}</h4>
                                    <span ng-bind-html="rev.html"></span>
                                </div><!-- accordian-inner -->
                            </div><!-- accordian-body -->
                        </div><!-- accordian-group -->
                    </div><!-- ng-repeat -->
                </div><!-- accordian -->
            </div>
        </div>
        <div ng-controller="yesNoVoteCtrl" class="row" ng-show="(canVote == 'checked')">
                ${yesNoVoteFooter()}
            </div>
        <div class="row" ng-show="(canComment == 'checked')">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="election_listing()">
    <div class="media well search-listing">
        <div class="row" style="margin-top:19px;">
            <div class="col-xs-3"><img src="{{item.flag}}" width="80" height="60"></div>
            <div class="col-xs-9">
                <a href="{{item.href}}">{{item.title}}</a><br>
                {{item.scopeLevel}} of {{item.scopeName}}<br>
                Election Date: {{item.electionDate}}<br>
            </div>
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-11">
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                <p><a href="{{item.href}}">View, vote and comment on ballot items.</a></p>
            </div>
        </div><!-- row -->
    </div><!-- media-well -->
</%def>

<%def name="election_home_listing()">
    <div class="media well search-listing">
        <div class="row">
            <div class="col-xs-11">
                <h4>{{item.niceDate}}</h4>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-11">
                <span ng-repeat="flag in item.flags">
                    <img src="{{flag}}" width="60" height="40">
                </span>
                <p><a href="{{item.href}}">View Interactive Sample Ballot</a></p>
            </div>
        </div>
        <div class="spacer"></div>
    </div><!-- media-well -->
</%def>

<%def name="sample_ballot_listing()">
    <div class="media well search-listing">
        <div class="row">
            <div class="col-xs-11">
                <h4>{{sampleBallot.niceDate}}</h4>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-11">
                <span ng-repeat="flag in sampleBallot.flags">
                    <img src="{{flag}}" width="60" height="40">
                </span>
            </div>
        </div>
        <div class="spacer"></div>
        <div ng-repeat="scopeLevel in sampleBallot.scopes">
            <div class="row">
                <div class="col-xs-11">
                    <img src="{{scopeLevel.flag}}" width="60" height="40"> <strong>{{scopeLevel.name}}</strong>
                    <div ng-repeat="ballot in scopeLevel.ballots" class="spacer">
                        <p><strong>{{ballot.title}}</strong></p>
                        <div ng-show="ballot.html">
                            <p ng-init="stringLimit=300"><span ng-bind-html="ballot.html | limitTo:stringLimit"></span>${moreLess()}</p>
                        </div>
                        <div ng-show="ballot.instructions">
                            <p><strong>Instructions:</strong></p>
                            <p ng-init="stringLimit=300"><span ng-bind-html="ballot.instructions | limitTo:stringLimit"></span>${moreLess()}</p>
                        </div>
                        <div ng-show="(ballot.ballotSlate == 'measures')">
                            <div class="spacer"></div>
                            <div ng-init="url = ballot.url; code = ballot.urlCode; ballotSlate = ballot.ballotSlate;">
                                <div ng-controller="ballotsController">
                                    <div class="row">
                                        <div class="col-xs-11">
                                            <div class="centered" ng-show="loading" ng-cloak>
                                            <i class="icon-spinner icon-spin icon-4x"></i>
                                            </div><!-- loading -->
                                            <div ng-repeat="item in activity">
                                                <div class="row">
                                                    ${ballot_measure_listing()}
                                                </div><!-- row -->
                                            </div><!-- ng-repeat -->
                                        </div><!-- col-xs-11 -->
                                    </div><!-- row -->
                                </div><!-- ng-controller -->
                            </div><!-- ng-init -->
                        </div>
                        <div ng-show="(ballot.ballotSlate == 'candidates')">
                        </div>
                    </div><!-- ng-repeat -->
                </div><!-- col-xs-11 -->
            </div><!-- row -->
        </div><!-- ng-repeat -->
    </div><!-- media-well -->
</%def>

<%def name="ballot_listing()">
    <div class="media well search-listing">
        <div class="row" style="margin-top:19px;">
            <div class="col-xs-9">
                <a href="{{item.href}}">{{item.title}}</a>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                <p><a href="{{item.href}}">View, vote and comment on ballot items.</a> &nbsp; &nbsp; <i class="glyphicon glyphicon-eye-open"></i> Views ({{item.views}})</p>
            </div><!-- col-xs-9 -->
        </div><!-- row -->
    </div><!-- media-well -->
</%def>

<%def name="ballot_measure_listing()">
    <div style="margin-top: 30px;"></div>
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode; url=item.url; ballotMeasureOfficialURL = item.ballotMeasureOfficialURL; number = item.number; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; type=item.objType; objType = 'ballotmeasure'; revisions = item.revisions; revisionList = item.revisionList; canEdit = item.canEdit">
        <div class="row">
            <div class="col-xs-11">
                <h4 class="listed-measure-title">{{item.title}}</h4>
                <p ng-show="(item.ballotMeasureOfficialURL != '')">Official Web Site: <a href="{{ballotMeasureOfficialURL}}" target="_blank">{{ballotMeasureOfficialURL}}</a></p>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div><!-- col-xs-11 -->
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-11">
                <div class="btn-group">
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#edit-{{urlCode}}">Edit</button>
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">trash</a>
                </div>
                <div id="edit-{{urlCode}}" class="collapse">
                    <form action="/ballotmeasure/{{urlCode}}/{{url}}/editHandler" role="form" method="POST">
                        <div class="row form-group spacer">
                            <div class="col-xs-3 col-xs-offset-1">
                                <label for="ballotMeasureTitle" >Title</label>
                            </div><!-- col-xs-3 -->
                            <div class="col-xs-6">
                                <input type="text" name="ballotMeasureTitle" class="form-control" value="{{item.title}}" required>
                            </div><!-- col-xs-6 -->
                        </div><!-- form-group -->
                        <div class="row form-group">
                            <div class="col-xs-3 col-xs-offset-1">
                                <label for="ballotMeasureNumber">Listing Order Number on Ballot</label>
                            </div><!-- col-xs-3 -->
                            <div class="col-xs-6">
                                <input type="text" name="ballotMeasureNumber" class="form-control" value="{{item.number}}" required>
                            </div><!-- col-xs-6 -->
                        </div><!-- form-group -->
                        <div class="row form-group">
                            <div class="col-xs-3 col-xs-offset-1">
                                <label for="ballotMeasureOfficialURL">Official Website URL</label>
                            </div><!-- col-xs-3 -->
                            <div class="col-xs-6">
                                <input type="text" name="ballotMeasureOfficialURL" class="form-control" value="{{item.ballotMeasureOfficialURL}}">
                            </div><!-- col-xs-6 -->
                        </div><!-- form-group -->
                        <div class="row form-group">
                            <div class="col-xs-3 col-xs-offset-1">
                                <label for="ballotMeasureText">Text</label>
                            </div><!-- col-xs-3 -->
                            <div class="col-xs-6">
                                ${lib_6.formattingGuide()}<br>
                                <textarea rows="3" name="ballotMeasureText" class="form-control" required>{{item.text}}</textarea>
                            </div><!-- col-xs-6 -->
                        </div><!-- form-group -->
                        <div class="row form-group">
                            <div class="col-xs-3 col-xs-offset-1">
                                <button class="btn btn-success" type="submit" class="btn">Save Item</button>
                            </div><!-- col-xs-3 -->
                        </div><!-- form-group -->
                    </form>
                </div>
                <div id="unpublish-{{urlCode}}" class="collapse" >
                    <div class="alert">
                        <strong>Are you sure you want to send this ballot measure to the trash?</strong>
                        <br />
                        <a href="/unpublish/ballotmeasure/{{urlCode}}" class="btn btn-danger">Yes</a>
                        <a class="btn accordion-toggle" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">No</a>
                        <span id = "unpublish_{{urlCode}}"></span>
                    </div><!-- alert -->
                </div>
                <ul class="unstyled">
                <div ng-repeat="rev in revisionList">
                    <li><a href="/ballotmeasure/{{rev.urlCode}}/{{rev.url}}/show">Revision: {{rev.date}}</a></li>
                </div><!-- ng-repeat -->
                </ul>
            </div><!-- col-xs-11 -->
        </div><!-- row -->
        <div ng-controller="yesNoVoteCtrl" class="row">
            ${yesNoVoteFooter()}
            ${actions()}
        </div>
    </div><!-- media -->
    <div class="spacer"></div>
</%def>

<%def name="ballot_candidate_listing()">
    <div style="margin-top: 30px;"></div>
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode; url=item.url; ballotCandidateParty = item.ballotCandidateParty; ballotCandidateOfficialURL = item.ballotCandidateOfficialURL; number = item.number; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; type=item.objType; objType = 'ballotcandidate'; revisions = item.revisions; revisionList = item.revisionList; canEdit = item.canEdit;">
        <div class="row">
            <div class="well yesNoWell">
                ${candidateVoteBlock()}
            </div>
            <h4 class="listed-candidate-title">{{item.title}}</h4>
            <p ng-show="(item.ballotCandateParty != '')">Party: {{ballotCandidateParty}}</p>
            <p ng-show="(item.ballotCandidateOfficialURL != '')">Official Web Site: <a href="{{ballotCandidateOfficialURL}}" target="_blank">{{ballotCandidateOfficialURL}}</a></p>
            <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
        </div><!-- row -->
        <div class="row">
            <div class="btn-group">
                <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#edit-{{urlCode}}">Edit</button>
                <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">trash</a>
            </div>
            <div id="edit-{{urlCode}}" class="collapse">
                <form action="/ballotcandidate/{{urlCode}}/{{url}}/editHandler" role="form" method="POST">
                    <div class="form-group spacer">
                        <label for="ballotCandidateTitle">Title</label><br>
                        <input type="text" name="ballotCandidateTitle" class="form-control" value="{{item.title}}" required>
                    </div><!-- form-group -->
                    <div class="form-group spacer">
                        <label for="ballotCandidateNumber">Listing Order Number on Ballot</label><br>
                        <input type="text" name="ballotCandidateNumber" value="{{item.number}}" class="col-xs-1" required>
                    </div><!-- form-group -->
                    <div class="form-group spacer">
                        <label for="ballotCandidateParty">Party</label><br>
                        <input type="text" name="ballotCandidateParty" class="form-control" value="{{item.ballotCandidateParty}}">
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotCandidateOfficialURL">Official Website URL</label><br>
                        <input type="text" name="ballotCandidateOfficialURL" class="form-control" value="{{item.ballotCandidateOfficialURL}}">
                    </div><!-- form-group -->
                    <div class="form-group">
                        <label for="ballotCandidateText">Text</label><br>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="ballotCandidateText" class="form-control" required>{{item.text}}</textarea>
                    </div><!-- form-group -->
                    <div class="form-group">
                        <button class="btn btn-success" type="submit" class="btn">Save Item</button>
                    </div><!-- form-group -->
                </form>
            </div><!-- collapse -->
            <div id="unpublish-{{urlCode}}" class="collapse" >
                <div class="alert">
                    <strong>Are you sure you want to send this ballot candidate to the trash?</strong>
                    <br />
                    <a href="/unpublish/ballotcandidate/{{urlCode}}" class="btn btn-danger">Yes</a>
                    <a class="btn accordion-toggle" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">No</a>
                    <span id = "unpublish_{{urlCode}}"></span>
                </div>
            </div><!-- collapse -->
            <ul class="unstyled">
                <div ng-repeat="rev in revisionList">
                    <li><a href="/ballotcandidate/{{rev.urlCode}}/{{rev.url}}/show">Revision: {{rev.date}}</a></li>
                </div><!-- ng-repeat -->
            </ul>
        </div><!-- row -->
        <div class="row">
            ${actions()}
        </div>
    </div><!-- media -->
    <div class="spacer"></div>
</%def>


<%def name="initiative_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl"> 
            ${authorPosting()}
            <div class="row" style="margin-top:19px;">
                <div class="col-xs-2">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <img class="thumbnail tight initiative-thumb no-top" src="{{item.thumbnail}}">
                        </a>
                    </div>
                </div>
                <div class="col-xs-10 no-left">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p><small>${metaData()}</small></p>
                    <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                    <p><strong>
                        <span ng-if="item.cost >= 0" class="grey centered">Net Cost:</span>
                        <span ng-if="item.cost < 0" class="grey centered">Net Savings:</span>
                        <span class="pull-right">{{(item.cost | currency).replace(".00", "")}}</span>
                    </strong></p>
                </div>
            </div>
            <div class="row">
                % if not c.authuser or c.authuser['memberType'] != 'organization':
                    ${yesNoVoteFooter()}
                % endif
                ${actions()}
            </div>
        </div>
    </div>
</%def>


<%def name="initiative_listing_condensed()">
    <div class="media well search-listing initiative-listing" style="height: 415px;" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl"> 
            <div class="row">
                <div class="col-sm-12">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo full-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="col-sm-12" style="height: 155px;">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p style="line-height: 16px;"><small>${metaData()}</small></p>
                    <!--
                    <p ng-init="stringLimit=300" class="markdown"><small><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</small></p>
                    -->
                    <h4>
                        <small class="grey centered">Estimated Cost:</small>
                        <span class="pull-right">{{item.cost | currency}}</span>
                    </h4>
                </div>
            </div>
            <div class="row">
                % if not c.authuser or c.authuser['memberType'] != 'organization':
                    ${yesNoVoteFooter(noStats = True)}
                % endif
            </div>
        </div>
    </div>
</%def>

<%def name="workshop_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl"> 
            ${authorPosting()}
            <div class="row" style="margin-top:19px;">
                <div class="col-sm-12">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p><small>${metaData()}</small></p>
                    <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                </div>
            </div>
            <div class="row">
                ${actions()}
            </div>
        </div>
    </div>
</%def>


<%def name="idea_listing()">
    <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl">
            ${authorPosting()}
            <div class="row" style="margin-top:19px;">
                <div class="col-sm-12">
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                    <strong ng-if="item.status == 'adopted'" class="green"><i class="icon-star"></i> Adopted</strong>
                    <strong ng-if="item.status == 'disabled'" class="red"><i class="icon-flag"></i> Disabled</strong>
                    <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                </div>
            </div>
            % if not c.authuser or c.authuser['memberType'] != 'organization':
                <div class="row" ng-if="item.readOnly == '1'">${yesNoVoteFooter(readonly = "1")}</div>
                <div class="row" ng-if="item.readOnly == '0'">${yesNoVoteFooter(readonly = "0")}</div>
            % endif
            <div class="row">
                <span ng-show="item.readOnly == '1'">${actions(readonly = '1')}</span>
                <span ng-show="item.readOnly == '0'">${actions(readonly = '0')}</span>
            </div>
    </div><!-- media well -->
</%def>

<%def name="resource_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl">
            <div class="row">
                <div class="col-xs-11">
                    <p>${authorPosting()}</p>
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a> <a ng-href="{{item.link}}"<small>({{item.link}})</small></a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                </div>
                <div class="col-xs-1">
                    <div class="row" ng-if="item.readOnly == '1'">${upDownVoteBlock(readonly = '1')}</div>
                    <div class="row" ng-if="item.readOnly == '0'">${upDownVoteBlock(readonly = '0')}</div>
                </div>
            </div>
            <div class="row">
                <span ng-show="item.readOnly == '1'">${actions(readonly = '1')}</span>
                <span ng-show="item.readOnly == '0'">${actions(readonly = '0')}</span>
            </div>
        </div>
    </div>
</%def>

<%def name="comment_listing()">
    <div ng-class="{pro : item.position == 'yes', con : item.position == 'no', neutral : item.position == 'neutral'}" class="media well search-listing-comment" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl">
            <div class="row">
                <div class="col-xs-11">
                    <p>${authorPosting()} <small class="left-space right-space">in</small> <small>${metaData()}</small></p>
                    <a ng-href="{{item.parentHref}}" class="no-highlight">{{item.text}}</a>
                </div>
                <div class="col-xs-1">
                    <div class="row" ng-if="item.readOnly == '1'">${upDownVoteBlock(readonly = '1')}</div>
                    <div class="row" ng-if="item.readOnly == '0'">${upDownVoteBlock(readonly = '0')}</div>
                </div>
            </div>
        </div>
    </div>
</%def>

                    
<%def name="discussion_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11 media-body">
                <p>${authorPosting()}</p>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}" target="_blank">{{item.title}} <small></small></a></h4>
                % if not c.w:
                    <p><small>${metaData()}</small></p>
                % endif
                <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
            <div class="col-xs-1">
                <div class="row" ng-if="item.readOnly == '1'">${upDownVoteBlock(readonly = '1')}</div>
                <div class="row" ng-if="item.readOnly == '0'">${upDownVoteBlock(readonly = '0')}</div>
            </div>
        </div>
        <div class="row">
            <span ng-show="item.readOnly == '1'">${actions(readonly = '1')}</span>
            <span ng-show="item.readOnly == '0'">${actions(readonly = '0')}</span>
        </div>
    </div>
</%def>

<%def name="position_listing()">
    <div class="media well search-listing" ng-class="{pro : item.position == 'support', con : item.position == 'oppose'}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11">
                ${authorPosting()}
                <p>
                    <strong ng-if="item.position == 'support'">We support: </strong>
                    <strong ng-if="item.position == 'oppose'">We oppose: </strong>
                    <a ng-href = '{{item.parentHref}}'><img ng-if="item.thumbnail != '0'" ng-src="{{item.thumbnail}}" style="height: 40px; width: 40px; border-radius: 4px;"></a>
                    <a ng-href="{{item.parentHref}}">{{item.parentTitle}}</a> <small><span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span><img class="thumbnail flag mini-flag border no-bottom" src="{{item.flag}}"></small>
                </p>
                <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
            <div class="col-xs-1">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="photo_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        ${authorPosting()}
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11 media-body">
                <div class="listed-photo">
                    <a href = '{{item.href}}'>
                        <div class="main-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                    </a>
                </div>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
            <div class="col-xs-1">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="yesNoVoteBlock(**kwargs)">
    <div class="form-group">
        <%
            if 'readonly' in kwargs:
                readonly = kwargs['readonly']
            else:
                readonly = "0"

        %>
        % if readonly == "1":
            <a class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>
        % elif 'user' in session:
            <a ng-click="updateYesVote()" class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a ng-click="updateNoVote()" class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>

        % else:
            <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>
        % endif
        <br>
        % if readonly == "1":
            Voting Complete
        % endif
        <div ng-cloak>
            <small class="grey">{{totalVotes}} votes <span ng-if="voted && item.readOnly == '0'">| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span></small>
            <small><span ng-if="item.readOnly == '1'">| <span class="green">{{(item.ups / item.voteCount * 100) | number:0}}% YES</span> | <span class="red">{{(item.downs / item.voteCount * 100) | number:0}}% NO</span></span></small> 
            <div class="progress" style="height: 12px; margin-bottom: 5px;">
                <div class="progress-bar" role="progress-bar" style="width: {{100 * totalVotes / goal | number:0}}%;"></div>
            </div>
            <small ng-if="item.goal == 100" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes needed for this initiative to advance.">{{goal - totalVotes | number:0}} NEEDED</small>
            <small ng-if="!(item.goal == 100)" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{goal - totalVotes | number}} NEEDED</small>
        </div>
    </div>
</%def>

<%def name="yesNoVoteFooter(**kwargs)">
    <div class="actions centered" style="padding:10px; padding-bottom: 10px;">

        <%
            if 'readonly' in kwargs:
                readonly = kwargs['readonly']
            else:
                readonly = "0"
        %>
        % if readonly == "1":
            <div class="row centered">
                <div class="col-sm-12">
                    Voting complete.<br>
                    <a class="btn btn-lg btn-success btn-vote {{voted}}">YES</a>
                    <a class="btn btn-lg btn-danger btn-vote {{voted}}">NO</a>
                </div>
            </div>
        % elif 'user' in session:
            <div class="row centered">
                <div class="col-sm-12">
                    <a ng-click="updateYesVote()" class="btn btn-lg btn-success btn-vote {{voted}}">YES</a>
                    <a ng-click="updateNoVote()" class="btn btn-lg btn-danger btn-vote {{voted}}">NO</a>
                </div>
            </div>
        % else:
            <div class="row centered">
                <div class="col-sm-12">
                    <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-success btn-vote {{voted}}">YES</a>
                    <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-danger btn-vote {{voted}}">NO</a>
                </div>
            </div>
        % endif
        % if not 'noStats' in kwargs:
            <div class="row text-center" style="margin: 0 19px; height:35px">
                <!-- multi-colored progress bar test
                <div class="progress col-sm-8">
                    <div class="progress-bar progress-bar-success" style="width: {{100 * yesVotes / 3 | number:0}}%">
                        <span class="sr-only">{{100 * yesVotes / 3 | number:0}}% Complete (success)</span>
                    </div>
                    <div class="progress-bar progress-bar-danger" style="width: {{100 * noVotes / 3 | number:0}}%">
                        <span class="sr-only">{{100 * noVotes / 3 | number:0}}% Complete (danger)</span>
                    </div>
                </div>
                -->
                <div class="col-sm-12">
                    <small class="grey">
                        {{totalVotes}} votes<span ng-if="item.goal">, <span class="grey " tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{item.goal - item.voteCount | number}} NEEDED</span> </span>
                        <span ng-if="voted || item.readOnly == '1'">| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span>
                    </small>
                </div>
            </div>
        % endif
    </div>
</%def>

<%def name="upDownVoteBlock(**kwargs)"> 
    <div class="text-center" >
    <%
        if 'readonly' in kwargs:
            readonly = kwargs['readonly']
        else:
            readonly = "0"
    %>
    % if readonly == "1":
        <a class="upVote {{voted}}">
            <i class="icon-chevron-sign-up icon-2x {{voted}}"></i>
        </a>
        <br>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a class="downVote {{voted}}">
            <i class="icon-chevron-sign-down icon-2x {{voted}}"></i>
        </a>
        <br /><small>Voting Complete</small><br>
    % elif 'user' in session:
        <a ng-click="updateYesVote()" class="upVote {{voted}}">
            <i class="icon-chevron-sign-up icon-2x {{voted}}"></i>
        </a>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a ng-click="updateNoVote()" class="downVote {{voted}}">
            <i class="icon-chevron-sign-down icon-2x {{voted}}"></i>
        </a>
    % else:
        <a href="#signupLoginModal" data-toggle="modal" class="upVote">
            <i class="icon-chevron-sign-up icon-2x"></i>
        </a>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a href="#signupLoginModal" data-toggle="modal" class="downVote">
            <i class="icon-chevron-sign-down icon-2x"></i>
        </a>
    % endif
    </div>
    <br>
</%def>

<%def name="candidateVoteBlock()">
    % if 'user' in session:
        <a ng-click="updateCandidateVote(urlCode, url)" class="yesVote {{mycandidateVotes[urlCode]}}">
            <div class="vote-icon yes-icon detail"></div>
        </a>
        <br>
        <br>
        <div class="totalVotesWrapper">
            <span class="grey pull-left">Votes:</span>
            <strong class="pull-right">
                <span class="totalVotes">{{totalcandidateVotes[urlCode]}}</span>
            </strong>
        </div>
    % else:
        <a href="#signupLoginModal" role="button" data-toggle="modal" class="yesVote">
            <div class="vote-icon yes-icon"></div>
        </a>
        <br>
        <div class="totalVotesWrapper">
            <small class="grey pull-left">Votes:</small>
            <strong class="pull-right">
                <span class="totalVotes">{{totalVotes}}</span>
            </strong>
        </div>
    % endif
</%def>

<%def name="moreLess()">
    <a class="green green-hover" ng-show="item.text.length > 200 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{item.urlCode}}" class="green green-hover"  ng-show="item.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="moreLessComment()">
    <a class="green green-hover" ng-show="comment.text.length > 200 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{comment.urlCode}}" class="green green-hover"  ng-show="comment.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="moreLessStatement()">
    <a ng-href="{{item.href}}" target="_blank">more</a>
</%def>

<%def name="metaData(*args)">
    <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>

    % if 'inline' in args:
        <img class="thumbnail flag inline-title-flag border no-bottom" src="{{item.flag}}"> 

    % else:
        <img class="thumbnail flag mini-flag border no-bottom" src="{{item.flag}}"> 
    % endif

    <a style="text-transform: capitalize;" ng-href="{{item.scopeHref}}">{{item.scopeName}}</a>
    <span ng-if="item.parentHref && item.parentTitle != ''">| <a ng-href="{{item.parentHref}}">{{item.parentTitle}}</a></span>
</%def>

<%def name="authorPosting()">
    <img class="avatar small-avatar inline" ng-src="{{item.authorPhoto}}" alt="{{item.authorName}}" title="{{item.authorName}}">
    <small>
        <a href="{{item.authorHref}}" class="green green-hover">{{item.authorName}}</a> 
        <span class="date">{{item.fuzzyTime}} ago</span>
    </small>
</%def>

<%def name="actions(**kwargs)">
    <%
        if 'readonly' in kwargs:
            readonly = kwargs['readonly']
        else:
            readonly = '0'
    %>
    % if not c.searchQuery or c.geoScope:
        <div class="actions" ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = 'reply'; numComments = item.numComments; readonly = item.readOnly;">
            <div ng-controller="commentsController">
                <div class="row">
                    <div class="col-xs-12 iconListing-row">
                        <ul class="horizontal-list iconListing">
                            <li ng-if="item.objType != 'workshop'">
                                <a ng-show="item.numComments == '0'" class="no-highlight" ng-click="showAddComments()"><span class="glyphicon glyphicon-comment"></span> Comments ({{numComments}})</a>
                                <a ng-show="!(item.numComments == '0')" class="no-highlight" ng-click="getComments()"><span class="glyphicon glyphicon-comment"></span> Comments ({{numComments}})</a>
                            </li>
                            <li ng-show="(item.objType != 'ballotmeasure' && item.objType != 'ballotcandidate')"><i class="glyphicon glyphicon-eye-open"></i> Views ({{item.views}})</li>
                            % if c.authuser and c.authuser['memberType'] == 'organization':
                                <li ng-if="item.objType == 'idea' || item.objType == 'initiative'"><a class="no-highlight" ng-href="{{item.href}}"><i class="glyphicon glyphicon-file"></i> Add position statement</a></li>
                            % endif 
                        </ul>
                    </div>
                </div>
                ### Comments
                <div class="activity-comments">
                <table class="activity-comments">
                    <tr class="centered" ng-show="commentsLoading" ng-cloak>
                        <td></td>
                        <td><i class="icon-spinner icon-spin icon-2x bottom-space-med"></i></td>
                    </tr>

                    <tr ng-show="newCommentLoading" ng-cloak>
                        <td></td>
                        <td>
                            <div class="centered">
                                <i class="icon-spinner icon-spin icon-2x"></i>
                            </div>
                        </td>
                    </tr>

                    <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral', question : comment.commentRole == 'question', suggestion : comment.commentRole == 'suggestion', hidden : commentsHidden}" class="comment-row">

                        <td class="comment-avatar-cell">
                            <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                        </td>
                        <td class="comment-main-cell">
                            <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>
                            <br>
                            <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="comment.html | limitTo:stringLimit"></span>${moreLessComment()}</p>
                            <div class="accordion" id="revisions">
                                <div ng-repeat="rev in comment.revisionList">
                                    <div class="accordion-group">
                                        <div class="accordion-heading">
                                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#revisions" href="#rev-{{rev.urlCode}}">
                                            Revision: {{rev.date}}
                                            </a>
                                        </div><!-- accordian-heading -->
                                        <div id="rev-{{rev.urlCode}}" class="accordion-body collapse">
                                            <div class="accordion-inner">
                                                <p>Position: {{rev.role}}</p>
                                                Comment: <span ng-bind-html="rev.html"></span>
                                            </div><!-- accordian-inner -->
                                        </div><!-- accordian-body -->
                                    </div><!-- accordian-group -->
                                </div><!-- ng-repeat -->
                            </div><!-- accordian -->
                            % if readonly == '0':
                            <div ng-show="(comment.canEdit == 'yes')">
                                <div class="btn-group btn-group-xs">
                                    <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#edit-{{comment.urlCode}}">Edit</button>
                                    <!-- <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#unpublish-{{comment.urlCode}}">Trash</button> -->
                                </div><!-- btn-group -->
                                <div id="edit-{{comment.urlCode}}" class="collapse">
                                    <div ng-controller="commentEditController" ng-init="urlCode = comment.urlCode; commentEditText = comment.text; commentEditRole = comment.commentRole;">
                                        <form class="no-bottom" ng-submit="submitEditComment()">
                                            <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                            <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                            <div ng-show="(comment.doCommentRole == 'yes')">
                                                &nbsp;
                                                <label class="radio inline">
                                                    <input type="radio" name="commentRole-{{comment.urlCode}}" value="neutral" ng-model="commentEditRole"> Neutral
                                                </label>
                                                <label class="radio inline">
                                                    <input type="radio" name="commentRole-{{comment.urlCode}}" value="yes" ng-model="commentEditRole"> Pro
                                                </label>
                                                <label class="radio inline">
                                                    <input type="radio" name="commentRole-{{comment.urlCode}}" value="no" ng-model="commentEditRole"> Con
                                                </label>
                                                <label class="radio inline">
                                                    <input type="radio" name="commentRole-{{comment.urlCode}}" value="question" ng-model="commentEditRole"> Question
                                                </label>
                                                <label class="radio inline">
                                                    <input type="radio" name="commentRole-{{comment.urlCode}}" value="suggestion" ng-model="commentEditRole"> Suggestion
                                                </label>
                                            </div><!-- ng-show -->
                                        </form>
                                    </div><!-- controller -->
                                </div><!-- collapse -->
                            </div><!-- ng-show -->
                            % endif
                        </td>
                        <td class="col-xs-1 comment-vote">
                            <div class="row" ng-init="objType='comment'; rated=comment.rated; urlCode=comment.urlCode; totalVotes=comment.voteCount; yesVotes=comment.ups; noVotes=comment.downs; netVotes=comment.netVotes">
                                <div ng-controller="yesNoVoteCtrl">
                                    % if readonly == '0':
                                        ${upDownVoteBlock(readonly = '0')}
                                    % else:
                                        ${upDownVoteBlock(readonly = '1')}
                                    % endif
                                </div>
                            </div>
                        </td>
                    </tr>
                    % if readonly == '0':
                    <tr ng-hide="newCommentLoading || commentsHidden">
                        % if c.authuser:
                            <td class="comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                            <td class="col-xs-10" style="padding: 10px 0px;">
                                <form class="no-bottom form-inline" ng-submit="submitComment()">
                                    <div class="form-group col-sm-10 text-right" style="margin-left: 0; padding-left:0;">
                                        % if c.privs and not c.privs['provisional']:
                                            <textarea class="form-control new-comment"  rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                        % else:
                                            <a href="#activateAccountModal" data-toggle='modal'>
                                            <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea></a>
                                        % endif

                                        <small class="left-space" ng-show="type == 'initiative' || type == 'idea' || 'ballotmeasure' || 'ballotcandidate'">
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="question"> Question 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="suggestion"> Suggestion 
                                            </span>
                                        </small>
                                        
                                    </div>
                                    <div class="form-group">
                                        % if c.privs and not c.privs['provisional']:
                                            <button type="submit" class="btn btn-primary">Submit</button>
                                        % else:
                                            <a href="#activateAccountModal" data-toggle='modal' class="btn btn-primary">Submit</a>
                                        % endif
                                    </div>
                                </form>
                            </td>
                        % else:
                        <!-- if not c.authuser -->
                            <td class="col-xs-1 comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar topbar-avatar"></td>
                            <td class="col-xs-11" style="padding: 10px;">
                                <a href="#signupLoginModal" data-toggle='modal' class="no-highlight no-hover">
                                    <form class="no-bottom" ng-submit="submitEditComment()">
                                            <div class="form-group">
                                                <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                            </div>
                                            <div class="form-group">
                                                <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                                <div ng-show="(comment.doCommentRole == 'yes')">
                                                    &nbsp;
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="neutral" ng-model="commentEditRole"> Neutral
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="yes" ng-model="commentEditRole"> Pro
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="no" ng-model="commentEditRole"> Con
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="question" ng-model="commentEditRole"> Question
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="suggestion" ng-model="commentEditRole"> Suggestion
                                                    </label>
                                                </div><!-- ng-show -->
                                            </div>
                                        </form>
                            </td>
                        % endif
                        <td></td>
                    </tr>
                    % endif
                </table>
                </div><!-- activity comments -->
            </div>
        </div>
    % endif
</%def>

<%def name="actions2(**kwargs)">
    <%
        if 'readonly' in kwargs:
            readonly = kwargs['readonly']
        else:
            readonly = '0'
    %>  
            ### Comments
            <div class="activity-comments">
            <table class="activity-comments">

                <tr class="actions-links">
                    <td colspan="2" style="padding: 10px;">
                        <ul class="horizontal-list iconListing">
                            <li>
                                <a ng-show="item.numComments == '0'" class="no-highlight" ng-click="showAddComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                                <a ng-show="!(item.numComments == '0')" class="no-highlight" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                            </li>
                            <li><i class="icon-eye-open"></i> Views ({{item.views}})</li>
                        </ul>
                    </td>
                </tr>

                <tr class="centered" ng-show="commentsLoading" ng-cloak>
                    <td></td>
                    <td><i class="icon-spinner icon-spin icon-2x bottom-space-med"></i></td>
                </tr>

                <tr ng-show="newCommentLoading" ng-cloak>
                    <td></td>
                    <td>
                        <div class="centered">
                            <i class="icon-spinner icon-spin icon-2x"></i>
                        </div>
                    </td>
                </tr>

                <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral', question : comment.commentRole == 'question', suggestion : comment.commentRole == 'suggestion', hidden : commentsHidden}">

                    <td class="comment-avatar-cell">
                        <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                    </td>
                    <td style="padding: 10px;">
                        <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>
                        <br>
                        <p ng-init="stringLimit=300" class="markdown"><span ng-bind-html="comment.html | limitTo:stringLimit"></span>${moreLessComment()}</p>  
                        <div class="accordion" id="revisions">
                                <div ng-repeat="rev in comment.revisionList">
                                    <div class="accordion-group">
                                        <div class="accordion-heading">
                                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#revisions" href="#rev-{{rev.urlCode}}">
                                            Revision: {{rev.date}}
                                            </a>
                                        </div><!-- accordian-heading -->
                                        <div id="rev-{{rev.urlCode}}" class="accordion-body collapse">
                                            <div class="accordion-inner">
                                                <p>Position: {{rev.role}}</p>
                                                Comment: <span ng-bind-html="rev.html"></span>
                                            </div><!-- accordian-inner -->
                                        </div><!-- accordian-body -->
                                    </div><!-- accordian-group -->
                                </div><!-- ng-repeat -->
                            </div><!-- accordian -->
                            % if readonly == '0':
                            <div ng-show="(comment.canEdit == 'yes')">
                                <div class="btn-group btn-group-xs">
                                    <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#edit-{{comment.urlCode}}">Edit</button>
                                    <!-- <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#unpublish-{{comment.urlCode}}">Trash</button> -->
                                </div><!-- btn-group -->
                                <div id="edit-{{comment.urlCode}}" class="collapse">
                                    <div ng-controller="commentEditController" ng-init="urlCode = comment.urlCode; commentEditText = comment.text; commentEditRole = comment.commentRole;">
                                        <form class="no-bottom" ng-submit="submitEditComment()">
                                            <div class="form-group">
                                                <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                            </div>
                                            <div class="form-group">
                                                <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                                <div ng-show="(comment.doCommentRole == 'yes')">
                                                    &nbsp;
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="neutral" ng-model="commentEditRole"> Neutral
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="yes" ng-model="commentEditRole"> Pro
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="no" ng-model="commentEditRole"> Con
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="question" ng-model="commentEditRole"> Question
                                                    </label>
                                                    <label class="radio inline">
                                                        <input type="radio" name="commentRole-{{comment.urlCode}}" value="suggestion" ng-model="commentEditRole"> Suggestion
                                                    </label>
                                                </div><!-- ng-show -->
                                            </div>
                                        </form>
                                    </div><!-- controller -->
                                </div><!-- collapse -->
                            </div><!-- ng-show -->
                            % endif
                        </td>
                        <td class="col-xs-1 comment-vote">
                            <div class="row" ng-init="objType='comment'; rated=comment.rated; urlCode=comment.urlCode; totalVotes=comment.voteCount; yesVotes=comment.ups; noVotes=comment.downs; netVotes=comment.netVotes">
                                <div ng-controller="yesNoVoteCtrl">
                                    % if readonly == '0':
                                        ${upDownVoteBlock(readonly = '0')}
                                    % else:
                                        ${upDownVoteBlock(readonly = '1')}
                                    % endif
                                </div>
                            </div>
                        </td>
                </tr>
                % if readonly == '0':
                <tr ng-hide="newCommentLoading || commentsHidden">
                    % if c.authuser:
                        <td class="col-xs-1 comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                        <td class="col-xs-11" style="padding: 10px 0px;">
                            <form class="no-bottom form-inline" ng-submit="submitComment()">
                                <div class="form-group col-sm-10 text-right" style="margin-left: 0; padding-left:0;">
                                    % if c.privs and not c.privs['provisional']:
                                        <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    % else:
                                        <a href="#activateAccountModal" data-toggle='modal'>
                                        <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea></a>
                                    % endif

                                    <small class="left-space" ng-show="type == 'initiative' || type == 'idea'">
                                        <span class="radio inline no-top right-space">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral 
                                        </span>
                                        <span class="radio inline no-top right-space">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro 
                                        </span>
                                        <span class="radio inline no-top right-space">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con 
                                        </span>
                                        <span class="radio inline no-top right-space">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="question"> Question 
                                        </span>
                                        <span class="radio inline no-top right-space">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="suggestion"> Suggestion 
                                        </span>

                                    </small>
                                    
                                </div>
                                <div class="form-group">
                                    % if c.privs and not c.privs['provisional']:
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    % else:
                                        <a href="#activateAccountModal" data-toggle='modal' class="btn btn-primary">Submit</a>
                                    % endif
                                </div>
                            </form>
                        </td>
                    % else:
                        <td class="col-xs-1 comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar topbar-avatar"></td>
                        <td class="col-xs-11" style="padding: 10px;">
                            <a href="#signupLoginModal" data-toggle='modal' class="no-highlight no-hover">
                                <form class="no-bottom form-inline">
                                    <div class="form-group col-sm-10">
                                        <textarea rows="1" class="form-control" style="width:100%" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                        <small class="left-space" ng-show="type == 'initiative' || type == 'idea'">
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con 
                                            </span>
                                        </small>
                                    </div>
                                    <div class="form-group">
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    </div>
                                </form>
                        </td>
                    % endif
                </tr>
                % endif
            </table>
            </div>
            
</%def>

<%def name="ngGeoSelect()">

    <div class="row-fluid">
        <div class="span3">Country:</div>
        <div class="span8">
            <select name="country" ng-model="country" ng-change="changeStateList()">
                <option value="">Select a country</option>
                <option value="united-states">United States</option>
            </select>
        </div><!-- span8 -->
    </div><!-- row-fluid -->
    
    <div class="row-fluid" ng-show="showStateSelect" ng-cloak>
        <div class="span3">State:</div>
        <div class="span8">
            <select name="state" ng-model="state" ng-change="changeCountyList()">
                <option value="0">Select a state</option>
                <option ng-repeat="state in stateList" ng-value="state.StateFullName">{{state.StateFullName}}</option>
            </select>
        </div><!-- span8 -->
    </div><!-- row-fluid -->
    
    <div class="row-fluid" ng-show="showCountySelect" ng-cloak>
        <div class="span3">County:</div>
        <div class="span8">
            <select ng-model="county" ng-change="changeCityList()">
                <option value="0">Select a county</option>
                <option ng-repeat="county in countyList" ng-value="county.County">{{county.County}}</option>
            </select>
        </div><!-- span8 -->
    </div><!-- row -->
    
    <div class="row-fluid" ng-show="showCitySelect" ng-cloak>
        <div class="span3">City:</div>
        <div class="span8">
            <select ng-model="city" ng-change="changePostalList()">
                <option value="0">Select a city</option>
                <option ng-repeat="city in cityList" ng-value="city.City">{{city.City}}</option>
            </select>
        </div><!-- span8 -->
    </div><!-- row-fluid -->
    
    <div class="row-fluid" ng-show="showPostalSelect" ng-cloak>
        <div class="span3">Zip Code:</div>
        <div class="span8">
            <select ng-model="postal">
                <option value="0">Select a zip code</option>
                <option ng-repeat="postal in postalList" ng-value="postal.ZipCode">{{postal.ZipCode}}</option>
            </select>
        </div><!-- span8 -->
    </div><!-- row-fluid -->
</%def>

<%def name="showSupportOppose()">
    <div class="centered" ng-show="positionsLoading" ng-cloak>
        <i class="icon-spinner icon-spin icon-4x"></i>
    </div>
    <div class="row" ng-show="!positionsLoading" ng-cloak>
        <div class="col-sm-6">
            <h4 class="initiative-title">Support</h4>
            <!-- a supporter -->
            <table class="table pro">
                <tr ng-if="support.length == 0">
                    <td>There are no supporters yet.</td>
                </tr>
                <tr ng-repeat="item in support">
                    <td style="vertical-align:top;"><img class="avatar med-avatar" ng-src="{{item.authorPhoto}}"></td>
                    <td>
                        <a ng-href="{{item.authorHref}}"><strong>{{item.authorName}}</strong></a><br><small class="grey">{{item.fuzzyTime}} ago</small>
                        <p ng-init="stringLimit=201" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLessStatement()}</p>
                    </td>
                </tr>
            </table>
        </div>
        <div class="col-sm-6">
            <h4 class="initiative-title">Oppose</h4>
            <!-- an opposer -->
            <table class="table con">
                <tr ng-if="oppose.length == 0">
                    <td>
                        There are no opponents yet.
                    </td>
                </tr>
                <tr ng-repeat="item in oppose"> 
                    <td style="vertical-align:top;"><img class="avatar med-avatar" ng-src="{{item.authorPhoto}}"></td>
                    <td>
                        <a ng-href="{{item.authorHref}}"><strong>{{item.authorName}}</strong></a><br>
                        <small class="grey">{{item.fuzzyTime}} ago</small>
                        <p ng-init="stringLimit=201" class="markdown"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLessStatement()}</p>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</%def>