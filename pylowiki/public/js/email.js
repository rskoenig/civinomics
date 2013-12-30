$(document).ready(function(){
	$(".generatedemail").each(function(i){
		var start = $(this).data("start");
		var end = $(this).data("end");
		if (!start || !end) { //shame on you
			$(this).text("EMAIL LINK IMPROPERLY FORMATTED");
			return;
		}
		var mailto = start + end;
		$(this).text(mailto);
		var subject = $(this).data("subject");
		if (subject) mailto += "?subject=" + subject;
		$(this).attr("href", "mailto:" + mailto);
	});
});