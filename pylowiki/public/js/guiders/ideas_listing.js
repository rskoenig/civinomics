    var workshopURL = document.getElementById("workshopTitle").href + "#guider=tour_close";
    
    $(document).ready(function() {
        guiders.createGuider({
            attachTo: "#vote_0",
            buttons: [{name: "next"}],
            description: "Click on the up chevron to support things you like, or the down chevron on things you don't.",
            id: "tour_vote",
            next: "tour_addbutton",
            title: "Vote, on everything",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#vote_0",
            overlay: "true",
            xButton: true,
            position: 3
        });

        guiders.createGuider({
            attachTo: "#addButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "Contribute your idea to the collective wisdom in 120 characters or less.",
            id: "tour_addbutton",
            prev: "tour_vote",
            next: "tour_workshopname",
            title: "Have a great idea? Add it!",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true,
            position: 9
        });

        
        guiders.createGuider({
            attachTo: "#workshopTitle",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=workshopURL; }}],
            description: "Remember, you can click on the workshop name to return to the workshop main page.",
            id: "tour_workshopname",
            prev: "tour_addbutton",
            title: "Workshop Name takes you back",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopTitle",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        
    });
