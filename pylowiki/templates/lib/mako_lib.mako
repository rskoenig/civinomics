<%!    
    import logging
    from ordereddict import OrderedDict
    log = logging.getLogger(__name__)
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.db.discussion import getDiscussionByID
    from pylowiki.lib.db.user import isAdmin, getUserByID
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.resource import getResourcesByParentID
    from pylowiki.lib.db.workshop import getWorkshop, isScoped
    
%>

################################################
## General
################################################

<%def name="return_to()">

    <% 
    session['return_to'] = request.path_info 
    session.save()
    %>

</%def>

<%def name="gravatar( email, size, float='none' )">
    <%from hashlib import md5%>
    <% gravatar = md5(email).hexdigest() %>
    <img src="http://www.gravatar.com/avatar/${gravatar}.jpg?s=${size}&d=http%3A%2F%2F${request.environ.get("HTTP_HOST")}%2Fimages%2Fpylo.jpg" style="width: ${size}px; float: ${float}; padding-right: 5px; vertical-align: middle;">
</%def>

<%def name="avatar( hash, size, float='none' )">
    <% avatarURL = "/images/avatars/%s.thumbnail" %(hash) %>
    <ul class="thumbnails">
    <li>
        <div class="thumbnail">
            <img src= "${avatarURL}" style = "width: ${size}px; float: ${float}; padding-right: 5px; vertical-align: middle;">
        </div>
    </li>
    </ul>
</%def>

<%def name="setProduct()">
	<%
		if 'survey' in request.path_info:
			session['product'] = 'surveys'
		elif 'workshop' in request.path_info:
			session['product'] = 'workshops'
		session.save()
	%>
</%def>

################################################
## Survey-specific
################################################

<%def name="setLastPage(pageNum, survey, slide)">
    <% 
        if slide['surveySection'] == 'before':
            key = '%s_%s_lastPage' %(survey['urlCode'], survey['url'])
            if key in session:
                if int(session[key]) < pageNum:
                    session[key] = pageNum
            else:
                session[key] = pageNum
            session.save()
    %>
</%def>

<%def name="setCurrentSurveyPage(survey, slide)">
    <% 
        if slide.id in map(int, survey['slides'].split(',')):
            key = '%s_%s_currentPage' %(survey['urlCode'], survey['url'])
            session[key] = int(slide['slideNum'])
            session.save()
    %>
</%def>

################################################
## Workshop-specific
################################################
<%! 
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.slideshow import getAllSlides
    from pylowiki.lib.fuzzyTime import timeSince
%>

<%def name="add_a(thing)">
	% if c.isScoped or c.isFacilitator or c.isAdmin:
            %if thing == 'resource' and (c.w['allowResources'] == '1' or c.isFacilitator or c.isAdmin):
	        <a href="/newResource/${c.w['urlCode']}/${c.w['url']}" style="letter-spacing:normal;" title="Click to add a new information resource to this workshop" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>
            %elif thing == 'sresource' and (c.s['allowComments'] == '1' or c.isFacilitator or c.isAdmin):
	        <a href="/newSResource/${c.s['urlCode']}/${c.s['url']}" title="Click to add a new information resource to this suggestion" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>
            %elif thing == 'suggestion' and (c.w['allowSuggestions'] == '1' or c.isFacilitator or c.isAdmin):
	        <a href="/newSuggestion/${c.w['urlCode']}/${c.w['url']}" title="Click to add a new suggestion to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-pencil"></i></a>
            %elif thing == 'discussion':
	        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Click to add a general discussion topic to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-folder-open"></i></a>
            %endif
    % else:
        % if 'user' not in session:
            %if thing == 'resource':
                <a href="/" style="letter-spacing:normal;" title="Sign Up or Log In to participate!" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>
            %elif thing == 'sresource':
                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>
            %elif thing == 'suggestion':
                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-pencil"></i></a>
            %elif thing == 'discussion':
                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-folder-open"></i></a>
            %endif
        % endif
	% endif
