# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398538074.5013199
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/admin_helpers/workshop.mako'
_template_uri = u'/lib/admin_helpers/workshop.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['flaggedItems', 'admin_info', 'admin', 'admin_facilitators', 'admin_event_log', 'marked_items', 'admin_listeners']


# SOURCE LINE 1

import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.idea             as ideaLib
import pylowiki.lib.db.comment          as commentLib
import pylowiki.lib.db.flag             as flagLib
import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.workshop         as workshopLib
import simplejson as json


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 11
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'  \n')
        # SOURCE LINE 11
        __M_writer(u'\n\n')
        # SOURCE LINE 35
        __M_writer(u'\n\n')
        # SOURCE LINE 54
        __M_writer(u'\n\n')
        # SOURCE LINE 152
        __M_writer(u'\n\n')
        # SOURCE LINE 209
        __M_writer(u'\n\n')
        # SOURCE LINE 278
        __M_writer(u'\n\n')
        # SOURCE LINE 288
        __M_writer(u'\n\n')
        # SOURCE LINE 366
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_flaggedItems(context,items):
    context.caller_stack._push_frame()
    try:
        active = context.get('active', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 290
        __M_writer(u'\n    ')
        # SOURCE LINE 291

        thisClass = 'tab-pane'
        if active == True:
            thisClass += ' active'
        objectMapping = {'comment': 'Comment', 'discussion':'Conversation', 'idea':'Idea', 'resource':'Resource'}
            
        
        # SOURCE LINE 296
        __M_writer(u'\n    <div class="')
        # SOURCE LINE 297
        __M_writer(escape(thisClass))
        __M_writer(u'">\n')
        # SOURCE LINE 298
        if not items:
            # SOURCE LINE 299
            __M_writer(u'            <p class="centered">There doesn\'t appear to be anything here.  Hooray!</p>\n')
            # SOURCE LINE 300
        elif len(items) == 0:
            # SOURCE LINE 301
            __M_writer(u'            <p class="centered">There doesn\'t appear to be anything here.  Hooray!</p>\n')
            # SOURCE LINE 302
        else:
            # SOURCE LINE 303
            __M_writer(u'            <table class="table table-bordered table-hover table-condensed">\n                <thead>\n                    <tr>\n                        <th>Flags</th>\n                        <th>Author</th>\n                        <th>Item</th>\n                        <th>Content</th>\n                        <th>Action</th> \n                    </tr>\n                </thead>\n                <tbody>\n')
            # SOURCE LINE 314
            for item in items:
                # SOURCE LINE 315
                __M_writer(u'                        ')

                rowClass = ''
                if item['deleted'] == '1' and not c.privs['admin']:
                    continue
                elif item['deleted'] == '1' and c.privs['admin']:
                    rowClass = 'error'
                    action = 'deleted'
                elif item['disabled'] == '1':
                    rowClass = 'warning'
                    action = 'disabled'
                else:
                    action = 'enabled'
                event = eventLib.getEventForThingWithAction(item, action)
                if action == 'enabled' and event:
                    rowClass = 'success'
                                        
                
                # SOURCE LINE 330
                __M_writer(u'\n                        <tr class="')
                # SOURCE LINE 331
                __M_writer(escape(rowClass))
                __M_writer(u'">\n                            <td> ')
                # SOURCE LINE 332
                __M_writer(escape(flagLib.getNumFlags(item)))
                __M_writer(u' </td>\n                            <td>\n                                ')
                # SOURCE LINE 334
 
                owner = userLib.getUserByID(item.owner)
                lib_6.userImage(owner, className = 'avatar small-avatar')
                lib_6.userLink(owner)
                                                
                
                # SOURCE LINE 338
                __M_writer(u'\n                            </td>\n                            <td> ')
                # SOURCE LINE 340
                __M_writer(escape(objectMapping[item.objType]))
                __M_writer(u' </td>\n                            <td>\n')
                # SOURCE LINE 342
                if item.objType != 'comment':
                    # SOURCE LINE 343
                    __M_writer(u'                                    <a ')
                    __M_writer(escape(lib_6.thingLinkRouter(item, c.w)))
                    __M_writer(u' class="expandable">')
                    __M_writer(escape(item['title']))
                    __M_writer(u'</a>\n')
                    # SOURCE LINE 344
                else:
                    # SOURCE LINE 345
                    __M_writer(u'                                    <a ')
                    __M_writer(escape(lib_6.thingLinkRouter(item, c.w, id='accordion-%s'%item['urlCode'])))
                    __M_writer(u' class="expandable">')
                    __M_writer(escape(item['data']))
                    __M_writer(u'</a>\n')
                    pass
                # SOURCE LINE 347
                __M_writer(u'                            </td>\n                            <td>\n')
                # SOURCE LINE 349
                if event:
                    # SOURCE LINE 350
                    __M_writer(u'                                    <p>\n                                    ')
                    # SOURCE LINE 351

                    owner = userLib.getUserByID(event.owner)
                    lib_6.userImage(owner, className = 'avatar small-avatar')
                    lib_6.userLink(owner)
                                                        
                    
                    # SOURCE LINE 355
                    __M_writer(u'\n                                    : ')
                    # SOURCE LINE 356
                    __M_writer(escape(event['reason']))
                    __M_writer(u'\n                                    </p>\n')
                    pass
                # SOURCE LINE 359
                __M_writer(u'                            </td>\n                        </tr>\n')
                pass
            # SOURCE LINE 362
            __M_writer(u'                </tbody>\n            </table>\n')
            pass
        # SOURCE LINE 365
        __M_writer(u'    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_admin_info(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        pending = context.get('pending', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 211
        __M_writer(u'\n    ')
        # SOURCE LINE 212
        wEvents = eventLib.getParentEvents(c.w) 
        
        __M_writer(u'\n    <table class="table table-bordered">\n    <thead>\n    <tr><th>Workshop Events</th></tr>\n    </thead>\n    <tbody>\n')
        # SOURCE LINE 218
        if wEvents:
            # SOURCE LINE 219
            __M_writer(u'        <br /><br />\n')
            # SOURCE LINE 220
            for wE in wEvents:
                # SOURCE LINE 221
                __M_writer(u'            <tr><td><strong>')
                __M_writer(escape(wE.date))
                __M_writer(u' ')
                __M_writer(escape(wE['title']))
                __M_writer(u'</strong> ')
                __M_writer(escape(wE['data']))
                __M_writer(u'</td></tr>\n')
                pass
            pass
        # SOURCE LINE 224
        __M_writer(u'    </tbody>\n    </table>\n    <br /><br />\n    <br /><br />\n    <table class="table table-bordered">\n    <thead>\n    <tr><th>Current Facilitators</th></tr>\n    </thead>\n    <tbody>\n')
        # SOURCE LINE 233
        for f in c.f:
            # SOURCE LINE 234
            __M_writer(u'        ')
 
            fUser = userLib.getUserByID(f.owner)
            fEvents = eventLib.getParentEvents(f)
            fPending = "" 
                    
            if pending in f and f['pending'] == '1':
                fPending = "(Pending)"
                    
            
            # SOURCE LINE 241
            __M_writer(u'\n        <tr><td><a href="/profile/')
            # SOURCE LINE 242
            __M_writer(escape(fUser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(fUser['url']))
            __M_writer(u'">')
            __M_writer(escape(fUser['name']))
            __M_writer(u'</a> ')
            __M_writer(escape(fPending))
            __M_writer(u'<br />\n')
            # SOURCE LINE 243
            if fEvents:
                # SOURCE LINE 244
                for fE in fEvents:
                    # SOURCE LINE 245
                    __M_writer(u'          &nbsp; &nbsp; &nbsp; <strong>')
                    __M_writer(escape(fE.date))
                    __M_writer(u' ')
                    __M_writer(escape(fE['title']))
                    __M_writer(u'</strong>  ')
                    __M_writer(escape(fE['data']))
                    __M_writer(u'<br />\n')
                    pass
                pass
            # SOURCE LINE 248
            if c.authuser.id == f.owner and c.authuser.id != c.w.owner:
                # SOURCE LINE 249
                __M_writer(u'           <form id="resignFacilitator" name="resignFacilitator" action="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/resignFacilitator" method="post">\n               &nbsp; &nbsp; &nbsp;Note: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;\n               <button type="submit" class="gold" value="Resign">Resign</button>\n           <br />\n           </form>\n')
                pass
            # SOURCE LINE 255
            __M_writer(u'        </td></tr>\n')
            pass
        # SOURCE LINE 257
        __M_writer(u'    </tbody>\n    </table>\n    <table class="table table-bordered">\n    <thead>\n    <tr><th>Disabled Facilitators</th></tr>\n    </thead>\n    <tbody>\n')
        # SOURCE LINE 264
        for f in c.df:
            # SOURCE LINE 265
            __M_writer(u'       ')
            fUser = userLib.getUserByID(f.owner) 
            
            __M_writer(u'\n       ')
            # SOURCE LINE 266
            fEvents = eventLib.getParentEvents(f) 
            
            __M_writer(u'\n       <tr><td><a href="/profile/')
            # SOURCE LINE 267
            __M_writer(escape(fUser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(fUser['url']))
            __M_writer(u'">')
            __M_writer(escape(fUser['name']))
            __M_writer(u'</a> (Disabled)<br />\n')
            # SOURCE LINE 268
            if fEvents:
                # SOURCE LINE 269
                for fE in fEvents:
                    # SOURCE LINE 270
                    __M_writer(u'          &nbsp; &nbsp; &nbsp; <strong>')
                    __M_writer(escape(fE.date))
                    __M_writer(u' ')
                    __M_writer(escape(fE['title']))
                    __M_writer(u'</strong>  ')
                    __M_writer(escape(fE['data']))
                    __M_writer(u'<br />\n')
                    pass
                pass
            # SOURCE LINE 273
            __M_writer(u'       </tr></td>\n')
            pass
        # SOURCE LINE 275
        __M_writer(u'    </tbody>\n    </table>\n    <br /><br />\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_admin(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 37
        __M_writer(u'\n    <div class="row-fluid" ng-controller="adminController">\n        <div class="section-wrapper">\n            <div class="browse">\n                <h4 class="section-header smaller">Civ Admin Panel</h4>\n                <form class="form-horizontal" ng-init="code=\'')
        # SOURCE LINE 42
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'\'">\n                    <div class="control-group">\n                        <label class="control-label" for="setDemo">Set as demo?</label>\n                        <div class="controls">\n                            <a id="setDemo" class="btn btn-primary" ng-click="setDemo()" href="#">Do it</a>\n                            <span class="help-block" ng-show="showResponse">{{response}}</span>\n                        </div>\n                    </div>\n                </form>\n            </div><!-- browse -->\n        </div><!-- section-wrapper -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_admin_facilitators(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        len = context.get('len', UNDEFINED)
        pending = context.get('pending', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 56
        __M_writer(u'\n    <p>To invite a member to be a listener of, or co-facilitate this workshop, visit their Civinomics profile page and look for the "Invite ..." button!</p>\n    <table class="table table-bordered table-condensed" ng-controller="facilitatorController">\n        <thead>\n            <tr>\n                <th>Facilitators</th>\n                <th>Email on new items</th>\n                <th>Email on flagging</th>\n            </tr>\n        </thead>\n        <tbody>\n        ')
        # SOURCE LINE 67
 
        activeFacilitators = 0
        for f in c.f:
            if f['disabled'] == '0' and f['pending'] == '0':
                activeFacilitators += 1
                
        
        # SOURCE LINE 72
        __M_writer(u'\n')
        # SOURCE LINE 73
        for f in c.f:
            # SOURCE LINE 74
            __M_writer(u'            ')

            fUser = userLib.getUserByID(f.owner)
            fEvents = eventLib.getParentEvents(f)
            fPending = ""
            if pending in f and f['pending'] == '1':
                fPending = "(Pending)"
                        
            
            # SOURCE LINE 80
            __M_writer(u'\n            <tr>\n                <td>\n                    ')
            # SOURCE LINE 83

            lib_6.userImage(fUser, className = 'avatar small-avatar')
            lib_6.userLink(fUser)
                                
            
            # SOURCE LINE 86
            __M_writer(u'\n                    ')
            # SOURCE LINE 87
            __M_writer(escape(fPending))
            __M_writer(u'\n                </td>\n')
            # SOURCE LINE 89
            if (f['pending'] != '1' and fUser.id == c.authuser.id) or c.privs['admin']:
                # SOURCE LINE 90
                __M_writer(u'                    ')

                itemsChecked = ''
                flagsChecked = ''
                if 'itemAlerts' in f and f['itemAlerts'] == '1':
                    itemsChecked = 'checked'
                if 'flagAlerts' in f and f['flagAlerts'] == '1':
                    flagsChecked = 'checked'
                                    
                
                # SOURCE LINE 97
                __M_writer(u'\n                    <td>\n                        <form ng-init="code=\'')
                # SOURCE LINE 99
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u"'; url='")
                __M_writer(escape(c.w['url']))
                __M_writer(u"'; user='")
                __M_writer(escape(fUser['urlCode']))
                __M_writer(u'\'" class="no-bottom">\n                            <input type="checkbox" name="flagAlerts" value="flags" ng-click="emailOnAdded()" ')
                # SOURCE LINE 100
                __M_writer(escape(itemsChecked))
                __M_writer(u'>\n                            <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>\n                        </form>\n                    </td>\n                    <td>\n                        <form ng-init="code=\'')
                # SOURCE LINE 105
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u"'; url='")
                __M_writer(escape(c.w['url']))
                __M_writer(u"'; user='")
                __M_writer(escape(fUser['urlCode']))
                __M_writer(u'\'" class="no-bottom">\n                            <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnFlagged()" ')
                # SOURCE LINE 106
                __M_writer(escape(flagsChecked))
                __M_writer(u'>\n                            <span ng-show="emailOnFlaggedShow">{{emailOnFlaggedResponse}}</span>\n                        </form>\n                    </td>\n')
                # SOURCE LINE 110
            else:
                # SOURCE LINE 111
                __M_writer(u'                    <td>')
                __M_writer(escape(fPending))
                __M_writer(u'</td>\n                    <td>')
                # SOURCE LINE 112
                __M_writer(escape(fPending))
                __M_writer(u'</td>\n')
                pass
            # SOURCE LINE 114
            if activeFacilitators > 1 and fUser.id == c.authuser.id:
                # SOURCE LINE 115
                __M_writer(u'                    </tr><tr><td colspan=3>\n                    <form class="form-inline" id="resignFacilitator" name="resignFacilitator" action="/workshop/')
                # SOURCE LINE 116
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/facilitate/resign/handler/" method="post">\n                        Resign as facilitator? &nbsp;&nbsp;Reason: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;\n                        <button type="submit" class="btn btn-warning" value="Resign">Resign</button>\n                        <br />\n                    </form>\n                    </td>\n')
                pass
            # SOURCE LINE 123
            __M_writer(u'            </tr>\n')
            pass
        # SOURCE LINE 125
        __M_writer(u'        </tbody>\n    </table>\n')
        # SOURCE LINE 127
        if len(c.df) > 0:
            # SOURCE LINE 128
            __M_writer(u'        <table class="table table-bordered">\n        <thead>\n        <tr><th>Disabled Facilitators</th></tr>\n        </thead>\n        <tbody>\n')
            # SOURCE LINE 133
            for f in c.df:
                # SOURCE LINE 134
                __M_writer(u'            <tr><td>\n            ')
                # SOURCE LINE 135
 
                fUser = userLib.getUserByID(f.owner)
                fEvents = eventLib.getParentEvents(f) 
                lib_6.userImage(fUser, className = 'avatar small-avatar')
                lib_6.userLink(fUser)
                            
                
                # SOURCE LINE 140
                __M_writer(u'\n            <br />\n')
                # SOURCE LINE 142
                if fEvents:
                    # SOURCE LINE 143
                    for fE in fEvents:
                        # SOURCE LINE 144
                        __M_writer(u'                    <strong>')
                        __M_writer(escape(fE.date))
                        __M_writer(u' ')
                        __M_writer(escape(fE['title']))
                        __M_writer(u'</strong>  ')
                        __M_writer(escape(fE['data']))
                        __M_writer(u'<br />\n')
                        pass
                    pass
                # SOURCE LINE 147
                __M_writer(u'            </tr></td>\n')
                pass
            # SOURCE LINE 149
            __M_writer(u'        </tbody>\n        </table>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_admin_event_log(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 13
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="section-wrapper">\n            <div class="browse">\n                <h4 class="section-header smaller">Event Log</h4>\n                A record of configuration and administrative changes to the workshop.<br />\n                ')
        # SOURCE LINE 19
        wEvents = eventLib.getParentEvents(c.w) 
        
        __M_writer(u'\n                <table class="table table-bordered">\n                <thead>\n                <tr><th>Workshop Events</th></tr>\n                </thead>\n                <tbody>\n')
        # SOURCE LINE 25
        if wEvents:
            # SOURCE LINE 26
            for wE in wEvents:
                # SOURCE LINE 27
                __M_writer(u'                        <tr><td><strong>')
                __M_writer(escape(wE.date))
                __M_writer(u' ')
                __M_writer(escape(wE['title']))
                __M_writer(u'</strong> ')
                __M_writer(escape(wE['data']))
                __M_writer(u'</td></tr>\n')
                pass
            pass
        # SOURCE LINE 30
        __M_writer(u'                </tbody>\n                </table>\n            </div><!-- browse -->\n        </div><!-- section-wrapper -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_marked_items(context):
    context.caller_stack._push_frame()
    try:
        def flaggedItems(items):
            return render_flaggedItems(context,items)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 280
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Manage Workshop</h4>\n            <p>Items that have been flagged, <span class="badge badge-warning">disabled</span>, or <span class="badge badge-success">enabled</span></p>\n            ')
        # SOURCE LINE 285
        __M_writer(escape(flaggedItems(c.flaggedItems)))
        __M_writer(u'\n        </div><!-- browse -->\n    </div><!-- section-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_admin_listeners(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 154
        __M_writer(u'\n')
        # SOURCE LINE 155
        if c.w['public_private'] != 'trial':
            # SOURCE LINE 156
            __M_writer(u'        <div ng-controller="listenerController" ng-init="user=\'')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u"'; code='")
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u"'; url='")
            __M_writer(escape(c.w['url']))
            __M_writer(u'\'; getList()">\n        <table class="table table-bordered">\n        <thead>\n        <tr><th>Officials \n        <button type="button" class="pull-right btn btn-small btn-success" data-toggle="collapse" data-target="#addlistener">\n        + Listener\n        </button>\n        <div id="addlistener" class="collapse">\n            <div class="spacer"></div>\n            <form id="addListener" ng-submit="saveListener()" class="form-inline" name="addListener">\n                New Listener: \n                <input type="text" name="lName" class="input-medium" ng-model="lName" placeholder="Name" required>\n                <input type="text" name="lTitle" class="input-medium" ng-model="lTitle" placeholder="Title" required>\n                <input type="text" name="lEmail" class="input-medium" ng-model="lEmail" placeholder="Email" required>\n                <button type="submit" class="btn btn-warning">Save</button>\n                <br />\n                <span ng-show="addListenerShow">{{addListenerResponse}}</span>\n            </form>\n        </div><!-- collapse -->\n        </th></th>\n        </thead>\n        <tbody>\n        <tr ng-repeat="listener in listeners">\n        <td>\n            <a href="{{listener.profileLink}}" class="{{listener.state}}"><img class="avatar small-avatar" src="{{listener.userImage}}"> <span id="listenerName{{listener.urlCode}}">{{listener.lName}}</span>, <span id="listenerTitle{{listener.urlCode}}">{{listener.lTitle}}</span> ({{listener.state}})</a>\n            <div class="btn-group pull-right"><button class=" btn btn-small btn-success" data-toggle="collapse" id="toggleButton{{listener.urlCode}}" data-target="#disableListener{{listener.urlCode}}">\n            {{listener.button}}</button> <button class="btn btn-small btn-success" data-toggle="collapse" data-target="#editListener{{listener.urlCode}}">\n            Edit</button></div><!-- btn-group -->\n            <div id="disableListener{{listener.urlCode}}" class="collapse">\n                <form id="toggleForm{{listener.urlCode}}" ng-submit="toggleListener(\'{{listener.urlCode}}\')" class="form-inline" name="toggleForm{{listener.urlCode}}">\n                <input type="text" name="lReason" ng-model="lReason" placeholder="Reason" required>\n                <button type="submit" class="btn btn-warning" id="toggleSubmit{{listener.urlCode}}">{{listener.button}} Listener</button>\n                <br />\n                <span id="toggleListenerResponse{{listener.urlCode}}"></span>\n                </form>\n            </div><!-- collapse -->\n            <div id="editListener{{listener.urlCode}}" class="collapse">\n                <form id="editForm{{listener.urlCode}}" ng-submit="editListener(\'{{listener.urlCode}}\')" class="form-inline" name="editForm{{listener.urlCode}}">\n                Edit Listener:<br />\n                Name: <input type="text" class="input-small" id="lName" name="lName" value="{{listener.lName}}" required>\n                Title: <input type="text" class="input-small" id="lTitle" name="lTitle" value="{{listener.lTitle}}" required>\n                Email: <input type="text" class="input-small" id="lEmail" name="lEmail" value="{{listener.lEmail}}" required>\n                <button type="submit" class="btn btn-warning">Save Changes</button>\n                <br />\n                <span id="editListenerResponse{{listener.urlCode}}"></span>\n                </form>\n            </div><!-- collapse -->\n        </td>\n        </tr>\n        </tbody>\n        </table>\n        </div><!-- listenerController -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


