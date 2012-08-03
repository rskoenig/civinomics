<%!    
    import logging
    log = logging.getLogger(__name__)
    from pylowiki.lib.db.flag import getFlags
    from pylowiki.lib.db.discussion import getDiscussionByID
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
## Platform-specific
################################################
<%! 
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.slideshow import getAllSlides
    from pylowiki.lib.fuzzyTime import timeSince
%>

<%def name="add_a(thing)">
	% if c.isScoped or c.isFacilitator:
            %if thing == 'resource':
	        <span class="pull-right ${thing}"><a href="/newResource/${c.w['urlCode']}/${c.w['url']}"><i class="icon-book"></i><i class="icon-plus"></i></a></span>
            %elif thing == 'suggestion':
	        <span class="pull-right ${thing}"><a href="/newSuggestion/${c.w['urlCode']}/${c.w['url']}"><i class="icon-pencil"></i><i class="icon-plus"></i></a></span>
            %endif
	% endif
</%def>

<%def name="list_resources()">
	% if int(c.w['numResources']) == 1:
		<p>No resources.</p>
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
                               ${resource['comment'][:50]}... <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a>
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
                                 <i class="icon-book"></i> <a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a><br>
                                 <span class="badge badge-info"><i class="icon-white icon-comment"></i>${numComments}</span>
                                 <span class="badge badge-important"><i class="icon-white icon-flag"></i>${numFlags}</span>
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
	<%
		pages = {
			"home": "",
			"background": "background",
			"feedback": "feedback",
			"leaderboard": "leaderboard",
			"discussion": "discussion"
		}
	%>
	<ul class="unstyled nav-thing">
	% for li in pages:
		% if page == li:
			<li class="current">
				<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${pages[li]}">${li.capitalize()}</a>
			</li>
		% else:
			<li>
				<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/${pages[li]}">${li.capitalize()}</a>
			</li>
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
                <% slideshowID = c.w['mainSlideshow_id'] %>
                <% slideList = getAllSlides(slideshowID) %>
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
