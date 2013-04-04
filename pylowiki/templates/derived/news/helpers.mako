<%def name='list_news(articles)'>
    % for article in articles:
        <div class="span8 news">   
            <h4><a href="${article['link']}">${article['title']}</a></h3>
            <strong>${article['source']}</strong>
            <p>${article['date']}</p>
        </div>
    % endfor
</%def>