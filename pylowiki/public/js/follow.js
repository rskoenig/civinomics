$('button.followButton').click(function(e){
    e.preventDefault();
    $button = $(this);
    var urlList = $button.attr('data-URL-list').split(/_/);
    var urlString = '/' + urlList[0] + '/' + urlList[1] + '/' + urlList[2] + '/follow/handler';
    if($button.hasClass('following')){
        //urlString = urlString + '/unfollow/';
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
        
        $button.removeClass('following');
        $button.removeClass('btn-civ');
        $button.removeClass('unfollow');
        if(urlList[0] == 'profile'){
            var bText = '<img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png"> <span> Follow </span>';
        } else {
            var bText = '<span><i class="icon-bookmark pull-left"></i> Bookmark </span>';            
        }
        $button.html(bText);
    } else {
        
        //urlString = urlString + '/follow/';
        $.ajax({
           type : 'POST',
           async : false,
           url  : urlString
        });
                   
        $button.addClass('following');
        $button.addClass('btn-civ');
        if(urlList[0] == 'profile'){
            var bText = '<img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png"> <span> Unfollow </span>';
        } else {
            var bText = '<span><i class="icon-bookmark icon-white pull-left"></i> Bookmarked </span>';
        }
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
