
$('a.flagButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#flag_0').empty().append(data.result);
});

$('a.flagCommentButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#flagged_' + data.code).empty().append(data.result);
});

$('.disableButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var formData = $(this).parents('form').serializeArray();
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString,
       data : formData
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#disableResponse-' + data.code).empty().append(data.result);
});

$('.enableButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var formData = $(this).parents('form').serializeArray();
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString,
       data : formData
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#enableResponse-' + data.code).empty().append(data.result);
});

$('.deleteButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var formData = $(this).parents('form').serializeArray();
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString,
       data: formData
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#deleteResponse-' + data.code).empty().append(data.result);
});

$('.immunifyButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var formData = $(this).parents('form').serializeArray();
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString,
       data : formData
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#immunifyResponse-' + data.code).empty().append(data.result);
});

$('.adoptButton').click(function(e){
    e.preventDefault();
    var urlString = $(this).attr('href');
    var formData = $(this).parents('form').serializeArray();
    var data = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString,
       data : formData
    }).responseText;
    var data = jQuery.parseJSON(data);
    $('#adoptResponse-' + data.code).empty().append(data.result);
});