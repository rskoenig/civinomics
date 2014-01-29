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
