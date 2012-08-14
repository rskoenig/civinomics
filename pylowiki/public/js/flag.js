
$('a.flagButton').live('click', function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#flag_response').empty().append(data.result);
});
