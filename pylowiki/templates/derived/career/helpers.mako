<%def name='showTitle(career)'>
           ${career["title"]}
</%def>

<%def name='showComLocation(career)'>
            ${career["commitment location"]}
</%def>

<%def name='showDescription(career)'>
            ${career["description"]}
</%def>

<%def name='showRequirements(career)'>
            <ul>
              <% requirements = career['requirements']%>
              % for requirement in requirements:
                    <li>${requirement}</li>
              % endfor
            </ul>
</%def>

<%def name='showRecommendeds(career)'>
            <ul>
              <% recommendeds = career['recommendeds']%>
              % for recommended in recommendeds:
                    <li>${recommended}</li>
              % endfor
            </ul>
</%def>