$(".search-icon").tooltip({placement:'bottom'});

$("#search-input").focus(function(){
    $(this).animate({ width: "275px"}, 200);
    $(".search-icon").css({display:"none"});
});

$("#search-input").blur(function(){
    $(this).animate({width: "150px"}, 200);
    $(".search-icon").css({display:"inline"});
});