$("#search-input").focus(function(){
    $(this).animate({ width: "250px"}, 200);
});

$("#search-input").blur(function(){
    $(this).animate({width: "150px"}, 200);
});