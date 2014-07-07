$(document).ready(function(){

    widcol = $('div#cols').width();
    wid1 = $('div.one').width();
    wid3 = $('div.three').width();
    wid2 = widcol-wid1-wid3-2
    
    $('div.two').width(wid2);
    
    ht3 = $('div.three').height();
    $('div.one,div.two').height(ht3);

});