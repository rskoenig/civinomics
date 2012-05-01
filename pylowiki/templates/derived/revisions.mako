<%inherit file="/base/base.mako"/>

<%namespace file="/derived/events.mako" import="events" />

<h1> ${c.heading} </h1>

Revision count: ${c.count}

<br /><br />

${events()}

