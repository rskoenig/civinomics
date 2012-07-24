<%!
   from pylowiki.lib.db.workshop import getWorkshopByID
   from pylons import request
   import webhelpers.paginate as paginate
%>
<%def name='showWorkshops(scopeList)'>
    %if scopeList:
        <% wList = [] %>
        %for wscope in scopeList:
            <% wID = wscope['workshopID'] %>
            <% w = getWorkshopByID(wID) %>
            %if w['deleted'] != 1 and w['startTime'] != '0000-00-00':
               %if w not in wList:
                   <% wList.append(w) %>
               %endif
            %endif
        %endfor
        <% pList = paginate.Page(
                wList, page=int(request.params.get('page', 1)),
                items_per_page = 10, item_count = len(wList)
        ) %>
        %if pList:
            <% pCount = len(pList) %>
            %if pCount == 1:
                <% plural = "" %>
            %else:
                <% plural = "s" %>
            %endif
            <h2>${pCount} Workshop${plural} Scoped For This Public Sphere</h2>
            %for item in pList:
                <div class="row-fluid well">
                <div class="span3">
                % if item['mainImage_hash'] == 'supDawg':
                    <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="mtn" class="left" style = "margin: 5px; width: 120px; height: 80px;"/></a>
                % else:
                    <a href="/workshops/${item['urlCode']}/${item['url']}"><img src="/images/${item['mainImage_identifier']}/${item['mainImage_directoryNum']}/thumbnail/${item['mainImage_hash']}.thumbnail" alt="mtn" class="left" style = "margin: 5px; width: 120px; height: 80px;"/></a>
                % endif
                </div>
                <div class="offset2">
                </div>
                <div class="span6">
                <h4><a href="/workshops/${item['urlCode']}/${item['url']}">${item['title']}</a></h4>
                <span><strong>Public sphere:</strong> ${item['publicScopeTitle']}</span><br>
                <span><strong>Goals:</strong> ${item['goals']}</span>
                </div>
                </div>
            %endfor
            <div class="row-fluid">
               <div class="span5">
               &nbsp;
               </div>
               <div class="span4">
                   <h4>Total Workshops: ${pCount} | View ${pList.pager('~3~')}</h4>
               </div>
            </div>
        %else:
            <h2>No Workshops Scoped For This Public Sphere</h2>
        %endif
    %else:
        <h2>No Workshops Scoped For This Public Sphere</h2>
    %endif
</%def>
