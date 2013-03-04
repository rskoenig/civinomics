// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	// the following is to make it work in the admin edit pages:
	previewParserPath:	'../../../../preview/restructuredtext/',
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [

		{name:'Heading 1', key:'1', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') } },
		{name:'Bold', key:'B', openWith:'**', closeWith:'**'},
		{name:'Italic', key:'I', openWith:'*', closeWith:'*'},

		{separator:'---------------' },

		{name:'Bulleted List', openWith:'* ' },
		{name:'Numeric List', openWith:'#. '},

		{separator:'---------------' },

		{name:'Code', openWith:'\n.. code-block:: [![Language:!:]!]\n\n    '},
		{name:'Picture', key:'P', replaceWith:'\n.. image:: [![Url:!:]!]\n  :alt: [![Alternative text]!]\n\n'},
		{name:'Link', key:'L', openWith:'`', closeWith:' <[![Url:!:http://]!]>`_', placeHolder:'Your text to link here...' },	
	]
}

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, char) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		for(i = 0; i < n; i++) {
			heading += char;
		}
		return '\n'+heading;
	}
}
