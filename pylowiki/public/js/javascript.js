//Ajax wiki and comment previewer
// previewTimer must live outside the functions.
var previewTimer = null;

function previewAjax( textarea, div ){
    if ( previewTimer ) {
        clearTimeout( previewTimer );
    }
    previewTimer = setTimeout( function() {
        sendPreview( textarea, div );
    }, 300 );
}

function sendPreview( textarea, div ){
    $.ajaxSetup ({
        cache: false
    });

    var url    = '/wiki/previewer/ajax';
    var params = { 'data' : $( '#' + textarea ).val() };

    $( '#' + div ).load( url, params );
}

function toggle( textarea, button, origtext ){
    if ( !$('#' + textarea + ":visible").size() ){
        $('#' + textarea).slideDown( "slow" );
        $('#' + button).text( "hide" );
    }
    else {
        $('#' + textarea).slideUp( "slow" );
        $('#' + button).text( origtext );
    }
}
