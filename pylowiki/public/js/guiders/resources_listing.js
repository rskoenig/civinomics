    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "This is the information resources listing page. Participating members can add links to information resources on the Web which will help educate about the workshop topic.",
            id: "tour_resources",
            next: "tour_1",
            title: "The Information Resources Listing Page",
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

    });