</%def>

<%def name="add_a_text(thing, prefix)">
	% if c.isScoped or c.isFacilitator or c.isAdmin:
            %if thing == 'resource' and (c.w['allowResources'] == '1' or c.isFacilitator or c.isAdmin):
	        ${prefix} <a href="/newResource/${c.w['urlCode']}/${c.w['url']}" title="Click to add a new information resource to this workshop">Add Resource</a>
            %elif thing == 'sresource' and (c.s['allowComments'] == '1' or c.isFacilitator or c.isAdmin):
	        ${prefix} <a href="/newSResource/${c.s['urlCode']}/${c.s['url']}" title="Click to add a new information resource to this suggestion">Add Resource</a>
            %elif thing == 'suggestion' and (c.w['allowSuggestions'] == '1' or c.isFacilitator or c.isAdmin):
	        ${prefix} <a href="/newSuggestion/${c.w['urlCode']}/${c.w['url']}" title="Click to add a new suggestion to this workshop">Add Suggestion</a>
            %elif thing == 'discussion':
	        ${prefix} <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Click to add a general discussion topic to this workshop">Add Discussion Topic</a>
            %endif
	% endif
</%def>

<%def name="fields_alert()">
    % if 'alert' in session:
        <% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">x</button>
            <strong>${alert['title']}</strong>
            ${alert['content']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
    % endif
</%def>

<%def name="list_resources(errorMsg, numDisplay = 10)">
	% if len(c.resources) == 0:
            <p><div class="alert alert-warning">${errorMsg}</div></p>
	% else:
        <%
            if numDisplay == 0:
                rList = c.paginator
            else:
                rList = c.resources
        %>
		<div class="civ-col-list">
            <% counter = 0 %>
            <ul class="unstyled civ-col-list">
		% for resource in rList:
			<% 
                author = getUserByID(resource.owner)
                flags = getFlags(resource) 
                
                if flags:
                    numFlags = len(flags)
                else:
                    numFlags = 0
             
                disc = getDiscussionByID(resource['discussion_id'])
                numComments = 0 
            
                if disc:
                    numComments = disc['numComments']
            %>

			% if resource['type'] == "post":
                <% rating = int(resource['ups']) - int(resource['downs']) %>
                <li>
                    <div class="row-fluid">
                        <h3>
                            <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">${resource['title']}</a>
                        </h3>
                        % if resource['deleted'] == '0':
                            % if len(resource['comment']) > 50:
                                ${resource['comment'][:50]}... <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a>
                            % else:
                                ${resource['comment']}
                            % endif
                        % else:
                            Deleted
                        % endif
                    </div><!-- row-fluid -->
                    <div class="row-fluid">
                        <div class="span2">
                            % if author['pictureHash'] == 'flash':
                                <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                            % else:
                                <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                            % endif
                        </div><!-- span2 -->
                        <div class="span10">
                             <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br>
                             <span class="badge badge-info" title="Resource rating"><i class="icon-white icon-ok-sign"></i> ${rating}</span>
                             <span class="badge badge-info" title="Resource comments"><i class="icon-white icon-comment"></i>${numComments}</span>
                             <span class="badge badge-inverse"><i class="icon-white icon-flag" title="Resource flags"></i>${numFlags}</span>
                             <br />
                             <i class="icon-time"></i> Added <span class="old">${timeSince(resource.date)}</span> ago<br /> 
                             <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">Rate and discuss this resource</a>
                             <br /><br />
                         </div><!-- span10 -->
                    </div><!-- row-fluid -->
                </li>
			% endif
            <% counter += 1 %>
            % if counter == numDisplay:
                <% break %>
            % endif
		% endfor
            </ul>
        </div>
	% endif
</%def>

<%def name="totalResources()">
        <% 
            if c.resources:
                total = len(c.resources)
            else:
                total = 0 
        %>
        <br />
        <p class="total">
                ${total}<br>
                <span>Resources</span><br />
                % if len(c.resources) > 15:
                    <span>Display Page ${ c.paginator.pager('~3~')}</span><br />
                % endif
                <span><a href="/workshop/${c.w['urlCode']}/${c.w['url']}">Back to Workshop</a></span>
        </p>
</%def>

<%def name="list_suggestions(sList, errorMsg, numDisplay, doSlider = 0)">
	% if len(sList) == 0:
            <p><div class="alert alert-warning">${errorMsg}</div></p>
	% else:
            <%
                if doSlider == 0:
                    badgeSpan = "span10"
                    slideSpan = "span0" 
                else:
                    if numDisplay == 0:
                        badgeSpan = "span2"
                        slideSpan = "span8"
                        sliderSize="normal"
                    else:
                        badgeSpan = "span4"
                        slideSpan = "span5"
                        sliderSize="small"
            %>

            <div class="civ-col-list">
            <% counter = 1 %>
            <ul class="unstyled civ-col-list">
            % for suggestion in sList:
                <% 
                    author = getUserByID(suggestion.owner)
                    workshop = getWorkshop(suggestion['workshopCode'], suggestion['workshopURL'])
                    scoped = isScoped(c.authuser, workshop)
                    flags = getFlags(suggestion)
                    resources = getResourcesByParentID(suggestion.id)
                    if flags:
                        numFlags = len(flags)
                    else:
                        numFlags = 0
                    disc = getDiscussionByID(suggestion['discussion_id'])
                    numComments = 0
                    if disc:
                        numComments = disc['numComments']
                %>
                <li>
                <div class="row-fluid">
                    <h3>
                    <a href="/workshop/${suggestion['workshopCode']}/${suggestion['workshopURL']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a>
                    </h3>
                    % if suggestion['deleted'] == '0':
                        ${suggestion['data'][:50]}... <a href="/workshop/${suggestion['workshopCode']}/${suggestion['workshopURL']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">more</a>
                    % else:
                        Deleted
                    % endif
                    <br /><br />
                </div><!-- row-fluid -->
                <div class="row-fluid">
                    <div class="span2">
                    % if author['pictureHash'] == 'flash':
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                    % else:
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                    % endif
                    </div><!-- span2 -->
                    <div class="${badgeSpan}">
                    <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br />
                    <span class="badge badge-info" title="Suggestion information resources"><i class="icon-white icon-book"></i>${len(resources)}</span>
                    <span class="badge badge-info" title="Suggestion comments"><i class="icon-white icon-comment"></i>${numComments}</span>
                    <span class="badge badge-inverse" title="Suggestion flags"><i class="icon-white icon-flag"></i>${numFlags}</span>
                    </div><!-- ${badgeSpan} -->
                % if 'user' in session and scoped and doSlider == 1 and suggestion['disabled'] == '0' and suggestion['deleted'] == '0':
                    <div class="${slideSpan}">
                        <div id="ratings${counter}" class="rating wide pull-right">
                            <div id="overall_slider" class="ui-slider-container">
                                % if suggestion.rating:
                                    <div id="${suggestion['urlCode']}_${suggestion['url']}" class="${sliderSize}_slider" data1="0_${suggestion['urlCode']}_${suggestion.rating['rating']}_overall_true_rateSuggestion" data2="${suggestion['url']}"></div>
                                % else:
                                    <div id="${suggestion['urlCode']}_${suggestion['url']}" class="${sliderSize}_slider" data1="0_${suggestion['urlCode']}_0_overall_false_rateSuggestion" data2="${suggestion['url']}"></div>
                                % endif
                             </div> <!-- /#overall_slider -->
                         </div> <!-- /#ratings${counter} -->
                    </div><!-- ${slideSpan} -->
                % else:
                    % if 'user' not in session and doSlider == 1 and suggestion['disabled'] == '0' and suggestion['deleted'] == '0':
                        <div class="${slideSpan}">
                            <div id="ratings${counter}" class="rating wide pull-right">
                                <div id="overall_slider" class="ui-slider-container">
                                    <div id="${suggestion['urlCode']}_${suggestion['url']}" class="${sliderSize}_slider"  data2="${suggestion['url']}"></div>
                                 </div> <!-- /#overall_slider -->
                             </div> <!-- /#ratings${counter} -->
                        </div><!-- ${slideSpan} -->
                    % endif
                % endif
                </div><!-- row-fluid -->
                <div class="row-fluid">
                    <i class="icon-time"></i> Added <span class="old">${timeSince(suggestion.date)}</span> ago 
                    % if 'user' in session and scoped and doSlider == '1':
                        | <a href="/workshop/${suggestion['workshopCode']}/${suggestion['workshopURL']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">Leave comment</a>
                    % endif
                    <br /><br />
                </div><!-- row-fluid -->
                </li>
                <% 
                    counter += 1
                    if counter == int(numDisplay):
                        break
                    endif
                %>
            % endfor
            </ul>
            % if c.paginator and (len(c.paginator) != len(c.suggestions)):
                <% state = True %>
                % for p in c.paginator:
                    <% state = not state %>
                % endfor
                <p>Total Suggestions: ${c.count} | View ${ c.paginator.pager('~3~') }</p>
            % endif
            </div>
    % endif
</%def>

<%def name="totalSuggestions()">
    <%
        if c.suggestions:
            total = len(c.suggestions)
        else:
            total = 0
    %>
        <br />
        <p class="total">
                ${total}<br>
                <span>Suggestions</span><br />
                % if len(c.suggestions) > 15:
                    <span>Display Page ${ c.paginator.pager('~3~')}</span><br />
                % endif
                <span><a href="/workshop/${c.w['urlCode']}/${c.w['url']}">Back to Workshop</a></span>
        </p>
</%def>

<%def name="facilitator()">
	% if len(c.facilitators) == 1:
		facilitator
	% else:
		facilitators
	% endif
</%def>

<%def name="your_facilitator()">
    % if c.facilitators == '0' or len(c.facilitators) == 0:
        <div class="alert alert-warning">No facilitators!</div>
    % else:
        <ul class="unstyled civ-col-list">
        % for facilitator in c.facilitators:
            <li>
            <% fuser = getUserByID(facilitator.owner) %>
            <div class="row-fluid">
                <div class="span2">
                % if fuser['pictureHash'] == 'flash':
                    <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatars/flash.profile" style="width:40px;" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a>
                % else:
                    <a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatar/${fuser['directoryNumber']}/profile/${fuser['pictureHash']}.profile" style="width:40px;" alt="${fuser['name']}" title="${fuser['name']}" class="thumbnail"></a>
                % endif
                </div><!-- span2 -->
                <div class="span8">
                    <a href="/profile/${fuser['urlCode']}/${fuser['url']}">${fuser['name']}</a>
                </div><!-- span8 -->
            </div><!-- row-fluid --> 
            </li>
        % endfor
        </ul>
        % if c.motd and int(c.motd['enabled']) == '1':
            <p>Facilitator message:</p> ${c.motd['messageSummary']}
        % else:

        % endif
    % endif
</%def>

<%def name="civ_col_img()">
	<script type="text/javascript">
		$(window).load(function() {
			$('.civ-img-cap').each(function(){
				$(this).width($(this).find('img').width());
			})
			$('.civ-img-cap .cap').css({'textAlign': 'left', 'right': 0});
		})
	</script>
</%def>

<%def name="nav_thing(page)">
    <%
        if 'user' in session:
	       pages = OrderedDict([("home",""), ("configure", "configure"), ("administrate", "administrate"), ("background", "background"), ("leaderboard", "leaderboard"), ("discussion", "discussion")])
        else:
	       pages = OrderedDict([("home",""), ("background", "background"), ("discussion", "discussion")])
    %>

	<ul class="unstyled nav-thing">
	% for li in pages.keys():
        <% lclass="nothingspecial" %>
		% if page == li:
            <% lclass="current" %>
        % endif
        % if li == 'configure' or li == 'administrate':
            % if c.conf['read_only.value'] == 'true':
                <% continue %>
            % endif
            % if 'user' in session and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
			    <li class="${lclass}"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${pages[li]}">${li.capitalize()}</a></li>
            % endif
        % else:
            <li class="${lclass}"><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${pages[li]}">${li.capitalize()}</a></li>
		% endif
	% endfor
	</ul> <!-- /.nav-thing -->
</%def>

<%def name="slideshow(counter)">
	<div id="slideshow${counter}" class="slideshow-container" style="border:1px solid black; padding:4px;">
		<div id="pager${counter}" class="pager">
			<ul id="nav${counter}" class="unstyled">
			</ul>
		</div>
		<div id="prevNext${counter}" class="prevNext">
			<a id="prev${counter}" href="#"><i class='icon-backward icon-white'></i></a>
			<a id="next${counter}" href="#"><i class='icon-forward icon-white'></i></a>
		</div>
		<div class="slideshow${counter}">
                <% 
                    if c.slides:
                        slideList = c.slides
                    else:
                        slideshowID = c.w['mainSlideshow_id']
                        slideList = getAllSlides(slideshowID)
                %>
                %for slide in slideList:
                    %if slide['deleted'] != '1':
                        % if slide['pictureHash'] == 'supDawg':
			<div class="slide">
				<a title="${slide['title']}<br/>${slide['caption']}" href="#">
                                <img src="/images/slide/slideshow/${slide['pictureHash']}.slideshow" alt="<strong>${slide['title']}</strong> ${slide['caption']}"/>
				</a>
			</div> <!-- /.slide -->
                        %else:
			<div class="slide">
				<a title="${slide['title']}<br/>${slide['caption']}" href="#">
                                <img src="/images/slide/${slide['directoryNumber']}/slideshow/${slide['pictureHash']}.slideshow" alt="<strong>${slide['title']}</strong> ${slide['caption']}"/>
				</a>
			</div> <!-- /.slide -->
                        %endif
                     %endif
                %endfor
		</div> <!-- /.slideshow -->
		<div class="caption${counter} caption"></div>
	</div> <!-- slideshow -->
</%def>

<%def name="slideshowHandler(counter)">
	<script type="text/javascript">
    	var onAfter = function(curr, next, opts) {
			$('.caption${counter}').html(next.firstElementChild.title);
    	}
    	var pagerBuilder = function(index, slide) {
    		img = $(slide).find('img');
    		return "<li><a href='#'><img src='" + img.attr('src') + "'></a></li>"
    	}
    	$(function(){
    		$('.caption${counter}').html(
    			$(this).parent('#slideshow${counter}').find('.slideshow>slide:visible').find('a').attr('title')
			);
	    	$('.slideshow${counter}')
	    		.cycle({
		    		fx: 'fade',
		    		pause: true,
		    		next: $('#next${counter}'),
		    		prev: $('#prev${counter}'),
		    		after: onAfter,
		    		timeout: 0,
		    		pager: '#nav${counter}',
		    		pagerAnchorBuilder: pagerBuilder
		    	})
		    	.touchwipe({
		    		wipeLeft: function() {
		    			$('#next${counter}').click();
		    		},
		    		wipeRight: function() {
		    			$('#prev${counter}').click();
		    		},
		    		min_move_x: 20,
		    		min_move_y: 20,
		    		preventDefaultEvents: true
				});
			$('#pager${counter}').hover(
				function(){
					$(this).animate({
						'opacity': 100
					}, 1000);
				},
				function(){
					$(this).animate({
						'opacity': 0
					}, 1000);
				}
			);
    	})
	</script>
</%def>

<%def name="displayProfilePicture()">
        <br />
	% if c.authuser['pictureHash'] == 'flash':
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}"><img src="/images/avatars/flash.profile" alt="${c.authuser['name']}" title="${c.authuser['name']}" style="display:block; margin-left:auto; margin-right:auto; vertical-align:middle;" class="thumbnail"></a>
	% else:
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
			<img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile" alt="${c.authuser['name']}" title="${c.authuser['name']}" style="display:block; margin-left:auto; margin-right:auto; vertical-align:middle;" class="thumbnail">
		</a>
	% endif
