<%!    
    import logging
    from ordereddict import OrderedDict
    log = logging.getLogger(__name__)
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.db.discussion import getDiscussionByID
    from pylowiki.lib.db.user import isAdmin
    from pylowiki.lib.db.facilitator import isFacilitator
    from pylowiki.lib.db.resource import getResourcesByParentID
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
		log.info(session)
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
	% if c.isScoped:
            %if thing == 'resource' and (c.w['allowResources'] == '1' or c.isFacilitator or c.isAdmin):
	        <a href="/newResource/${c.w['urlCode']}/${c.w['url']}" title="Click to add a new information resource to this workshop" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>
            %elif thing == 'sresource' and (c.s['allowComments'] == '1' or c.isFacilitator or c.isAdmin):
	        <span class="pull-right resource" style="font-size:xx-small; text-transform:lowercase;"><a href="/newSResource/${c.s['urlCode']}/${c.s['url']}" title="Click to add a new information resource to this suggestion" style="text-decoration:none" class="btn btn-success btn-mini">new<i class="icon-white icon-book"></i></a></span>
            %elif thing == 'suggestion' and (c.w['allowSuggestions'] == '1' or c.isFacilitator or c.isAdmin):
	        <a href="/newSuggestion/${c.w['urlCode']}/${c.w['url']}" title="Click to add a new suggestion to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-pencil"></i></a>
            %elif thing == 'feedback':
	        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/feedback" title="Click to add feedback about this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-volume-up"></i></a>
            %elif thing == 'discussion':
	        <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/addDiscussion" title="Click to add a general discussion topic to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-folder-open"></i></a>
            %endif
	% endif
</%def>

