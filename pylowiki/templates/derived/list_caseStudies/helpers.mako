<%def name='list_studies(studies)'>
    % if len(studies) == 0:
        <p>There does not seem to be anything here!</p>
    % else:
        % for study in studies:
            <div class="span12 well">
                <a class="thumbnail plain span2" href="/corp/caseStudies/${study['url']}">
                    <img src="/images/corp/casestudies/${study['url']}/${study['image']}">  
                </a>
                <div class="span10">
                    <strong><a href="/corp/caseStudies/${study['url']}">${study['title']}</a></strong>
                    <p>
                        ${study['description']}
                    </p>
                    <p><strong>${study['date']}</strong></p>
                </div>
            </div>
        % endfor
    %endif
</%def>

<%def name="list_clientLogos(clients)">
    <ul class="thumbnails plain">
    %for client in clients:
        <li class="client">
            <a href="/corp/caseStudies/${client['url']}">
                <img src="/images/corp/casestudies/${client['logo']}">
            </a>
        </li>
    % endfor
</%def>