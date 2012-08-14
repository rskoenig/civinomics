
$('button.followButton').live('click', function(e){
    e.preventDefault();
    $button = $(this);
    var urlList = $button.attr('rel').split(/_/);
    var urlString = '/' + urlList[0] + '/' + urlList[1] + '/' + urlList[2];
    if($button.hasClass('following')){
        urlString = urlString + '/unfollow/';
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
        
        $button.removeClass('following');
        $button.removeClass('unfollow');
        var bText = '+Follow';
        $button.text(bText);
    } else {
        
        urlString = urlString + '/follow/';
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
                   
        $button.addClass('following');
        $button.text('-Unfollow');
    }
});

$('button.followButton').hover(function(){
     $button = $(this);
    if($button.hasClass('following')){
        $button.removeClass('unfollow');
        $button.addClass('unfollow');
        $button.text('-Unfollow');
    }
}, function(){
    if($button.hasClass('following')){
        $button.removeClass('unfollow');
        $button.text('+Following');
    }
});
