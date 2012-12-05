<%def name='showTitle(study)'>
           ${study["title"]}
</%def>

<%def name="showSlide(study)">
            <ul class="thumbnails">
              <li class="span6">
                <div class="thumbnail">
                    <img src="/images/corp/casestudies/${study['url']}/${study['image']}" alt="">
                </div> 
              </li>
            </ul>
</%def>

<%def name='status(study)'>
            <span class="label label-${study['statusType']}">${study['statusMessage']}</span>
</%def>

<%def name='respondents(study)'>
             iPad -   <strong>${study['ipadRespondents']}</strong>
</%def>

<%def name='listPartners(study)'>
            <% partners = study['partners']%>
            % for partner in partners:
            <a href="${partner['url']}" target="_blank">${partner['name']}</a>
              % if str(partner) != str(partners[-1]): 
                  ,
              % endif 
            % endfor    
</%def>

<%def name='sponsors(study)'>
            <% sponsors = study['sponsors']%>
            % for sponsor in sponsors:
            <a href="${sponsor['url']}" target="_blank">${sponsor['name']}</a>
              % if str(sponsor) != str(sponsors[-1]):
                  ,
              % endif 
            % endfor    
</%def>

<%def name='dates(study)'>
            ${study['dates']}
</%def>

<%def name='publications(study)'>
            <% publications= study['publications']%>
            % for publication in publications:
            <a href="/images/corp/casestudies/${study['url']}/${publication['url']}" target="_blank">${publication['name']}</a>
            % endfor
            
</%def>

<%def name='background(study)'>
            <p>${study['background']}
            </p>
</%def>

<%def name='solution(study)'>
            <p>${study['solution']}
            </p>
</%def>

<%def name='slideShow(study)'>
              % if len(study['pictures']) > 0:
                </br>
                  <div id="myCarousel" class="carousel slide centered" style="width:600px; background-color:#000000;">
                      <!-- Carousel items -->
                      <div class="carousel-inner"> 
                      <% pictures= study['pictures']%>
                      
                      <% picture = pictures[0] %>
                        <div class="active item"><img class="centered" src="/images/corp/casestudies/${study['url']}/${picture['image']}"/>
                                    <div class="carousel-caption">
                                        <h4>${picture['title']}</h4>
                                        <div style="color:#ffffff;">${picture['caption']}</div>
                                    </div>
                                </div>  
                      
                      

                       <% assclownpics = pictures[1:] %>
                             % for picture in assclownpics:
                                    <div class="item"><img class="centered" src="/images/corp/casestudies/${study['url']}/${picture['image']}"/>
                                        <div class="carousel-caption">
                                            <h4>${picture['title']}</h4>
                                            <div style="color:#ffffff;">${picture['caption']}</div>
                                        </div>
                                    </div>  
                            % endfor
                            


                        </div>
            
                      
                      <!-- Carousel nav -->
                      <a class="carousel-control left" href="#myCarousel" data-slide="prev">&lsaquo;</a>
                      <a class="carousel-control right" href="#myCarousel" data-slide="next">&rsaquo;</a>
                   </div>
              % endif
</%def>


<%def name='results(study)'>
            <p>${study['results']}
              </p> 
              % if len(study['questions']) > 0:
                <% questions= study['questions']%>
                % for question in questions:
                <p><em>${question['title']}</em></p>
                <img class="thumbnail centered" width="600px" src="/images/corp/casestudies/${study['url']}/${question['image']}" alt="">
                </br>
                % endfor
              % endif
</%def>

<%def name='nextSteps(study)'>
            <p>${study["nextSteps"]}
              </p>
</%def>