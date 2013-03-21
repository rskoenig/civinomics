      
    var workshopURL = document.getElementById("workshopTitle").href;
    var resourcesURL = workshopURL + '/resources#guider=tour_0';
    var discussionsURL = workshopURL + '/discussions#guider=tour_0';
    var ideasURL = workshopURL + '/ideas#guider=tour_0';  
    
    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "Welcome to the Civinomics tour!  You may press escape on your keyboard or click the 'x' in the upper left hand corner of this box to exit the tutorial at any time. ",
            id: "tour_welcome",
            next: "tour_1",
            title: "Welcome!",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true,
        });

        guiders.createGuider({
            attachTo: "#civinomicsLogo",
            buttons: [{name: "next"}],
            description: "Click on the Civinomics logo if you want to go to the Civinomics main page where all workshops are listed. ",
            id: "tour_1",
            next: "tour_2",
            title: "Civinomics home.",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#civinomicsLogo",
            overlay: "true",
            xButton: true,
            position: 3
        });
        
        guiders.createGuider({
            attachTo: "#workshopTitle",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "This is the name of the workshop. You can click it to return to the workshop main page.",
            id: "tour_2",
            prev: "tour_1",
            next: "tour_3",
            title: "Workshop Name.",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopTitle",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        guiders.createGuider({
            attachTo: "#workshopGoals",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "Here is where the workshop's facilitator has outlined the goals for this workshop.",
            id: "tour_3",
            prev: "tour_2",
            next: "tour_4",
            title: "Workshop Goals",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopGoals",
            overlay: "true",
            xButton: true,
            position: 9
        });
                
        guiders.createGuider({
            attachTo: "#workshopNotables",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "Notables are the Facilitators and Listeners monitoring the workshop. Facilitators here are charged with keeping the peace and facilitating the workshop process.  Listeners have signed onto this workshop to get your feedback!",
            id: "tour_4",
            prev: "tour_3",
            next: "tour_5",
            title: "Notables",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopNotables",
            overlay: "true",
            xButton: true,
            position: 9
        });
        
        guiders.createGuider({
            attachTo: "#workshopActivity",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "The activity stream shows the most recent contributions made to the workshop, with links to the author profile and the item which was added. ",
            id: "tour_5",
            prev: "tour_4",
            next: "tour_6",
            title: "Activity",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopActivity",
            overlay: "true",
            xButton: true,
            position: 9
        });
        
        guiders.createGuider({
            attachTo: "#workshopSlideshow",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "The slideshow is an educational introduction to the workshop topic. When visiting a workshop for the first time, be sure to go through the slideshow.",
            id: "tour_6",
            prev: "tour_5",
            next: "tour_7",
            title: "Slideshow",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopSlideshow",
            overlay: "true",
            xButton: true,
            position: 3
        });
        
        
        guiders.createGuider({
            attachTo: "#workshopInformation",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "Along with the slideshow, this section provides background information about the topic of the workshop.",
            id: "tour_7",
            prev: "tour_6",
            next: "tour_8",
            title: "Background",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopInformation",
            overlay: "true",
            xButton: true,
            position: 12
        });
        
                
        guiders.createGuider({
            attachTo: "#resourceButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=resourcesURL; }}],
            description: "The Learn section of the workshop is where links to information resources relevant to the workshop and the workshop goals are added by members and the facilitators.",
            id: "tour_8",
            prev: "tour_7",
            next: "tour_9",
            title: "Learn",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#resourceButton",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        guiders.createGuider({
            attachTo: "#discussionButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=discussionsURL;}}],
            description: "The Talk section of the workshop is for questions and answers, longer discussions/debates, and general feedback to the workshop facilitators and listeners.",
            id: "tour_9",
            prev: "tour_8",
            next: "tour_10",
            title: "Talk",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#discussionButton",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        guiders.createGuider({
            attachTo: "#ideaButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next", onclick: function() { window.location.href=ideasURL;}}],
            description: "Vote on existing ideas or add new ideas. Ideas are short and should directly address the workshop's goals.",
            id: "tour_10",
            prev: "tour_9",
            next: "tour_11",
            title: "Vote",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#ideaButton",
            overlay: "true",
            xButton: true,
            position: 6
        });
                
        guiders.createGuider({
            attachTo: "#workshopBookmark",
            buttons: [{name:"prev", onclick: guiders.prev}, {name:"close", onclick: guiders.hideAll}],
            description: "Bookmark the workshop to add a link to it in the 'My Workshop' tab in your profile. This makes it easy to find when you want to visit the workshop again to catch up.",
            id: "tour_11",
            prev: "tour_10",
            title: "Bookmark",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopBookmark",
            overlay: "true",
            xButton: true,
            position: 6
        });
                
        guiders.createGuider({
            buttons: [{name:"close"}],
            description: "Now that you've taken the tour, go start or find workshops that fit your interests and work with other people to make something better.",
            id: "tour_close",
            title: "Make Things Better",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true,
            position: 6
        }); 
    });
