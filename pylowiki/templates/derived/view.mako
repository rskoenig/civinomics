<%inherit file="/base/base.mako" />

##This allows certain controllers to return_to previous url
<%namespace file="/lib/mako_lib.mako" import="return_to" />

##This shows the comments on the page
<%namespace file="/derived/comments.mako" import="comments" />
${return_to()}

${c.content}

${comments()}
