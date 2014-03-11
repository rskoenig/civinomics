<%def name="listenerFacilitationInvite()">
    <div ng-if="isRead(read)">
        <div class="media">
            <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left">
            <div class="media-body">
                <p>
                    <a ng-href="{{userLink}}">{{userName}}</a>
                    invites you to facilitate 
                    <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                </p>
                <p>
                    (You have already responded by 
                    {{responseAction}})
                </p>
            </div>
        </div>
    </div> <!-- end if read -->
    <div ng-if="notRead(read)">
        <form method="post" name="inviteListener" id="inviteListener" action="{{formLink}}">
            <input type="hidden" name="workshopCode" value="{{itemCode}}">
            <input type="hidden" name="workshopURL" value="{{itemUrl}}">
            <input type="hidden" name="messageCode" value="{{messageCode}}">
            <div class="media">
                <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left">
                <div class="media-body">
                    <p>
                        <a ng-href="{{userLink}}">{{userName}}</a>
                        invites you to
                        {{action}}
                        <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                    </p>
                    <p>
                        {{messageText}}
                    </p>
                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{action}} the workshop">Accept</button>
                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{action}} the workshop">Decline</button>
                </div>
            </div>
        </form>
    </div> <!-- end if not read -->
</%def>

<%def name="listenerSuggestion()">
    <div class="media">
        <div class="media-body">
            <p>
                Member 
                <a ng-href="{{userLink}}">{{userName}}</a>
                has a listener suggestion for workshop 
                <a ng-href="{{itemLink}}">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
        </div>
    </div>
</%def>

<%def name="authorInvite()">
    <div ng-if="isRead(read)">
        <div class="media">
            <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left">
            <div class="media-body">
                <p>
                    <a ng-href="{{userLink}}">{{userName}}</a>
                    invites you to facilitate 
                    <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                </p>
                <p>
                    (You have already responded by 
                    {{responseAction}})
                </p>
            </div>
        </div>
    </div> <!-- end if read -->
    <div ng-if="notRead(read)">
        <form method="post" name="inviteFacilitate" id="inviteFacilitate" action="{{formLink}}">
            <input type="hidden" name="initiativeCode" value="{{itemCode}}">
            <input type="hidden" name="initiativeURL" value="{{itemUrl}}">
            <input type="hidden" name="messageCode" value="{{messageCode}}">
            <div class="media">
                <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left">
                <div class="media-body">
                    <p>
                        <a ng-href="{{userLink}}">{{userName}}</a>
                        invites you to 
                        {{action}} 
                        <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                    </p>
                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{action}} the initiative">Accept</button>
                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{action}} the initiative">Decline</button>
                </div>
            </div>
        </form>
    </div> <!-- end if not read -->
</%def>

<%def name="authorResponse()">
    <div class="media">
        <div class="media-body">
            <p>
                <a ng-href="{{userLink}}">{{userName}}</a>
                <span>{{messageText}}</span>
                <a ng-href="{{itemLink}}">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="commentResponse()">
    <div class="media">
        <div class="media-body">
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{commentData}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="commentOnPhotoOnInitiative()">
    <div class="media">
        <div class="media-body">
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{commentData}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="commentOnResource()">
    <div class="media">
        <div class="media-body">
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="commentOnUpdate()">
    <div class="media">
        <div class="media-body">
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedPhoto()">
    <div class="media">
        <div class="media-body">
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your photo:
                <!-- note: photo needs a link to the unpublished page, link to src of image and title -->
                <img ng-src="{{itemLink}}" class="green green-hover" title="{{itemTitle}}" alt="{{itemTitle}}">
            </p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiative()">
    <div class="media">
        <div class="media-body">
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiativeResource()">
    <div class="media">
        <div class="media-body">
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative resource:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiativeUpdate()">
    <div class="media">
        <div class="media-body">
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative update:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedAdopted()">
    <div class="media">
        <div class="media-body">
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                You posted:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
        </div>
    </div>
</%def>