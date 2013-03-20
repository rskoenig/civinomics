     var workshopURL = document.getElementById("workshopTitle").href + "#guider=tour_9";  
    
    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the information resources listing page. Participating members can add links to information resources on the Web which will help educate about the workshop topic.",
            id: "tour_0",
            next: "tour_1",
            title: "The Resources Listing Page",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true
        });
        
        guiders.createGuider({
            attachTo: "#workshopTitle",
            buttons: [{name: "next"}],
            description: "Remember, you can click on the workshop name to return to the workshop main page.",
            id: "tour_1",
            next: "tour_2",
            title: "Workshop Name.",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopTitle",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        guiders.createGuider({
            attachTo: "#addButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "You need a Civinomics account, and need to be logged in to add a new information resource.",
            id: "tour_2",
            prev: "tour_1",
            next: "tour_3",
            title: "Login To Add a New Resource",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#addButton",
            overlay: "true",
            xButton: true,
            position: 9
        });
        
        guiders.createGuider({
            attachTo: "#content_0",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "This is the resource name which links to the resource web page, the name of the author which links to their profile page and a link to the comments about this resource. ",
            id: "tour_3",
            prev: "tour_2",
            next: "tour_4",
            title: "Resource Listing",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#content_0",
            overlay: "true",
            xButton: true,
            position: 12
        });
        
        guiders.createGuider({
            attachTo: "#author_0",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "This is the avatar of the author of the resource. Click it to display their profile page.",
            id: "tour_4",
            prev: "tour3",
            next: "tour_5",
            title: "Resource Author",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#author_0",
            overlay: "true",
            xButton: true,
            position: 3
        });
        
        guiders.createGuider({
            attachTo: "#vote_0",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=workshopURL; }}],
            description: "This is the current vote count for the resource. Participants can click on the up chevron to vote the resource up, or the down chevron to vote the resource down. The votes reflect participants ranking of the resource for value or veracity.",
            id: "tour_5",
            prev: "tour4",
            next: "tour_5",
            title: "Resource Voting",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#vote_0",
            overlay: "true",
            xButton: true,
            position: 3
        });

    });
