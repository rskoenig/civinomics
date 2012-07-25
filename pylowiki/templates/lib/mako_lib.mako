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
    <img src = "${avatarURL}" style = "width: ${size}px; float: ${float}; padding-right: 5px; vertical-align: middle;">
</%def>

## Bootstrap

<%! 
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.slideshow import getAllSlides
    from pylowiki.lib.fuzzyTime import timeSince
%>

<%def name="add_a(thing)">
	% if c.isScoped or c.isFacilitator:
            %if thing == 'resource':
	        <span class="pull-right ${thing}"><a href="/newResource/${c.w['urlCode']}/${c.w['url']}"><i class="icon-plus"></i></a></span>
            %elif thing == 'suggestion':
	        <span class="pull-right ${thing}"><a href="/newSuggestion/${c.w['urlCode']}/${c.w['url']}"><i class="icon-plus"></i></a></span>
            %endif
	% endif
</%def>

<%def name="list_resources()">
	% if int(c.w['numResources']) == 1:
		<p>No resources.</p>
	% else:
		<ul class="unstyled civ-col-list">
		% for resource in c.resources:
			<% author = getUserByID(resource.owner) %>
			% if resource['type'] == "post":
				<li class="post">
					<h3>
						<a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">
							${resource['title']}
						</a>
					</h3>
					<p>
						<img src="/images/glyphicons_pro/glyphicons/png/glyphicons_039_notes@2x.png" height="50" width="40" style="float: left; margin-right: 5px;">${resource['comment'][:50]}...
					</p>
					<p><a href="/workshop/${c.w['urlCode']}/${c.w['url']}/resource/${resource['urlCode']}/${resource['url']}">more</a></p>
					<p>
						posted by 
						<a href="/profile/${author['urlCode']}/${author['url']}">${author['name']}</a>
						<span class="old">${timeSince(resource.date)}</span> ago
					</p>
				</li>
			% endif
		% endfor
		</ul>
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
                <ul class="unstyled">
		% for facilitator in c.facilitators:
			<% fuser = getUserByID(facilitator.owner) %>
			% if fuser['pictureHash'] == 'flash':
				<li><a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatars/flash.profile" width="40"> ${fuser['name']}</a></li>
			% else:
				<li><a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatar/${fuser['directoryNumber']}/profile/${fuser['pictureHash']}.profile" width="40"> ${fuser['name']}</a></li>
			% endif
		% endfor
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
			"stats": "stats",
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
	% if c.authuser['pictureHash'] == 'flash':
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}"><img src="/images/avatars/flash.profile"></a>
	% else:
		<a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">
			<img src="/images/avatar/${c.authuser['directoryNumber']}/profile/${c.authuser['pictureHash']}.profile">
		</a>
	% endif
</%def>
