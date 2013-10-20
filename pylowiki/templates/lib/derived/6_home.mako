<%namespace name="workshopHelpers" file="/lib/derived/6_workshop_home.mako" />


<%def name="homeSlide(item)">
	<div class="span wrap-voting-group slide" style="background-image:url('${item['photo']}'); background-size: cover; background-position: center center;">
	  <a href="${item['link']}">
	    <span class="link-span dark-gradient"></span><!-- used to make entire div a link -->
	    <div class="row-fluid tile-title lead">Featured Workshop</div>
	    <div class="row-fluid featured">
	    	<table>
	            <tr>
	              <td style="vertical-align: top; padding-top: 3px;">
	                ${workshopHelpers.displayWorkshopFlag(item['item'], 'small')}
	              </td>
	              <td style="padding-left: 5px;">
	                <span class="featured-title lead">${item['title']}</span><br>
	     			<span class="featured-scope-title">${item['scopeTitle']}</span>
	              </td>
	            </tr>
	         </table>
	    </div>
	  </a>
	</div>
</%def>