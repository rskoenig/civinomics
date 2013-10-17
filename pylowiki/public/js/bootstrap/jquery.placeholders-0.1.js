(function( $ ) {

  $.fn.placeholders = function(bAddClass) {
	
	var inputElem = document.createElement('input');
	var textAreaElem = document.createElement('textarea');

	function testProps(props,el) {
		var attrs = {};
		for ( var i = 0, len = props.length; i < len; i++ ) {
			attrs[ props[i] ] = !!(props[i] in el);
		}
		return attrs;
	};
	
	var rProps = ['placeholder'];
	var Tester = { 
				   input:testProps(rProps,inputElem)
				  ,textarea:testProps(rProps,textAreaElem)
				 };
	
	if(!Tester.input.placeholder || !Tester.textarea.placeholder){
		var selector = [];
		if(!Tester.input.placeholder) selector.push("input[type='text']","input[type='password']","input[type='search']");
		if(!Tester.textarea.placeholder) selector.push("textarea");
		selector = selector.join(',');
		var textInputs = this.find(selector);
		for(var i=0,len=textInputs.length; i<len; i++)
		{
			var jInput = $(textInputs[i]);
			var attrVal = jInput.attr("placeholder");
			if(typeof attrVal !== 'undefined' && attrVal !== false)
			{
				var nameAttr = jInput.attr("name");
				var tag = textInputs[i].nodeName.toLowerCase();
				var textDelegate;
				if(tag == "input"){
					textDelegate = $("<input type='text' for='"+nameAttr+"'>");
				}else{
					textDelegate = $("<textarea for='"+nameAttr+"'>");
				}
				textDelegate.addClass("hasPlaceHolder").val(attrVal);
				jInput.hide();
				jInput.after(textDelegate);
			}
		}

		this.on("focus",selector,function(e){
			var jInput = $(e.currentTarget);
			if(jInput.hasClass("hasPlaceHolder"))
			{
				var tag = e.currentTarget.nodeName.toLowerCase();
				var inputName = jInput.attr("for");
				jInput.hide();
				var actual = jInput.siblings(tag+"[name="+inputName+"]");
				actual.show(0,function(){
					setTimeout(function(){actual.focus();},10);
				});
				
			}
		});
		this.on("blur",selector,function(e){
			var jInput = $(e.currentTarget);
			var currentVal = jInput.val();
			if(!jInput.hasClass("hasPlaceHolder") && currentVal == "")
			{
				var tag = e.currentTarget.nodeName.toLowerCase();
				var inputName = jInput.attr("name");
				jInput.hide();
				jInput.siblings(tag+"[for="+inputName+"]").show();
			}
		});
	}else{
		if(bAddClass){
			var jTextInputs = this.find("input[placeholder],textarea[placeholder]");
			
			function addPlaceholderClass(){
				var jInput = $(this);
				var currentVal = jInput.val();
				if(currentVal == ""){
					jInput.addClass("hasPlaceHolder")
				}
			};
			
			jTextInputs.each(addPlaceholderClass);
			jTextInputs.focus(function(){
				$(this).removeClass("hasPlaceHolder");
			});
			jTextInputs.blur(addPlaceholderClass);
		}
	}
	return this;
  };
})( jQuery );