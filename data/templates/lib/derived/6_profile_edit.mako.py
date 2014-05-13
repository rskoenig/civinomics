# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398542813.7620749
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_profile_edit.mako'
_template_uri = u'/lib/derived/6_profile_edit.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['editProfile', 'linkAccounts', 'preferences', 'memberEvents', 'memberAdmin', 'changePassword', 'profileInfo', 'profilePicture']


# SOURCE LINE 1

import pylowiki.lib.db.user             as userLib
import pylowiki.lib.db.listener         as listenerLib
import pylowiki.lib.db.facilitator      as facilitatorLib
import pylowiki.lib.db.workshop         as workshopLib
import pylowiki.lib.db.mainImage        as mainImageLib
import pylowiki.lib.db.discussion       as discussionLib
import pylowiki.lib.db.comment          as commentLib
import pylowiki.lib.db.event            as eventLib
import pylowiki.lib.db.generic          as generic


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 13
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 16
    ns = runtime.TemplateNamespace(u'helpersEdit', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_edit.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpersEdit')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 11
        __M_writer(u' \n\n')
        # SOURCE LINE 13
        __M_writer(u'\n\n')
        # SOURCE LINE 129
        __M_writer(u'\n\n')
        # SOURCE LINE 200
        __M_writer(u'\n\n')
        # SOURCE LINE 309
        __M_writer(u'\n\n')
        # SOURCE LINE 345
        __M_writer(u'\n\n')
        # SOURCE LINE 367
        __M_writer(u'\n\n')
        # SOURCE LINE 405
        __M_writer(u'\n\n')
        # SOURCE LINE 427
        __M_writer(u'\n\n')
        # SOURCE LINE 478
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editProfile(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        helpersEdit = _mako_get_namespace(context, 'helpersEdit')
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u'\n    ')
        # SOURCE LINE 16
        __M_writer(u'\n    ')
        # SOURCE LINE 17

        tab1active = ""
        tab2active = ""
        tab3active = ""
        tab4active = ""
        tab5active = ""
        tab6active = ''
        prefactive = ''
        linkactive = ''
                    
        if c.tab == "tab1":
            tab1active = "active"
        elif c.tab == "tab2":
            tab2active = "active"
        elif c.tab == "tab3":
            tab3active = "active"
        elif c.tab == "tab4":
            tab4active = "active"
        elif c.tab == "tab5":
            tab5active = "active"
        elif c.tab == 'tab6':
            tab6active = 'tab6'
        else:
            tab1active = "active"
            
        msgString = ''
        if c.unreadMessageCount != 0:
            msgString = ' (' + str(c.unreadMessageCount) + ')'
            
        
        # SOURCE LINE 45
        __M_writer(u'\n    <div class="row-fluid">\n')
        # SOURCE LINE 47
        if c.conf['read_only.value'] == 'true':
            # SOURCE LINE 48
            __M_writer(u'            <h1> Sorry, Civinomics is in read only mode right now </h1>\n')
            # SOURCE LINE 49
        else:
            # SOURCE LINE 50
            __M_writer(u'            <div class="tabbable">\n                <div class="span3">\n                    <div class="section-wrapper">\n                        <div class="browse">\n                            <ul class="nav nav-pills nav-stacked">\n                            <li class="')
            # SOURCE LINE 55
            __M_writer(escape(tab1active))
            __M_writer(u'"><a href="#tab1" data-toggle="tab">1. Info\n                            </a></li>\n                            <li class="')
            # SOURCE LINE 57
            __M_writer(escape(tab6active))
            __M_writer(u'"><a href="#tab6" data-toggle="tab">2. Picture\n                            </a></li>\n                            <li class="')
            # SOURCE LINE 59
            __M_writer(escape(tab4active))
            __M_writer(u'"><a href="#tab4" data-toggle="tab">3. Password\n                            </a></li>\n                            <li class="')
            # SOURCE LINE 61
            __M_writer(escape(prefactive))
            __M_writer(u'"><a href="#pref" data-toggle="tab">4. Preferences\n                            </a></li>\n                            <li class="')
            # SOURCE LINE 63
            __M_writer(escape(linkactive))
            __M_writer(u'"><a href="#link" data-toggle="tab">5. Sharing\n                            </a></li>\n')
            # SOURCE LINE 65
            if c.admin:
                # SOURCE LINE 66
                __M_writer(u'                            <li class="')
                __M_writer(escape(tab5active))
                __M_writer(u'"><a href="#tab5" data-toggle="tab">6. Administrate\n                            Admin only - shhh!.</a></li>\n')
                pass
            # SOURCE LINE 69
            if c.user['memberType'] != 'organization' and not c.privs['provisional']:
                # SOURCE LINE 70
                __M_writer(u'                                <a href="#upgradeOrg" role="button" class="btn btn-success" data-toggle="modal">Upgrade to Organization</a>\n                                <div id="upgradeOrg" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="upgradeOrgLabel" aria-hidden="true">\n                                    <div class="modal-header">\n                                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\xd7</button>\n                                        <h3 id="myModalLabel">Upgrade to Organization</h3>\n                                    </div>\n                                    <div class="modal-body">\n                                        <p>Organizations are a special class of membership:</p>\n                                        <ul>\n                                        <li>Organizations can\'t vote, only individuals. Sorry.</li>\n                                        <li>Organizations can be voted up or down</li>\n                                        <li>Members can post topics or comments in Organization forums</li>\n                                        <li>Organization get easy to remember Civinomics addresses: civinomics.com/YourOrganization</li>\n                                        <li>Organizations are listed as a separate category in search results</li>\n                                        </ul>\n                                    </div>\n                                    <div class="modal-footer">\n                                        <button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>\n                                        <a href="/profile/')
                # SOURCE LINE 88
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/organization/upgrade/handler" class="btn btn-primary">Upgrade to Organization</a>\n                                    </div>\n                            </div>\n')
                pass
            # SOURCE LINE 92
            __M_writer(u'                            </ul>\n                        </div><!-- browse -->\n                    </div><!-- section-wrapper -->\n                </div> <!-- /.span3 -->\n                <div class="span9">\n                    ')
            # SOURCE LINE 97
            __M_writer(escape(lib_6.fields_alert()))
            __M_writer(u'\n')
            # SOURCE LINE 98
            if c.conf['read_only.value'] == 'true':
                # SOURCE LINE 99
                __M_writer(u'                        <!-- read only -->\n')
                # SOURCE LINE 100
            else:
                # SOURCE LINE 101
                __M_writer(u'                        <div class="tab-content">\n                            <div class="tab-pane ')
                # SOURCE LINE 102
                __M_writer(escape(tab1active))
                __M_writer(u'" id="tab1">\n                                ')
                # SOURCE LINE 103
                __M_writer(escape(helpersEdit.profileInfo()))
                __M_writer(u'\n                            </div><!-- tab1 -->\n                            <div class="tab-pane ')
                # SOURCE LINE 105
                __M_writer(escape(tab4active))
                __M_writer(u'" id="tab4">\n                                ')
                # SOURCE LINE 106
                __M_writer(escape(helpersEdit.changePassword()))
                __M_writer(u'\n                            </div><!-- tab4 -->\n                            <div class="tab-pane ')
                # SOURCE LINE 108
                __M_writer(escape(tab6active))
                __M_writer(u'" id="tab6">\n                                ')
                # SOURCE LINE 109
                __M_writer(escape(helpersEdit.profilePicture()))
                __M_writer(u'\n                            </div><!-- tab6 -->\n                            <div class="tab-pane ')
                # SOURCE LINE 111
                __M_writer(escape(prefactive))
                __M_writer(u'" id="pref">\n                                ')
                # SOURCE LINE 112
                __M_writer(escape(helpersEdit.preferences()))
                __M_writer(u'\n                            </div><!-- preferences -->\n                            <div class="tab-pane ')
                # SOURCE LINE 114
                __M_writer(escape(linkactive))
                __M_writer(u'" id="link">\n                                ')
                # SOURCE LINE 115
                __M_writer(escape(helpersEdit.linkAccounts()))
                __M_writer(u'\n                            </div><!-- sharing -->\n')
                # SOURCE LINE 117
                if c.admin:
                    # SOURCE LINE 118
                    __M_writer(u'                                <div class="tab-pane ')
                    __M_writer(escape(tab5active))
                    __M_writer(u'" id="tab5">\n                                    ')
                    # SOURCE LINE 119
                    __M_writer(escape(helpersEdit.memberAdmin()))
                    __M_writer(u'\n                                    ')
                    # SOURCE LINE 120
                    __M_writer(escape(helpersEdit.memberEvents()))
                    __M_writer(u'\n                                </div><!-- tab5 -->\n')
                    pass
                # SOURCE LINE 123
                __M_writer(u'                        </div><!-- tab-content -->\n')
                pass
            # SOURCE LINE 125
            __M_writer(u'                </div> <!-- /.span9 -->\n            </div><!-- tabbable -->\n')
            pass
        # SOURCE LINE 128
        __M_writer(u'    </div> <!-- /.row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_linkAccounts(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 369
        __M_writer(u'\n    ')
        # SOURCE LINE 370
 
        facebookChecked = ''
        twitterChecked = ''
        if 'facebookAuthId' in c.user:
            facebookChecked = 'checked'
        if 'twitterAuthId' in c.user:
            twitterChecked = 'checked'
            
        
        # SOURCE LINE 377
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Social Network Sharing</h4>\n            <div class="row-fluid">\n                <div class="span3">Facebook account:</div>\n                <div class="span6">\n')
        # SOURCE LINE 384
        if facebookChecked == 'checked':
            # SOURCE LINE 385
            __M_writer(u'                        Email registered with facebook:\n                        <input type="text" id="fbEmail" class="span10" name="fbEmail" ng-model="fbEmail" ng-init="fbEmail=\'')
            # SOURCE LINE 386
            __M_writer(escape(c.user['fbEmail']))
            __M_writer(u'\'" required>\n')
            # SOURCE LINE 387
        else:
            # SOURCE LINE 388
            __M_writer(u'                        Account not connected with facebook.\n')
            pass
        # SOURCE LINE 390
        __M_writer(u'                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span3">Twitter account:</div>\n                <div class="span6">\n')
        # SOURCE LINE 395
        if twitterChecked == 'checked':
            # SOURCE LINE 396
            __M_writer(u'                        Email registered with twitter:\n                        <input type="text" id="email" class="span10" name="email" ng-model="email" ng-init="email=\'')
            # SOURCE LINE 397
            __M_writer(escape(c.user['email']))
            __M_writer(u'\'" required>\n')
            # SOURCE LINE 398
        else:
            # SOURCE LINE 399
            __M_writer(u'                        Account not connected with twitter.\n')
            pass
        # SOURCE LINE 401
        __M_writer(u'                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n        </div><!-- browse -->\n    </div><!-- section-wrapper-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_preferences(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 347
        __M_writer(u'\n    ')
        # SOURCE LINE 348
 
        commentsChecked = ''
        if 'commentAlerts' in c.user and c.user['commentAlerts'] == '1':
            commentsChecked = 'checked'
            
        
        # SOURCE LINE 352
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Preferences</h4>\n            <div class="row-fluid">\n                <div class="span3">Email when:</div>\n                <div class="span6">\n                    <form ng-init="code=\'')
        # SOURCE LINE 359
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u"'; url='")
        __M_writer(escape(c.user['url']))
        __M_writer(u'\'" class="no-bottom form-inline">\n                        New comments added to my items: <input type="checkbox" name="commentAlerts" value="comments" ng-click="emailOnComments()" ')
        # SOURCE LINE 360
        __M_writer(escape(commentsChecked))
        __M_writer(u'>\n                        <span ng-show="emailOnCommentsShow">{{emailOnCommentsResponse}}</span>\n                    </form>\n                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n        </div><!-- browse -->\n    </div><!-- section-wrapper-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_memberEvents(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 407
        __M_writer(u'\n')
        # SOURCE LINE 408
        if c.events:
            # SOURCE LINE 409
            __M_writer(u'       ')
            numEvents = len(c.events) 
            
            __M_writer(u'\n       ')
            # SOURCE LINE 410
            eString = "Events" 
            
            __M_writer(u'\n')
            # SOURCE LINE 411
            if numEvents == 1:
                # SOURCE LINE 412
                __M_writer(u'          ')
                eString = "Event" 
                
                __M_writer(u'\n')
                pass
            # SOURCE LINE 414
            __M_writer(u'       <strong>')
            __M_writer(escape(numEvents))
            __M_writer(u' ')
            __M_writer(escape(eString))
            __M_writer(u':</strong>\n       <br /><br />\n')
            # SOURCE LINE 416
            for event in c.events:
                # SOURCE LINE 417
                __M_writer(u'          ')
                user = userLib.getUserByID(event.owner) 
                
                __M_writer(u'\n          ')
                # SOURCE LINE 418
                __M_writer(escape(event['title']))
                __M_writer(u' ')
                __M_writer(escape(event.date))
                __M_writer(u'\n')
                # SOURCE LINE 419
                if user:
                    # SOURCE LINE 420
                    __M_writer(u'              by ')
                    __M_writer(escape(user['name']))
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 422
                __M_writer(u'          <br />\n          Reason: ')
                # SOURCE LINE 423
                __M_writer(escape(event['data']))
                __M_writer(u'\n          <br /><br />\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_memberAdmin(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 429
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header" style="text-align: center"><br />Administrate Member</h3><br />\n')
        # SOURCE LINE 433
        if c.user['disabled'] == '1':
            # SOURCE LINE 434
            __M_writer(u'                ')
            eAction = 'Enable' 
            
            __M_writer(u'\n')
            # SOURCE LINE 435
        else:
            # SOURCE LINE 436
            __M_writer(u'                ')
            eAction = 'Disable' 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 438
        __M_writer(u'            <form method="post" name="enableUser" id="enableUser" class="form-horizontal" action="/profile/')
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/enable/handler">\n            <strong>')
        # SOURCE LINE 439
        __M_writer(escape(eAction))
        __M_writer(u' Member</strong><br />\n            <fieldset>\n                <div class="control-group">\n                    <label for="enable" class="control-label">Reason for ')
        # SOURCE LINE 442
        __M_writer(escape(eAction))
        __M_writer(u'</label>\n                    <div class="controls">\n                        <input type="text" name="enableUserReason">\n                        <input type="radio" name="verifyEnableUser" value="0"> Verify ')
        # SOURCE LINE 445
        __M_writer(escape(eAction))
        __M_writer(u'\n                        &nbsp;&nbsp;<button type="submit" class="btn btn-warning">')
        # SOURCE LINE 446
        __M_writer(escape(eAction))
        __M_writer(u' Member</button>\n                    </div> <!-- /.controls -->\n                </div> <!-- /.control-group -->\n            </fieldset>\n            </form>\n            <br /><br />\n            ')
        # SOURCE LINE 452
 
        if c.user['accessLevel'] == '0':
            newAccess = "200"
            newTitle = "Admin"
            oldTitle = "User"
        else:
            newAccess = "0"
            newTitle = "User"
            oldTitle = "Admin"
                    
        
        # SOURCE LINE 461
        __M_writer(u'\n            <form method="post" name="userPrivs" id="userPrivs" class="form-horizontal" action="/profile/')
        # SOURCE LINE 462
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/privs/handler">\n            <strong>Change Access Level From ')
        # SOURCE LINE 463
        __M_writer(escape(oldTitle))
        __M_writer(u' To ')
        __M_writer(escape(newTitle))
        __M_writer(u'</strong><br />\n            <fieldset>\n            <div class="control-group">\n                <label for="setPrivs" class="control-label">Reason for Change</label>\n                <div class="controls">\n                    <input type="text" name="accessChangeReason">\n                    <input type="radio" name="accessChangeVerify" value="0"> Verify Change\n                    &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Change Access</button>\n                </div> <!-- /.controls -->\n            </div> <!-- /.control-group -->\n            </fieldset>\n            </form>\n            <br /><br />\n        </div><!-- browse -->\n    </div><!-- section-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_changePassword(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 311
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Update Your Password</h4>\n            <form action="/profile/')
        # SOURCE LINE 315
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/password/update/handler" enctype="multipart/form-data" method="post" class="form-horizontal">\n\t\t    <fieldset>\n            <div class="control-group">\n                <label for="oldPassword" class="control-label">Old Password:</label>\n                <div class="controls">\n                    <input type="password" id="oldPassword" name="oldPassword">\n                    <span class="help-inline"> If you reset your password, this is the random string you received via email.</span>\n                </div> <!-- /.controls -->\n            </div> <!-- /.control-group -->\n            <div class="control-group">\n                <label for="newPassword" class="control-label">New Password:</label>\n                <div class="controls">\n                    <input type="password" id="newPassword" name="newPassword">\n                </div> <!-- /.controls -->\n            </div> <!-- /.control-group -->\n            <div class="control-group">\n                <label for="reNewPassword" class="control-label">Repeat New Password:</label>\n                <div class="controls">\n                    <input type="password" id="reNewPassword" name="reNewPassword">\n                </div> <!-- /.controls -->\n            </div> <!-- /.control-group -->\n            <div class="control-group">\n                <div class="controls">\n                    <button type="submit" class="btn btn-warning" name="submit">Save Changes</button>\n                </div> <!-- /.controls -->\n            </div> <!-- /.control-group -->\n            </fieldset>\n            </form>\n        </div><!-- browse -->\n    </div><!-- section-wrapper-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_profileInfo(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 131
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n\t        <form id="infoEdit" name="infoEdit" class="form-horizontal edit-profile">\n    \t\t    <h4 class="section-header smaller">Update Your Profile Information</h4>\n                <fieldset>\n                <div class="control-group">\n\t\t\t\t    <label for="member-name" class="control-label">Membership Type:</label>\n\t\t\t\t    ')
        # SOURCE LINE 139
 
        memberType = 'Individual'
        if c.user['memberType'] == 'organization':
            memberType = 'Organization'
                                            
        
        # SOURCE LINE 143
        __M_writer(u'\n\t\t\t\t    <div class="controls">\n\t\t\t\t\t    ')
        # SOURCE LINE 145
        __M_writer(escape(memberType))
        __M_writer(u'\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n\t\t\t    <div ng-class=" {\'control-group\': true, \'error\': infoEdit.member_name.$error.pattern} ">\n\t\t\t\t    <label for="member-name" class="control-label">Your Name:</label>\n\t\t\t\t    <div class="controls">\n\t\t\t\t\t    <input type="text" id="member-name" class="span10" name="member_name" value="')
        # SOURCE LINE 151
        __M_writer(escape(c.user['name']))
        __M_writer(u'" ng-model="fullName" ng-init="fullName=\'')
        __M_writer(escape(c.user['name']))
        __M_writer(u'\'" ng-pattern="fullNameRegex" required>\n                        <span class="error help-block" ng-show="infoEdit.member_name.$error.pattern">Use only letters, numbers, spaces, and _ (underscore)</span>\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n\t\t\t    <div class="control-group">\n\t\t\t\t    <label for="email" class="control-label">Email:</label>\n\t\t\t\t    <div class="controls">\n\t\t\t\t\t    <input type="text" id="email" class="span10" name="email" ng-model="email" ng-init="email=\'')
        # SOURCE LINE 158
        __M_writer(escape(c.user['email']))
        __M_writer(u'\'" required>\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n                <div ng-class=" {\'control-group\': true, \'error\': infoEdit.postalCode.$error.pattern} ">\n\t\t\t\t    <label for="postalCode" class="control-label">Postal code:</label>\n                    <div class="controls">\n\t\t\t\t\t    <input type="text" id="postalCode" class="span10" name="postalCode" onBlur="geoCheckPostalCode()" ng-model="postalCode" ng-init="postalCode=\'')
        # SOURCE LINE 164
        __M_writer(escape(c.user['postalCode']))
        __M_writer(u'\'" ng-pattern="postalCodeRegex" required>\n                        <br />\n                        <span class="error help-block" ng-show="infoEdit.postalCode.$error.pattern">Use only numbers.</span>\n                        <span id="postalCodeResult"></span>\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n        \t    <div class="control-group">\n\t\t\t\t    <label for="greetingMsg" class="control-label">Short bio:</label>\n\t\t\t\t    <div class="controls">\n                        <input type="text" name="greetingMsg" ng-model="greetingMsg" ng-init="greetingMsg=\'')
        # SOURCE LINE 173
        __M_writer(escape(c.user['greetingMsg']))
        __M_writer(u'\'" rows=4 class="span10">\n                        <span class="help-block">Displayed with your posts<br>(example: Thomas Jefferson, Founding Father)</span>\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n       \t        <div class="control-group">\n\t\t\t\t    <label for="orgLink" class="control-label">Your website:</label>\n    \t\t\t    <div class="controls">\n                        <input type="text" class="span10" name="websiteLink" ng-model="websiteLink" ng-init="websiteLink=\'')
        # SOURCE LINE 180
        __M_writer(escape(c.user['websiteLink']))
        __M_writer(u'\'">\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n       \t        <div class="control-group">\n\t\t\t\t    <label for="orgLinkMsg" class="control-label">A description of your website:</label>\n\t\t\t\t    <div class="controls">\n                        <textarea name="websiteDesc" ng-model="websiteDesc" ng-init="websiteDesc=\'')
        # SOURCE LINE 186
        __M_writer(escape(c.user['websiteDesc']))
        __M_writer(u'\'" rows=4 class="span10"></textarea>\n\t\t\t\t    </div> <!-- /.controls -->\n\t\t\t    </div> <!-- /.control-group -->\n                <div class="form-actions save-profile" ng-class="{\'light-yellow\':infoEdit.$dirty && submitStatus == -1, \'light-blue\':!infoEdit.$dirty && submitStatus == -1, \'light-green\':submitStatus == 0, \'light-red\':submitStatus == 1}">\n                    <input type="submit" class="btn btn-warning" ng-class="{\'disabled\':!infoEdit.$dirty}" value="Save changes" ng-click="submitProfileEdit()"></input>\n                    <span class="help-inline" ng-show="!infoEdit.$dirty && submitStatus == -1" ng-cloak>No Changes</span>\n                    <span class="help-inline" ng-show="infoEdit.$dirty && submitStatus == -1" ng-cloak>Unsaved Changes</span>\n                    <span class="help-inline" ng-show="submitStatus == 0" ng-cloak>Successfully saved changes</span>\n                    <span class="help-inline" ng-show="submitStatus == 1" ng-cloak>Error saving changes</span>\n                </div>\n                </fieldset>\n\t        </form>\n        </div><!-- browse -->\n    </div><!-- section-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_profilePicture(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 202
        __M_writer(u'\n')
        # SOURCE LINE 204
        __M_writer(u'     <div class="section-wrapper" ng-init="code=\'')
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u"'; url='")
        __M_writer(escape(c.user['url']))
        __M_writer(u'\'">\n        <div class="browse">\n            <h4 class="section-header smaller">Add or Change Your Pictures</h4>\n            <form class="form-horizontal" id="setImageSourceForm" name="setImageSourceForm">\n')
        # SOURCE LINE 208
        if 'facebookAuthId' in c.user.keys():
            # SOURCE LINE 209
            __M_writer(u'                    <div class="control-group">\n                        <label class="control-label" for="avatarType">\n                            ')
            # SOURCE LINE 211
            __M_writer(escape(lib_6.userImage(c.user, className="avatar avatar-small", forceSource="facebook")))
            __M_writer(u'\n                        </label>\n                        <div class="controls chooseAvatar">\n                            <label class="radio">\n                                <input type="radio" value="facebook" name="avatarType" id="avatarType" ng-click="uploadImage = false" ng-model="imageSource">\n                                    Use your facebook image\n                                </input>\n                            </label>\n                        </div>\n                    </div>\n')
            pass
        # SOURCE LINE 222
        __M_writer(u'                \n                <div class="control-group">\n                    <label class="control-label" for="avatarType">\n                        ')
        # SOURCE LINE 225
        __M_writer(escape(lib_6.userImage(c.user, className="avatar avatar-small", forceSource="gravatar")))
        __M_writer(u'\n                    </label>\n                    <div class="controls chooseAvatar">\n                        <label class="radio">\n                            <input type="radio" value="gravatar" name="avatarType" id="avatarType" ng-click="uploadImage = false" ng-model="imageSource">\n                                Use your \n                                <a href="http://gravatar.com" target="_blank">gravatar</a> \n                                image\n                            </input>\n                        </label>\n                    </div>\n                </div>\n                <div class="control-group">\n                    <label class="control-label" for="avatarType">\n                        ')
        # SOURCE LINE 239
        __M_writer(escape(lib_6.userImage(c.user, className="avatar avatar-small", forceSource="civ")))
        __M_writer(u'\n                    </label>\n                    <div class="controls chooseAvatar">\n                        <label class="radio">\n                            <input type="radio" value="civ" name="avatarType" id="avatarType" ng-click="uploadImage = true" ng-model="imageSource">\n                                Use your uploaded image\n                            </input>\n                        </label>\n                    </div>\n                </div>\n                <div class="form-actions save-profile" ng-class="{\'light-yellow\':setImageSourceForm.$dirty && submitStatus == -1, \'light-blue\':!setImageSourceForm.$dirty && submitStatus == -1, \'light-green\':submitStatus == 0, \'light-red\':submitStatus == 1}">\n                    <input type="submit" class="btn btn-warning" ng-class="{\'disabled\':!setImageSourceForm.$dirty}" value="Save changes" ng-click="setImageSource()"></input>\n                    <span class="help-inline" ng-show="!setImageSourceForm.$dirty && submitStatus == -1" ng-cloak>No Changes</span>\n                    <span class="help-inline" ng-show="setImageSourceForm.$dirty && submitStatus == -1" ng-cloak>Unsaved Changes</span>\n                    <span class="help-inline" ng-show="submitStatus == 0" ng-cloak>Successfully saved changes</span>\n                    <span class="help-inline" ng-show="submitStatus == 1" ng-cloak>Error saving changes</span>\n                </div>\n            </form>\n            <form id="fileupload" action="/profile/')
        # SOURCE LINE 257
        __M_writer(escape(c.authuser['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.authuser['url']))
        __M_writer(u'/picture/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: \'fileupload-processing\'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="uploadImage">\n                <!-- Redirect browsers with JavaScript disabled to the origin page -->\n                <noscript>&lt;input type="hidden" name="redirect" value="http://blueimp.github.com/jQuery-File-Upload/"&gt;</noscript>\n                <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->\n                <div id="fileupload-button-div" class="row-fluid fileupload-buttonbar collapse in">\n                    <div class="span10 offset1">\n                        <!-- The fileinput-button span is used to style the file input field as button -->\n                        <span class="btn btn-success fileinput-button span6 offset3" data-toggle="collapse" data-target="#fileupload-button-div">\n                            <i class="icon-plus icon-white"></i>\n                            <span>Select your picture</span>\n                            <input type="file" name="files[]">\n                        </span>\n                        <!-- The loading indicator is shown during file processing -->\n                        <div class="fileupload-loading"></div>\n                    </div>\n                    <!-- The global progress information -->\n                </div>\n                <div class="row-fluid">\n                    <div class="span10 offset1 fade" data-ng-class="{true: \'in\'}[!!active()]">\n                        <!-- The global progress bar -->\n                        <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + \'%\'}"></div></div>\n                        <!-- The extended global progress information -->\n                        <div class="progress-extended">&nbsp;</div>\n                    </div>\n                </div>\n                <!-- The table listing the files available for upload/download -->\n                <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">\n                    <tbody><tr data-ng-repeat="file in queue">\n                        <td data-ng-switch="" on="!!file.thumbnail_url">\n                            <div class="preview" data-ng-switch-when="true">\n                                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"> New profile photo uploaded.</a>\n                            </div>\n                            <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>\n                        </td>\n                        <td>\n                            <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>\n                        </td>\n                        <td>\n                            <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">\n                                <i class="icon-upload icon-white"></i>\n                                <span>Start</span>\n                            </button>\n                            <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel" data-toggle="collapse" data-target="#fileupload-button-div">\n                                <i class="icon-ban-circle icon-white"></i>\n                                <span>Cancel</span>\n                            </button>\n                        </td>\n                    </tr>\n                </tbody></table>\n            </form>\n        </div><!-- browse -->\n    </div><!-- section-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


