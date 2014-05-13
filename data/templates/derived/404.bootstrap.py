# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398463804.1621771
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/404.bootstrap'
_template_uri = '/derived/404.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE HTML>\n<html lang="en-US">\n<head>\n\t<meta charset="UTF-8">\n\t<title>404: Page Not Found</title>\n\n\t<!-- styles -->\n\t<link type="text/css" rel="stylesheet" href="/styles/bootstrap/civinomics-workshops.css">\n    <link type="text/css" rel="stylesheet" href = "/styles/404.css" />\n</head>\n\n<body class="unfound">\n\t<div class="navbar navbar-fixed-top"> <!-- begin navbar -->\n\t\t<div class="navbar-inner">\n\t\t\t<div class="container">\n\t\t\t\t<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n\t\t\t\t\t<span class="icon-bar"></span>\n\t\t\t\t\t<span class="icon-bar"></span>\n\t\t\t\t\t<span class="icon-bar"></span>\n\t\t\t\t</a>\n\t\t\t\t<a href="/" class="brand">civinomics</a>\n\t\t\t\t<div class="nav-collapse"> <!-- hides when display is too small -->\n\t\t\t\t\t<ul class="nav pull-right nav-pills">\n\t\t\t\t\t\t<li><a href="/">Home</a></li>\n')
        # SOURCE LINE 25
        if 'user' in session:
            # SOURCE LINE 26
            __M_writer(u'\t\t\t\t\t\t\t<li><a href="/login/logout">Logout</a></li>\n\t\t\t\t\t\t\t<li class="dropdown">\n\t\t\t\t\t\t\t\t<ul class="dropdown-menu">\n')
            # SOURCE LINE 29
            if int(c.authuser['accessLevel']) >= 100:
                # SOURCE LINE 30
                __M_writer(u'\t\t\t\t\t\t\t\t\t\t<li><a href="/addWorkshop">Add Workshop</a></li>\n')
                pass
            # SOURCE LINE 32
            if int(c.authuser['accessLevel']) >= 200:
                # SOURCE LINE 33
                __M_writer(u'\t\t\t\t\t\t\t\t\t\t<li><a href="/systemAdmin">Sys Admin</a></li>\n')
                pass
            # SOURCE LINE 35
            __M_writer(u'\t\t\t\t\t\t\t\t\t<li><a href="/login/logout">Logout</a></li>\n\t\t\t\t\t\t\t\t</ul> <!-- /.dropdown-menu -->\n\t\t\t\t\t\t\t</li> <!-- /.dropdown -->\n')
            # SOURCE LINE 38
            if int(c.authuser['accessLevel']) >= 100:
                # SOURCE LINE 39
                __M_writer(u'    \t\t\t\t\t\t\t<li class="dropdown">\n    \t\t\t\t\t\t\t    <a href="#" class="dropdown-toggle" data-toggle="dropdown">\n    \t\t\t\t\t\t\t        Surveys\n    \t\t\t\t\t\t\t        <b class="caret"></b>\n    \t\t\t\t\t\t\t    </a>\n    \t\t\t\t\t\t\t    <ul class="dropdown-menu">\n')
                # SOURCE LINE 45
                if int(c.authuser['accessLevel']) >= 200:
                    # SOURCE LINE 46
                    __M_writer(u'    \t\t\t\t\t\t\t         <li><a href="/surveyAdmin">Survey admin</a></li>\n')
                    pass
                # SOURCE LINE 48
                __M_writer(u'    \t\t\t\t\t\t\t        <li><a href="/addSurvey">Add survey</a></li>\n    \t\t\t\t\t\t\t        <li><a href="/showSurveys">My surveys</a></li>\n    \t\t\t\t\t\t\t    </ul>\n    \t\t\t\t\t\t\t</li>\n')
                pass
            pass
        # SOURCE LINE 54
        __M_writer(u'\t\t\t\t\t</ul> <!-- /.nav -->\n\t\t\t\t</div> <!-- /.nav-collapse -->\n\t\t\t</div> <!-- /.container -->\n\t\t</div> <!-- /.navbar-inner -->\n\t</div> <!-- /.navbar -->\n\t<div class="container-fluid"> <!-- responsive container for everything -->\n\t\t\t<div class="row">\n\t\t\t\t<center>\n\t\t\t\t\t<table>\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<td class="unfound-title">ERR 404</td>\n\t\t\t\t\t\t</tr>\n\t\t\t\t\t</table>\n\t\t\t\t</center>\n\t\t\t</div>\n\n\t\t\t<div class="row">\n\t\t\t\t\t<div class="unfound-message">\n\t\t\t\t\t<center>\n\t\t\t\t\t\t<table>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>546865 206D61 676963 616C20 636F6D 707574 617469</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>6F6E20 676E6F 6D6573 206861 766520 666169 6C6564</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>212020 4D6179 626520 696620 796F75 206869 742072</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>656672 657368 206173 206661 737420 617320 796F75</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>206361 6E2065 766572 797468 696E67 207769 6C6C20</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t<td>776F72 6B2061 676169 6E3F3F 3F3F3F 3F3F3F 3F3F3F</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t</table>\n\t\t\t\t\t</center>\n\t\t\t\t\t<br />\n\t\t\t\t\t<br />\n\n\t\t\t\t\tYou have attempted to access a non-existent page.\n\t\t\t\t\tOops!\n\t\t\t\t\t</div>\n\t\t\t</div>\n\t\t<div class="row-fluid">\n\t\t\t<footer class="span12">\n\t\t\t\t<div class="row">\n\t\t\t\t\t<a href="/surveys">Surveys</a>\n\t\t\t\t</div> <!-- /.row -->\n\t\t\t\t<div class="row">\n\t\t\t\t\t<a href="/corp/about">About Us</a> |\n\t\t\t\t\t<a href="/corp/contact">Contact</a> |\n\t\t\t\t\t<a href="/corp/terms">Terms of Use</a> |\n\t\t\t\t\t<a href="/corp/privacy">Privacy</a>\n\t\t\t\t</div> <!-- /.row -->\n\t\t\t</footer>\n\t\t</div> <!-- /.row-fluid -->\n\t</div> <!-- /.container-fluid -->\n\n\t<!-- scripts go at the bottom so they don\'t keep the user waiting -->\n\t<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>\n\t<script type="text/javascript" src="/js/bootstrap/bootstrap.min.js"></script>\n</body>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


