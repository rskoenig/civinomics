<%!
    from pylowiki.lib.db.surveyAnswer import getAllAnswersForSurvey
    import logging
    log = logging.getLogger(__name__)
%>

<%def name="showTitle(title)">
    <h1 style="text-align:center;">${title}</h1>
</%def>

<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>

<%def name='showBasicTable(results, survey)'>
    <table class="table table-striped">
        <tbody>
            <tr>
                <td>Members:</td>
                <%
                    l = []
                    for item in results:
                        if item.owner not in l:
                            l.append(item.owner)
                    numMembers = len(l)
                %>
                <td>${numMembers}</td>
            </tr>
            <tr>
                <td>Generate new CSV: </td>
                <td><a href="/generateResults/${survey['urlCode']}/${survey['url']}">Click me</a></td>
            </tr>
        </tbody>
    </table>
</%def>

<%def name="previousResults(survey, files)">
    <table class="table">
        <thead>
            <tr>
                <th>Date generated (PST)</th>
                <th>File generated</th>
            </tr>
        </thead>
        <tbody>
            % for tup in files:
                <tr>
                    <td>${tup[1]}</td>
                    <td><a href="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${tup[0]}">${tup[0]}</a></td>
                </tr>
            % endfor
        </tbody>
    </table>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>