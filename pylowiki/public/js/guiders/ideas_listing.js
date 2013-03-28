    var workshopURL = document.getElementById("workshopTitle").href + "#guider=tour_close";
    
    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the ideas page, where all the ideas for the workshop are listed.",
            id: "tour_ideas",
            next: "tour_workshopname",
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
            id: "tour_workshopname",
            next: "tour_addbutton",
            title: "Workshop Name",
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
            description: "Have a great idea which addresses the workshop goals? Add it!",
            id: "tour_addbutton",
            prev: "tour_workshopname",
            next: "tour_idea",
            title: "Add a New Idea",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true,
            position: 9
        });

        guiders.createGuider({
            attachTo: "#content_0",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "This is an idea. Click on the comments link to visit the idea comments page, or click on the name of the author to visit their profile page.",
            id: "tour_idea",
            prev: "tour_addbutton",
            next: "tour_vote",
            title: "Idea Listing",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#content_0",
            overlay: "true",
            xButton: true,
            position: 12
        });
        
        guiders.createGuider({
            attachTo: "#vote_0",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=workshopURL; }}],
            description: "This is the current vote count for the idea.<br>Click on the up chevron to vote the idea up, or the down chevron to vote the idea down.<p>Votes reflect participants' ranking of how well the idea addresses the workshop goals.",
            id: "tour_vote",
            prev: "tour_idea",
            title: "Idea Voting",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#vote_0",
            overlay: "true",
            xButton: true,
            position: 3
        });

    });
