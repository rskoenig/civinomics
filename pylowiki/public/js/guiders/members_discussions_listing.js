    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the conversations listing page. Participating members can start conversations related to the workshop topic to ask questions, provide feedback to the facilitator and listeners, or generally discuss topics related to the workshop.",
            id: "tour_discussions",
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
            title: "Login To Start a New Cnversation",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#addButton",
            overlay: "true",
            xButton: true,
            position: 9
        });

    });
