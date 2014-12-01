$(document).ready(function() { 
	var options = { 
	    target:   '#output',   // target element(s) to be updated with server response 
	    beforeSubmit:  beforeSubmit,  // pre-submit callback 
	    uploadProgress: OnProgress, //upload progress callback 
	    resetForm: true        // reset the form after successful submit 
	}; 
	        
	 $('input:file').change(function() {
	 	$("#file_accepted").show();
	 	var filename = $('input[type=file]').val().replace(/C:\\fakepath\\/i, '');
	 	$( "#file_accepted" ).prepend( "<p> Your selected file is: "+filename+"</p>" );
	 	
	}); 
	
	$("#submit_button").click(
		function(){
			$("#status_txt").show();
		    $(this).ajaxSubmit(options);            
		    return false; 
		}				
	);
	
	$("#cancel_button").click(
		function(){
			$("#file_accepted").hide();
		}
	);
	});
	
	function beforeSubmit(){
//check whether client browser fully supports all File API
if (window.File && window.FileReader && window.FileList && window.Blob)
{
   var fsize = $('#FileInput')[0].files[0].size; //get file size
       var ftype = $('#FileInput')[0].files[0].type; // get file type
    //allow file types 
  switch(ftype)
       {
        case 'application/csv':
        break;
        default:
         $("#output").html("<b>"+ftype+"</b> Unsupported file type!");
     return false
       }

   //Allowed file size is less than 5 MB (1048576 = 1 mb)
   if(fsize>5242880) 
   {
     alert("<b>"+fsize +"</b> Too big file! <br />File is too big, it should be less than 5 MB.");
     return false
   }
    }
    else
{
   //Error for older unsupported browsers that doesn't support HTML5 File API
   alert("Please upgrade your browser, because your current browser lacks some new features we need!");
       return false
}
}
function OnProgress(event, position, total, percentComplete)
{
//Progress bar
$('#progressbox').show();
$('#progressbar').width(percentComplete + '%') //update progressbar percent complete
$('#statustxt').html(percentComplete + '%'); //update status text
if(percentComplete>50)
    {
        $('#statustxt').css('color','#000'); //change status text to white after 50%
    }
}

var app = angular.module('myApp', ['ngGrid']);
	app.controller('MyCtrl', function($scope) {
	    $scope.myData = [{name: "Moroni", age: 50},
	                     {name: "Tiancum", age: 43},
	                     {name: "Jacob", age: 27},
	                     {name: "Nephi", age: 29},
	                     {name: "Enos", age: 34}];
	    $scope.gridOptions = { 
	        data: 'myData',
	        columnDefs: [{field:'name', displayName:'Name'}, {field:'age', displayName:'Age'}]
	    };
});
