$(document).ready(function() {
    $(".survey_slider").jColorSlider();
    $(".survey_multiSlider").jColorSlider();
    $("#mcs5_container").mCustomScrollbar("horizontal",400,"easeOutCirc",0,"fixed","no","no",10);
    
    $(function()
    {
        $('.radioSubmit').click( function() 
        {
            $.ajax(
            {
                type: "POST",
                url: $(this).attr('href'),
                data: {'radioButton': $('form input[type=radio]:checked').val()},
                success: function(data) 
                {
                    //var data = $.parseJSON(data)
                    $('.message').empty().append(data);
                }
            })
            return false; // cancel link default action
        });
    });
    
    $(function()
    {
        $('.textareaSubmit').click( function() 
        {
            $.ajax(
            {
                type: "POST",
                url: $(this).attr('href'),
                data: {'feedback': $('#textarea').val()},
                success: function(data) 
                {
                    //var data = $.parseJSON(data)
                    $('.message').empty().append(data);
                }
            })
            return false; // cancel link default action
        });
    });
    
    $(function()
    {
        $('.itemRankingSubmit').click( function() 
        {
            $.ajax(
            {
                type: "POST",
                url: $(this).attr('href'),
                data: $("form").serialize(),
                success: function(data) 
                {
                    //var data = $.parseJSON(data)
                    $('.message').empty().append(data);
                }
            })
            return false; // cancel link default action
        });
    });
});