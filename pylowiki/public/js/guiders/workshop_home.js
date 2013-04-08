    
    var workshopURL = document.getElementById("workshopTitle").href;
    var ideasURL = workshopURL + '/ideas#guider=tour_ideas';
    $(document).ready(function() {
        guiders.createGuider({
            buttons: [{name: "next"}],
            description: "Welcome to the Civinomics tour!<br>You may press escape on your keyboard or click the 'x' in the upper left hand corner of this box to exit the tutorial at any time. ",
            id: "tour_welcome",
            next: "tour_logo",
            title: "Welcome!",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true
        });

        guiders.createGuider({
            attachTo: "#civinomicsLogo",
            buttons: [{name: "next"}],
            description: "<br><h1 class=guiders_title>Civinomics home</h1></p><p>Click on the Civinomics logo if you want to go back to the Civinomics main page where all workshops are listed.</p> ",
            id: "tour_logo",
            next: "tour_name",
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
            description: "This is the name of the workshop. You can click it to return to the workshop main page from any of the other workshop pages.",
            id: "tour_name",
            prev: "tour_logo",
            next: "tour_goals",
            title: "Workshop Name",
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
            id: "tour_goals",
            prev: "tour_name",
            next: "tour_notables",
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
            description: "Notables are the Facilitators and Listeners monitoring the workshop.<br><p>Facilitators here are charged with keeping the peace and facilitating the workshop process.<p>Listeners have signed onto this workshop to get your feedback!",
            id: "tour_notables",
            prev: "tour_goals",
            next: "tour_info",
            title: "Notables",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopNotables",
            overlay: "true",
            xButton: true,
            position: 9
        });
        
        guiders.createGuider({
            attachTo: "#workshopInformation",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "Along with the slideshow, this section provides background information about the topic of the workshop.",
            id: "tour_info",
            prev: "tour_notables",
            next: "tour_slideshow",
            title: "Background",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopInformation",
            overlay: "true",
            xButton: true,
            position: 12
        });
        
        
      
        guiders.createGuider({
            attachTo: "#workshopSlideshow",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "The slideshow is an educational introduction to the workshop topic. When visiting a workshop for the first time, be sure to go through the slideshow.",
            id: "tour_slideshow",
            prev: "tour_info",
            next: "tour_learn",
            title: "Slideshow",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#workshopSlideshow",
            overlay: "true",
            xButton: true,
            position: 3
        });
        
        
        guiders.createGuider({
            attachTo: "#resourceButton",
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "The Learn section of the workshop is where links to information resources relevant to the workshop and the workshop goals are added by members and the facilitators.",
            id: "tour_learn",
            prev: "tour_slideshow",
            next: "tour_talk",
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
            buttons: [{name:"prev", onclick: guiders.prev}, {name: "next"}],
            description: "The Talk section of the workshop is for questions and answers, longer discussions/debates, and general feedback to the workshop facilitators and listeners.",
            id: "tour_talk",
            prev: "tour_learn",
            next: "tour_vote",
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
            id: "tour_vote",
            prev: "tour_talk",
            title: "Vote",
            closeOnEscape: true,
            autoFocus: true,
            highlight: "#ideaButton",
            overlay: "true",
            xButton: true,
            position: 6
        });
        
        guiders.createGuider({
            buttons: [{name:"close"}],
            description: "Now that you've taken the tour, go start or find workshops that fit your interests and work with other people make something better.",
            id: "tour_close",
            title: "Make Things Better",
            closeOnEscape: true,
            autoFocus: true,
            overlay: "true",
            xButton: true,
            position: 6
        });
        
    });