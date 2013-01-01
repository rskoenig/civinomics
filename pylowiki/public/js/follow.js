
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
        var bText = '<img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png"> <span> Follow </span>';
        $button.html(bText);
    } else {
        
        urlString = urlString + '/follow/';
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
                   
        $button.addClass('following');
        var bText = '<img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png"> <span> Unfollow </span>';
        $button.html(bText);
    }
});

$('button.followButtonFoo').hover(function(){
     $button = $(this);
    if($button.hasClass('following')){
        $button.removeClass('unfollow');
        $button.addClass('unfollow');
        $button.text('Unfollow');
    }
}, function(){
    if($button.hasClass('following')){
        $button.removeClass('unfollow');
        $button.text('Following');
    }
});
