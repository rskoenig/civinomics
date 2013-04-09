$(document).ready(function()
{
    $('.unread-message').click(function(event){
        event.preventDefault();
        var code = $(this).attr('data-code');
        var thisMessage = $(this);
        $.post('/message/' + code + '/mark/read', 
            function(response)
            {
                if (response == "OK"){
                    thisMessage.attr('class', '');
                }
                else{
                    thisMessage.attr('clas', 'unread-message error');
                }
            }
        );
    });
});