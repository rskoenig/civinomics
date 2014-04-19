$('button.activateButton').click(function(e){
    e.preventDefault();
    $button = $(this);
    var urlList = $button.attr('data-URL-list').split(/_/);
    var urlString = '/activate/user/' + urlList[1];
    if($button.hasClass('notactivated')){
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
        
        $button.removeClass('notactivated');
        var bText = '<span>User Activated</span>';
        $button.html(bText);
    } 
});

$('button.resendActivateEmailButton').click(function(e){
    e.preventDefault();
    $button = $(this);
    var urlList = $button.attr('data-URL-list').split(/_/);
    var urlString = '/activateResend/' + urlList[1];
    var result = $.ajax({
        type : 'POST',
        async : false,
        url  : urlString
    });
    var message = "Registration email resent!" ;  
    document.getElementById('resendMessage').innerText = message;
});