</%def>

<%def name="displayWorkshopHeader(page)">
   <div class="row-fluid">
       <div class="span2">
            % if c.w['mainImage_hash'] == 'supDawg':
                <a href="/workshops/${c.w['urlCode']}/${c.w['url']}"><img src="/images/${c.w['mainImage_identifier']}/thumbnail/${c.w['mainImage_hash']}.thumbnail" class="thumbnail" alt="${c.w['title']}" title="${c.w['title']}" style="width: 120px; height: 80px;"/></a>
            % else:
                <a href="/workshops/${c.w['urlCode']}/${c.w['url']}"><img src="/images/${c.w['mainImage_identifier']}/${c.w['mainImage_directoryNum']}/thumbnail/${c.w['mainImage_hash']}.thumbnail" alt="${c.w['title']}" title="${c.w['title']}" class="thumbnail left" style = "width: 120px; height: 80px;"/></a>
            % endif
        </div><!-- span3 -->
        <div class="span9">
            <h1><a href="/workshop/${c.w['urlCode']}/${c.w['url']}">${c.w['title']}</a></h1>
            <br/>
            ${nav_thing(page)}
            <!--
            <img src="/images/glyphicons_pro/glyphicons_halflings/png/glyphicons_halflings_134_globe.png"> ${c.w['publicScopeTitle']} &nbsp; &nbsp; 
            <i class="icon icon-cog"></i> ${c.w['goals']}
            -->
        </div><!-- span9 -->
   </div><!-- row-fluid -->