<%def name="fields_alert()">
    % if 'alert' in session:
        <% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">Ã—</button>
            <strong>${alert['title']}</strong>
            ${alert['content']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
    % endif
</%def>

<%def name="list_resources(errorMsg)">
	% if len(c.resources) == 0:
            <p><div class="alert alert-warning">${errorMsg}</div></p>
	% else:
		<div class="civ-col-list">
                <table>
                <tbody>
		% for resource in c.resources:
			<% author = getUserByID(resource.owner) %>
                        <% flags = getFlags(resource) %>
                        % if flags:
                            <% numFlags = len(flags) %>
                        % else:
                            <% numFlags = 0 %>
                        % endif
                        <% disc = getDiscussionByID(resource['discussion_id']) %>
                        <% numComments = 0 %>
                        % if disc:
                            <% numComments = disc['numComments'] %>
                        % endif
			% if resource['type'] == "post":
                            <tr>
                            <td colspan=2>
                               <h3>
                               <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">${resource['title']}</a>
                               </h3>
                               % if len(resource['comment']) > 50:
                                   ${resource['comment'][:50]}... <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a>
                               % else:
                                   ${resource['comment']}
                               % endif
                            </td>
                            </tr>
                            <tr>
                            <td>
                                % if author['pictureHash'] == 'flash':
                                    <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                                % else:
                                    <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                                % endif
                            </td>
                            <td>
                                 <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br>
                                 <span class="badge badge-info" title="Resource comments"><i class="icon-white icon-comment"></i>${numComments}</span>
                                 <span class="badge badge-important"><i class="icon-white icon-flag" title="Resource flags"></i>${numFlags}</span>
                             </td>
                             </tr>
                             <tr>
                             <td colspan=2>
                                 <i class="icon-time"></i> <span class="old">${timeSince(resource.date)}</span> ago | <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">Leave comment</a>
           
                             </td>
                             </tr>
                             <tr>
                             <td colspan=2><hr></td>
                             </tr>
			% endif
		% endfor
                </tbody>
                </table>
                </div>
	% endif
</%def>

<%def name="list_suggestions(errorMsg, doSlider = False)">
	% if len(c.suggestions) == 0:
            <p><div class="alert alert-warning">${errorMsg}</div></p>
	% else:
            <div class="civ-col-list">
            <% counter = 1 %>
            <table>
            <tbody>
            % for suggestion in c.suggestions:
                <% author = getUserByID(suggestion.owner) %>
                <% flags = getFlags(suggestion) %>
                <% resources = getResourcesByParentID(suggestion.id) %>
                % if flags:
                    <% numFlags = len(flags) %>
                % else:
                    <% numFlags = 0 %>
                % endif
                <% disc = getDiscussionByID(suggestion['discussion_id']) %>
                <% numComments = 0 %>
                % if disc:
                    <% numComments = disc['numComments'] %>
                % endif
                <tr>
                <td colspan=3>
                    <h3>
                    <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">${suggestion['title']}</a>
                    </h3>
                    ${suggestion['data'][:50]}... <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">more</a>
                </td>
                </tr>
                <tr>
                <td>
                    % if author['pictureHash'] == 'flash':
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="${author['name']}" title="${author['name']}"></a>
                    % else:
                        <a href="/profile/${author['urlCode']}/${author['url']}"><img src="/images/avatar/${author['directoryNumber']}/profile/${author['pictureHash']}.profile" class="thumbnail" style="width:30px;" alt="${author['name']}" title="${author['name']}"></a>
                    % endif
                </td>
                <td>
                    <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br>
                    <span class="badge badge-info" title="Suggestion information resources"><i class="icon-white icon-book"></i>${len(resources)}</span>
                    <span class="badge badge-info" title="Suggestion comments"><i class="icon-white icon-comment"></i>${numComments}</span>
                    <span class="badge badge-important" title="Suggestion flags"><i class="icon-white icon-flag"></i>${numFlags}</span>
                </td>
                % if 'user' in session and doSlider:
                    <td>
                        <div id="ratings${counter}" class="rating pull-left">
                            <div id="overall_slider" class="ui-slider-container clearfix">
                                % if suggestion.rating:
                                    <div id="${suggestion['urlCode']}_${suggestion['url']}" class="small_slider" data1="0_${suggestion['urlCode']}_${suggestion.rating['rating']}_overall_true_rateSuggestion" data2="${suggestion['url']}"></div>
                                % else:
                                    <div id="${suggestion['urlCode']}_${suggestion['url']}" class="small_slider" data1="0_${suggestion['urlCode']}_0_overall_false_rateSuggestion" data2="${suggestion['url']}"></div>
                                % endif
                             </div> <!-- /#overall_slider -->
                         </div> <!-- /#ratings${counter} -->
                    </td>
                % else:
                    <td>&nbsp;</td>
                % endif
                </tr>
                <tr>
                <td colspan=3>
                    <i class="icon-time"></i> <span class="old">${timeSince(suggestion.date)}</span> ago | <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/suggestion/${suggestion['urlCode']}/${suggestion['url']}">Leave comment</a>
                </td>
                </tr> 
                <tr>
                <td colspan=3><hr></td>
                </tr>
                <% counter += 1 %>
                % endfor
                </tbody>
                </table>
                </div>
% endif
</%def>


<%def name="facilitator()">
	% if len(c.facilitators) == 1:
		Your facilitator
	% else:
		Your facilitators
	% endif
</%def>

<%def name="your_facilitator()">
	% if c.facilitators == False or len(c.facilitators) == 0:
		<div class="alert alert-warning">No facilitators!</div>
	% else:
                <table class="table table-striped">
                <tbody>
		% for facilitator in c.facilitators:
			<% fuser = getUserByID(facilitator.owner) %>
                        <tr>
                        <td>
                            <ul class="unstyled thumbnails">
                            <li>
			    % if fuser['pictureHash'] == 'flash':
				<a href="/profile/${fuser['urlCode']}/${fuser['url']}" class="thumbnail"><img src="/images/avatars/flash.profile" style="width:40px;" alt="${fuser['name']}" title="${fuser['name']}"></a>
			% else:
				<a href="/profile/${fuser['urlCode']}/${fuser['url']}" class="thumbnail"><img src="/images/avatar/${fuser['directoryNumber']}/profile/${fuser['pictureHash']}.profile" style="width:40px;" alt="${fuser['name']}" title="${fuser['name']}"></a>
			    % endif
                            </li>
                            </ul>
                        </td>
                        <td>
                            <a href="/profile/${fuser['urlCode']}/${fuser['url']}">${fuser['name']}</a>
                        </td>
                        </tr>
		% endfor
                </tbody>
                </table>
		% if c.motd and int(c.motd['enabled']) == 1:
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
	<% pages = OrderedDict([("home",""), ("configure", "configure"), ("administrate", "administrate"), ("background", "background"), ("feedback", "feedback"), ("leaderboard", "leaderboard"), ("discussion", "discussion")])  %>

	<ul class="unstyled nav-thing">
	% for li in pages.keys():
                <% lclass="nothingspecial" %>
		% if page == li:
                        <% lclass="current" %>
                % endif
                % if li == 'configure' or li == 'administrate':
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
	<div id="slideshow${counter}" class="slideshow-container">
		<div id="pager${counter}" class="pager">
			<ul id="nav${counter}" class="unstyled">
			</ul>
		</div>
		<div id="prevNext${counter}" class="prevNext">
			<a id="prev${counter}" href="#"><i class='icon-backward icon-white'></i></a>
			<a id="next${counter}" href="#"><i class='icon-forward icon-white'></i></a>
			<!-- <span class="currSlide${counter}"></span> -->
		</div>
		<div class="slideshow${counter}">
                % if c.slides:
                     <% slideList = c.slides %>
                % else:
                     <% slideshowID = c.w['mainSlideshow_id'] %>
                     <% slideList = getAllSlides(slideshowID) %>
                % endif
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
	</div> <!-- /#slideshow${counter} -->
</%def>

<%def name="slideshowHandler(counter)">
	<script type="text/javascript">
    	var onAfter = function(curr, next, opts) {
    		// var index = opts.currSlide + 1;
    		// $('.currSlide${counter}').html(index + "/" + opts.slideCount);
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
        <ul class="thumbnails">
        <li>
	% if c.authuser['pictureHash'] == 'flash':
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}" class="thumbnail"><img src="/images/avatars/flash.profile" alt="${c.authuser['name']}" title="${c.authuser['name']}"></a>
	% else:
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}" class="thumbnail">
			<img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile" alt="${c.authuser['name']}" title="${c.authuser['name']}">
		</a>
	% endif
        </li>
        </ul>
</%def>
