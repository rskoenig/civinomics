<%namespace name="workshopHelpers" file="/lib/derived/6_workshop_home.mako" />


<%def name="homeSlide(item)">
	<div class="span wrap-voting-group slide" style="background-image:url('${item['photo']}'); background-size: cover; background-position: center center;">
	  <a href="${item['link']}">
	    <span class="link-span dark-gradient"></span><!-- used to make entire div a link -->
	    <div class="row-fluid tile-title lead">Featured Workshop</div>
	    <div class="row-fluid featured">
	    	<table>
	            <tr>
	              <td style="padding-left: 5px;">
	                <span class="featured-title">${item['title']}</span><br>
	     			${workshopHelpers.displayWorkshopFlag(item['item'], 'small')}<span class="featured-scope-title lead">${item['scopeTitle']}</span>
	              </td>
	            </tr>
	         </table>
	    </div>
	  </a>
	</div>
</%def>