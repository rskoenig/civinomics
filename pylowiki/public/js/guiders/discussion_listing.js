    var workshopURL = document.getElementById("workshopTitle").href + "#guider=tour_10"; 

    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the conversations listing page. Participating members can start conversations related to the workshop topic to ask questions, provide feedback to the facilitator and listeners, or generally discuss topics related to the workshop.",
            id: "tour_0",
            next: "tour_1",
            title: "The Conversations Listing Page",
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
            title: "Login To Start a New Conversation",
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
            description: "This is the conversation topic which links to the conversation page, the name of the author which links to their profile page and a link to the comments about this conversation. ",
            id: "tour_3",
            prev: "tour_2",
            next: "tour_4",
            title: "Conversation Listing",
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
            description: "This is the avatar of the author of the conversation topic. Click it to display their profile page.",
            id: "tour_4",
            prev: "tour3",
            next: "tour_5",
            title: "Conversation Topic Author",
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
            description: "This is the current vote count for the conversation topic. Participants can click on the up chevron to vote the conversation up, or the down chevron to vote the conversation down. The votes reflect participants ranking of the value of the conversation.",
            id: "tour_5",
            prev: "tour4",
            next: "tour_5",
            title: "Conversation Voting",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#vote_0",
            overlay: "true",
            xButton: true,
            position: 3
        });

    });
