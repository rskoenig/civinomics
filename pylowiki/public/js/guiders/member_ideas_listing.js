    var workshopURL = document.getElementById("workshopTitle").href + "#guider=tour_close";    
    
    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the ideas listing page. Participating members can contribute ideas which address the goals of the workshop. All contributed ideas are voted up or down depending on how participating members rank their value.",
            id: "tour_0",
            next: "tour_1",
            title: "The Ideas Listing Page",
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
            description: "You need a Civinomics account, and need to be logged in to add a new idea.",
            id: "tour_2",
            prev: "tour_1",
            next: "tour_3",
            title: "Login To Add a New Idea",
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
            description: "This is the idea, which links to the idea comments page, the name of the author which links to their profile page and a link to the comments about this idea. ",
            id: "tour_3",
            prev: "tour_2",
            next: "tour_4",
            title: "Idea Listing",
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
            description: "This is the avatar of the author of the idea. Click it to display their profile page.",
            id: "tour_4",
            prev: "tour3",
            next: "tour_5",
            title: "Idea Author",
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
            description: "This is the current vote count for the idea. Participants can click on the up chevron to vote the idea up, or the down chevron to vote the idea down. The votes reflect participants ranking of how well the idea addresses the workshop goals.",
            id: "tour_5",
            prev: "tour4",
            next: "tour_5",
            title: "Idea Voting",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#vote_0",
            overlay: "true",
            xButton: true,
            position: 3
        });


    });
