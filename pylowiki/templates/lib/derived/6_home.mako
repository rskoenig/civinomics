<%def name="homeSlide(item)">
	<div class="span wrap-voting-group slide" style="background-image:url('${item['photo']}'); background-size: cover; background-position: center center;">
	  <a href="${item['link']}">
	    <span class="link-span dark-gradient"></span><!-- used to make entire div a link -->
	    <div class="row-fluid tile-title lead">
	      ${item['title']}
	    </div>
	  </a>
	</div>
</%def>