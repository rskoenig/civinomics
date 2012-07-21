<%!
	from pylowiki.lib.db.user import getUserByID
%>

<%def name="workshopBlurb()">
	<p><strong>Workshops</strong> are an online space where <strong>Members</strong> residing in the participating 
<strong>Public Sphere </strong> make contributions, as individuals
working in a community, to accomplish the workshop <strong>Goals</strong>.
These contributions can take the form of links to information 
<strong>Resources</strong> to help inform the workshop topic, <strong>Suggestions</strong> toward accomplishing the goals of the workshop,or <strong>Comments</strong> offering insights to the information and
contributions in the workhop. Members also <strong>Rank</strong> the
contributions of others to give an aggregate community sense of the
credibility and/or value of the contribution (and hence, the contributor).
<br /> <br />
Rate this workshop. Use the comments to ask questions of the
<strong>Facilitator</strong>, make suggestions as to ways to improve
the workshop, or otherwise chime in on how things are done in this workshop.
Your facilitator and the team at Civinomics need the feedback to build
your community.
</p>
</%def>

<%def name="displaySlider()">
	% if "user" in session:
		% if c.rating:
			<div id="overall_slider" class="ui-slider-container">
				<div id="${c.w['urlCode']}_${c.w['url']}" class="normal_slider" data1="0_${c.w['urlCode']}_${c.w['url']}_${c.rating['rating']}_overall_true_rateFacilitation" data2="${c.w['url']}"></div>
			</div>
		% else:
			<div id="overall_slider" class="ui-slider-container">
				<div id="${c.w['urlCode']}_${c.w['url']}" class="normal_slider" data1="0_${c.w['urlCode']}_${c.w['url']}_0_overall_false_rateFacilitation" data2="${c.w['url']}"></div>
			</div>
		% endif
	% endif
</%def>

<%def name="your_facilitator()">
	% if c.facilitators == False or len(c.facilitators) == 0:
		<div class="alert alert-warning">No facilitators!</div>
	% else:
		% for facilitator in c.facilitators:
			<% fuser = getUserByID(facilitator.owner) %>
			% if fuser['pictureHash'] == 'flash':
				<a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatars/flash.profile" width="50"> ${fuser['name']}</a>
			% else:
				<a href="/profile/${fuser['urlCode']}/${fuser['url']}"><img src="/images/avatar/${fuser['directoryNumber']}/profile/${fuser['pictureHash']}.profile" width="50"> ${fuser['name']}</a>
			% endif
		% endfor
	% endif
</%def>
