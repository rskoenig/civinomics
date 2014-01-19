$(document).ready(function(){

    $('#fldtabs li').hover(
        function() {
            $(this).css({
                'background':'#fff',
                'color':'#030303'
            });
            $(this).find('a').css({
                'background':'#fff',
                'color':'#030303'
            });
        },
        function() {
            $(this).css({
                'background':'rgba(255,255,255,.3)',
                'color':'#aaa'
            });
            $(this).find('a').css({
                'background':'none',
                'color':'#aaa'
            });
        });

});