</%def>

<%def name="displayFeedbackSlider()">
    % if "user" in session and c.isScoped:
        <h2 class="civ-col"><i class="icon-volume-up"></i> Feedback</h2>
        <div class="civ-col-inner">
            <div class="well workshop_header">
                Provide feedback for the workshop facilitators.
                What do you think about the running of this workshop?
                <br /> <br />

                <div id="ratings0" class="rating pull-left">
                    <div id="overall_slider" class="ui-slider-container clearfix">
                        % if c.rating:
                            <div id="${c.w['urlCode']}_${c.w['url']}" class="small_slider" data1="0_${c.w['urlCode']}_${c.rating['rating']}_overall_true_rateFacilitation" data2="${c.w['url']}"></div>
                        % else:
                            <div id="${c.w['urlCode']}_${c.w['url']}" class="small_slider" data1="0_${c.w['urlCode']}_0_overall_false_rateFacilitation" data2="${c.w['url']}"></div>
                        % endif
                    </div><!-- overall_slider -->
                </div><!-- ratings0 -->
                <br /> <br />
                <br /> <br />
            </div><!-- well -->
        </div><!-- civ-col-inner -->
    % endif
</%def>

<%def name="displayEvents()">
    % if c.events:
        <h2 class="civ-col">Change Log</h2>

        <ul class="unstyled">
        % for e in c.events:
            <% eOwner = getUserByID(e.owner) %>
            <li>${e['title']} : by <a href="/profile/${eOwner['urlCode']}/${eOwner['url']}">${eOwner['name']}</a> ${e.date} : ${e['data']}</li>
        % endfor
        </ul>
    % endif
</%def>
