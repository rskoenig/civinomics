$(document).ready(function(){
	$(".generatedemail").click(function(){
		var start = $(this).data("start");
		var end = $(this).data("end");
		if (!start || !end) //shame on you
			return;
		var mailto = "mailto:" + start + end;
		var subject = $(this).data("subject");
		if (subject) mailto += "?subject=" + subject;
		window.location.href = mailto;
	});
});