<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="thingCount(thing, title)">
    <h3 class="profile-count centered">${len(thing)}</h4>
    <div class="green centered"><p>${title}</p></div>
</%def>

<%def name="showWorkshop(workshop)">
    <div class="media profile-workshop">
        <a class="pull-left" ${lib_6.workshopLink(workshop)}>
            <img class="media-object" src="${lib_6.workshopImage(workshop, raw=True) | n}">
        </a>
        <div class="media-body">
            <a ${lib_6.workshopLink(workshop)}><h5 class="media-heading">${workshop['title']}</h5></a>
            Short, one sentence description here
        </div>
    </div>
</%def>

