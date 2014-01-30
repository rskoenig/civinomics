<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>

<%def name='showTitle()'>
    <h1 style="text-align:center;">
    	I want to use
    </h1>
</%def>

<%def name='workshopItem()'>
	<a href="/workshops" class="thumbnail">
        <img src="http://placehold.it/260x180">
    </a>
    <div class="caption">
        <h3 style="text-align:center;">Workshops</h3>
    </div>
</%def>

<%def name='surveyItem()'>
	<a href="/surveys" class="thumbnail">
        <img src="http://placehold.it/260x180">
    </a>
    <div class="caption">
        <h3 style="text-align:center;">Surveys</h3>
    </div>
</%def>

<%def name='spacer()'>
    <div class="row">
        <p></p>
    </div>
</%def>