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
            var bText = '<span><i class="icon-user med-green"></i><strong> Follow </span>';
        } else {
            var bText = '<span><i class="icon-bookmark med-green"></i><strong> Bookmark </strong></span>';            
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
            var bText = '<span><i class="icon-user icon-white"></i><strong> Following </strong></span>';
        } else {
            var bText = '<span><i class="icon-bookmark icon-white"></i><strong> Bookmarked </strong></span>';
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
