# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398538074.43221
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/admin_helpers/configure.mako'
_template_uri = u'/lib/admin_helpers/configure.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['fields_alert', 'emailInvite', 'edit_background', 'tags', 'private', 'intro', 'change_scope', 'basic', 'scope', 'public', 'publish']


# SOURCE LINE 1

import time
from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList
from pylowiki.lib.db.user import getUserByEmail
from pylowiki.lib.db.tag import getWorkshopTagCategories
import pylowiki.lib.db.workshop         as workshopLib


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 36
        __M_writer(u'\n\n')
        # SOURCE LINE 44
        __M_writer(u'\n\n\n')
        # SOURCE LINE 143
        __M_writer(u'\n\n')
        # SOURCE LINE 171
        __M_writer(u'\n\n')
        # SOURCE LINE 223
        __M_writer(u'\n\n\n\n')
        # SOURCE LINE 247
        __M_writer(u'\n\n')
        # SOURCE LINE 297
        __M_writer(u'\n\n')
        # SOURCE LINE 359
        __M_writer(u'\n\n')
        # SOURCE LINE 533
        __M_writer(u'\n\n')
        # SOURCE LINE 556
        __M_writer(u'\n\n')
        # SOURCE LINE 573
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fields_alert(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 9
        __M_writer(u'\n')
        # SOURCE LINE 10
        if 'alert' in session:
            # SOURCE LINE 11
            __M_writer(u'\t\t')
            alert = session['alert'] 
            
            __M_writer(u' \n            <div class="alert alert-')
            # SOURCE LINE 12
            __M_writer(escape(alert['type']))
            __M_writer(u' workshop-admin" style="overflow: visible;">\n')
            # SOURCE LINE 15
            __M_writer(u'                <button data-dismiss="alert" class="close">x</button>\n')
            # SOURCE LINE 16
            if 'upgrade to a Professional' in alert['title']:
                # SOURCE LINE 17
                __M_writer(u'                    <div class="row-fluid">\n                        <div class="span8">\n                            <strong>')
                # SOURCE LINE 19
                __M_writer(escape(alert['title']))
                __M_writer(u'</strong>\n                        </div>\n                        <div class="span4">\n                            <form name="workshopUpgrade" id="workshopUpgrade" action="/workshop/')
                # SOURCE LINE 22
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/upgrade/handler" method="POST" class="no-bottom">\n                                <button type="submit" class="btn btn-large btn-civ pull-right">Upgrade to Pro</button>\n                            </form>\n                        </div>\n                    </div>\n')
                # SOURCE LINE 27
            else:
                # SOURCE LINE 28
                __M_writer(u'                    <strong>')
                __M_writer(escape(alert['title']))
                __M_writer(u'</strong>\n')
                pass
            # SOURCE LINE 30
            __M_writer(u'            </div>\n        ')
            # SOURCE LINE 31
 
            session.pop('alert')
            session.save()
                    
            
            # SOURCE LINE 34
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_emailInvite(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 558
        __M_writer(u'\n    <form name="private" id="private" class="left form-inline" action="/workshop/')
        # SOURCE LINE 559
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >\n        <div class="row-fluid">\n            <label for="newMember" class="help-inline">Enter the email addresses of people to invite, separated by commas or cut and paste from Excel.</label>\n            <textarea class="input-block-level" rows=1 name="newMember"/></textarea>\n        </div><!-- row-fluid -->\n        <div class="row-fluid">\n            <label for="inviteMsg" class="help-inline">Add optional message to email invitation:</label>\n            <textarea class="input-block-level" rows=2 name="inviteMsg"/></textarea><br />\n            <!-- \n            <a href="/workshop/')
        # SOURCE LINE 568
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/previewInvitation" target="_blank">Preview Invitation</a> (will open in a new window)<br />\n            -->\n        </div><!-- row-fluid -->\n        <br /><button type="submit" class="btn btn-primary" name="addMember"><i class="icon-envelope icon-white"></i> Send Invites</button>\n    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_edit_background(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 227
        __M_writer(u'\n    <div class="section-wrapper wiki-well">\n        <div class="browse">\n            <h4 class="section-header smaller">Background</h4>\n            <a href="#" class="btn btn-mini btn-info pull-left bottom-space" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-list"></i> <i class="icon-picture"></i> View Formatting Guide</a>\n            <form name="workshop_background" id="workshop_background" class="left form-inline" action = "/workshop/')
        # SOURCE LINE 232
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/update/background/handler" enctype="multipart/form-data" method="post" >\n               <textarea rows="10" id="data" name="data" class="span12">')
        # SOURCE LINE 233
        __M_writer(escape(c.page['data']))
        __M_writer(u'</textarea>\n               <div class="background-edit-wrapper">\n')
        # SOURCE LINE 235
        if not c.published:
            # SOURCE LINE 236
            __M_writer(u'                        <button type="submit" name="submit" class="btn btn-warning pull-right">Save Background and Continue</button>\n')
            # SOURCE LINE 237
        else:
            # SOURCE LINE 238
            __M_writer(u'                        <button type="submit" name="submit" class="btn btn-warning pull-right">Save Changes</button>\n')
            pass
        # SOURCE LINE 240
        __M_writer(u'               </div><!-- text-align -->\n            </form>\n            <div class="preview-information-wrapper" id="live_preview">\n               hi\n            </div>\n        </div><!-- browse -->\n    </div><!-- sectio-wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 173
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Tags</h4>\n            Tags are descriptive key words used to categorize your workshop.<br />\n            <form name="workshop_tags" id="workshop_tags" class="left form-inline" action = "/workshop/')
        # SOURCE LINE 178
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/configureTagsWorkshopHandler" enctype="multipart/form-data" method="post" >\n            <div class="row-fluid">\n                <div class="span1">\n                </div><!-- span1 -->\n                <div class="span5">\n                    ')
        # SOURCE LINE 183
 
        tagList = getWorkshopTagCategories()
                            
        
        # SOURCE LINE 185
        __M_writer(u'\n                    <br />\n                    <strong>Pick 1 or 2</strong> <span class="help-inline"><span class="label label-important">Required</span></span><br />\n                    <fieldset>\n')
        # SOURCE LINE 189
        for tag in tagList:
            # SOURCE LINE 190
            if tag in c.categories:
                # SOURCE LINE 191
                __M_writer(u'                            ')
                checked = 'checked' 
                
                __M_writer(u'\n')
                # SOURCE LINE 192
            else:
                # SOURCE LINE 193
                __M_writer(u'                            ')
                checked = 'unchecked' 
                
                __M_writer(u'\n')
                pass
            # SOURCE LINE 195
            __M_writer(u'                        <label class="checkbox">\n                        <input type="checkbox" name="categoryTags" value="')
            # SOURCE LINE 196
            __M_writer(escape(tag))
            __M_writer(u'" ')
            __M_writer(escape(checked))
            __M_writer(u' /> ')
            __M_writer(escape(tag))
            __M_writer(u'\n                        </label><br />\n')
            pass
        # SOURCE LINE 199
        __M_writer(u'                    </fieldset>\n                    <br />\n')
        # SOURCE LINE 201
        if not c.published:
            # SOURCE LINE 202
            __M_writer(u'                        <button type="submit" class="btn btn-warning">Save Tags and Continue</button>\n')
            # SOURCE LINE 203
        else:
            # SOURCE LINE 204
            __M_writer(u'                        <button type="submit" class="btn btn-warning">Save Tags</button>\n')
            pass
        # SOURCE LINE 206
        __M_writer(u'                </div><!-- span5 -->\n            </div><!-- row -->\n            </form>\n        </div><!-- browse -->\n    </div><!-- section-header -->\n\n    <script>\n        $(function(){\n            var max = 2;\n            var checkboxes = $(\'input[type="checkbox"]\');\n\n            checkboxes.change(function(){\n                var current = checkboxes.filter(\':checked\').length;\n                checkboxes.filter(\':not(:checked)\').prop(\'disabled\', current >= max);\n                });\n        });\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_private(context):
    context.caller_stack._push_frame()
    try:
        def emailInvite():
            return render_emailInvite(context)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 299
        __M_writer(u'\n\n')
        # SOURCE LINE 301
        if c.w['public_private'] != 'public':
            # SOURCE LINE 302
            __M_writer(u'        <div class="container-fluid well">\n            <table class="boxOffsetParent">\n                <tr>\n                    <td rowspan="2" class="scope-icon">\n                        <i class="icon-group icon-4x"></i>\n                    </td>\n                    <td>\n                        <h4><lead>Private</lead></h4>\n                    </td>\n                </tr>\n                <tr>\n                    <td>\n                        <ul>\n                            <li>Private workshops are not visible to the public.</li>\n                            <li>Private workshops are invitation only.</li>\n')
            # SOURCE LINE 317
            if c.w['type'] == 'personal':
                # SOURCE LINE 318
                __M_writer(u'                                <li>Free workshops are limited to 20 participants.</li>\n')
                pass
            # SOURCE LINE 320
            __M_writer(u'                        </ul>\n                    </td>\n                </tr>\n            </table>\n            <hr>\n            <div class="row-fluid">\n                <strong>Add People</strong><br>\n                    ')
            # SOURCE LINE 327
            __M_writer(escape(emailInvite()))
            __M_writer(u'\n                    <br>\n\n')
            # SOURCE LINE 330
            if c.pmembers:
                # SOURCE LINE 331
                __M_writer(u'                        <form name="private" id="private" class="left form-inline" action="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/configurePrivateWorkshopHandler" enctype="multipart/form-data" method="post" >\n                            <hr>\n                            <strong>Workshop Members (')
                # SOURCE LINE 333
                __M_writer(escape(len(c.pmembers)))
                __M_writer(u')</strong><br>\n                            <br>\n                            \n                            ')
                # SOURCE LINE 336
 
                memberList = []
                for pmember in c.pmembers:
                    memberList.append(pmember['email'])
                memberList.sort()
                                            
                
                # SOURCE LINE 341
                __M_writer(u'\n\n                            <select name="selected_members">\n')
                # SOURCE LINE 344
                for member in memberList:
                    # SOURCE LINE 345
                    __M_writer(u'                                <option valuevalue="')
                    __M_writer(escape(member))
                    __M_writer(u'">')
                    __M_writer(escape(member))
                    __M_writer(u'</option>\n')
                    pass
                # SOURCE LINE 347
                __M_writer(u'                            </select>\n\n                            <button type="submit" class="btn" name="resendInvites"><i class="icon-envelope"></i> Resend Invite</button>\n                            <button type="submit" class="btn btn-danger" name="deleteMembers"><i class="icon-trash icon-white"></i> Delete Member</button><br>\n                            <br>\n                        </form>\n')
                pass
            # SOURCE LINE 354
            __M_writer(u'            </div><!-- row-fluid -->\n        </div><!-- container-fluid -->\n')
            pass
        # SOURCE LINE 357
        __M_writer(u'    </form>\n    <br />\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_intro(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 38
        __M_writer(u'\n    <div style="text-align: center">Build your workshop!<br />\n')
        # SOURCE LINE 40
        if not c.published:
            # SOURCE LINE 41
            __M_writer(u'       <br />Checklist must be completed before the workshop can be published.<br />\n')
            pass
        # SOURCE LINE 43
        __M_writer(u'    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_change_scope(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 249
        __M_writer(u'\n    <div class="span3"><strong>Current Scope:</strong></div>\n        ')
        # SOURCE LINE 251

        if c.w['public_private'] == 'public':
            currentScope = 'Public'
            newScope = 'Private'
        else:
            currentScope = 'Private'
            newScope = 'Public'
                
        
        # SOURCE LINE 258
        __M_writer(u'\n        <form name="scope" id="scope" class="left form-inline" action = "/workshop/')
        # SOURCE LINE 259
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/configure')
        __M_writer(escape(newScope))
        __M_writer(u'WorkshopHandler" enctype="multipart/form-data" method="post" >\n            <div class="row-fluid">\n                <div class="span2">\n                    <label class="radio">\n                        <input type="radio" name="optionsRadios" id="optionsRadios1" value="Private" \n')
        # SOURCE LINE 264
        if currentScope == 'Private':
            # SOURCE LINE 265
            __M_writer(u'                            checked\n')
            pass
        # SOURCE LINE 267
        __M_writer(u'                        >\n                        Private  <i class="icon-group set-scope-icon"></i>\n                    </label>\n                </div>\n                <div class="span2">\n                    <label class="radio">\n')
        # SOURCE LINE 273
        if c.w['type'] == 'professional':
            # SOURCE LINE 274
            __M_writer(u'                        <input type="radio" name="optionsRadios" id="optionsRadios2" value="Public"\n')
            # SOURCE LINE 275
            if currentScope == 'Public':
                # SOURCE LINE 276
                __M_writer(u'                            checked\n')
                pass
            # SOURCE LINE 278
            __M_writer(u'                        >\n                        Public  <i class="icon-globe set-scope-icon"></i>\n')
            # SOURCE LINE 280
        else:
            # SOURCE LINE 281
            __M_writer(u'                    <button class="transparent">\n                        <input type="radio" name="optionsRadios" id="optionsRadios2" value="Public" disabled>\n                    </button>\n                        Public  <i class="icon-globe set-scope-icon"></i>\n')
            pass
        # SOURCE LINE 286
        __M_writer(u'                    </label>\n                </div>\n                <div class="span3">\n')
        # SOURCE LINE 289
        if c.w['type'] == 'professional':
            # SOURCE LINE 290
            __M_writer(u'                        <button type="submit" class="btn btn-warning" name="changeScope">Change Scope</button>\n')
            # SOURCE LINE 291
        else:
            # SOURCE LINE 292
            __M_writer(u'                        <button class="disabled btn btn-warning">Change Scope</button>\n')
            pass
        # SOURCE LINE 294
        __M_writer(u'                </div> \n            </div>  \n        </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_basic(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 47
        __M_writer(u'\n\n    ')
        # SOURCE LINE 49

        if not c.started:
          wstarted = 0
        else:
          wstarted = 1
            
        
        # SOURCE LINE 54
        __M_writer(u'\n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Basic Info</h4>\n            <div class="row-fluid">\n                <div class="span12" style="padding: 19px;">\n                    <form name="edit_issue" id="edit_issue" action = "/workshop/')
        # SOURCE LINE 60
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/configureBasicWorkshopHandler" enctype="multipart/form-data" method="post" ng-cloak>\n                        <fieldset>\n                            <h4>Workshop Name</h4>\n                            <input id = "inputTitle" type="text" name="title" size="50" maxlength="100" value = "{{workshopTitle}}" ng-model = "workshopTitle" class="input-xxlarge editWorkshopName"/>\n                            <h4>Introduction</h4>\n                            <span class="muted">A one paragraph description why this matters.</span>\n                            <textarea rows="8" id = "inputDescription" name="description" size="50" class="span12 editWorkshopDescription">')
        # SOURCE LINE 66
        __M_writer(escape(c.w['description']))
        __M_writer(u'</textarea>\n                            ')
        # SOURCE LINE 67

        if 'allowIdeas' in c.w and c.w['allowIdeas'] == '1':
            yesChecked = 'checked'
            noChecked = ''
        elif 'allowIdeas' in c.w and c.w['allowIdeas'] == '0':
            yesChecked = ''
            noChecked = 'checked'
        else:
            yesChecked = 'checked'
            noChecked = ''
                                    
        
        # SOURCE LINE 77
        __M_writer(u'\n                            <h4>Can participants add ideas?</h4>\n                            <label class="radio">\n                                <input type="radio" id="allowIdeas" name="allowIdeas" value="1" ')
        # SOURCE LINE 80
        __M_writer(escape(yesChecked))
        __M_writer(u'> Yes\n                            </label>\n                            \n                            <label class="radio">\n                                <input type="radio" id="allowIdeas" name="allowIdeas" value="0" ')
        # SOURCE LINE 84
        __M_writer(escape(noChecked))
        __M_writer(u'> No\n                            </label>\n                            ')
        # SOURCE LINE 86
 
        if 'allowResources' in c.w and c.w['allowResources'] == '1':
            yesChecked = 'checked'
            noChecked = ''
        elif 'allowResources' in c.w and c.w['allowResources'] == '0':
            yesChecked = ''
            noChecked = 'checked'
        else:
            yesChecked = 'checked'
            noChecked = ''
                                    
        
        # SOURCE LINE 96
        __M_writer(u'\n                            <h4>Can participants add information resource links?</h4>\n                            <label class="radio">\n                                <input type="radio" id="allowResources" name="allowResources" value="1" ')
        # SOURCE LINE 99
        __M_writer(escape(yesChecked))
        __M_writer(u'> Yes\n                            </label>\n                            \n                            <label class="radio">\n                                <input type="radio" id="allowResources" name="allowResources" value="0" ')
        # SOURCE LINE 103
        __M_writer(escape(noChecked))
        __M_writer(u'> No\n                            </label>\n                            <br>\n\n                        <h4>Goals</h4>\n')
        # SOURCE LINE 109
        __M_writer(u'                        <p class="muted">Double-click on an existing goal to edit.</p>\n                        <div ng-controller="GoalsCtrl">\n                            <p> {{remaining()}} of {{goals.length}} remaining </p>\n                            <ul class="unstyled goalList">\n                                <li ng-repeat="goal in goals">\n                                    <span>\n                                    <input type="checkbox" ng-model="goal.done" ng-click="goalStatus(goal)" class="goal-checkbox">\n                                    <span class="goal-title done-{{goal.done}}" ng-dblclick="goalEditState(goal)" ng-hide="goal.editing">{{goal.title}}</span>\n                                    <form ng-submit="goalEditDone(goal)" class="inline">\n                                        <input type="text" ng-show="goal.editing" value="{{goal.title}}" ng-model="editTitle" maxlength="100" civ-focus="goal.editing" civ-blur="goalEditState(goal)">\n                                    </form>\n                                    <a ng-click="deleteGoal(goal)" class="inline pull-right"><img src="/images/glyphicons_pro/glyphicons/png/glyphicons_192_circle_remove.png" class="deleteGoal"></a></span>\n                                </li>\n                            </ul>\n                            <form ng-submit="addGoal()" class="addGoal">\n                                <div class="input-append">\n                                    <input type="text" ng-model="goalTitle" size="100" maxlength = "100" placeholder="New goal here" class="addGoal" id="addGoal">\n                                    <button class="btn btn-primary" type="submit" value="add">add</button>\n                                </div>\n                            </form>\n                            <p class = "green">{{100 - goalTitle.length}}</p>\n                        </div>\n\n')
        # SOURCE LINE 132
        if not c.published:
            # SOURCE LINE 133
            __M_writer(u'                            <button type="submit" class="btn btn-warning">Save Basic Info and Continue</button>\n')
            # SOURCE LINE 134
        else:
            # SOURCE LINE 135
            __M_writer(u'                            <button type="submit" class="btn btn-warning">Save Basic Info</button>\n')
            pass
        # SOURCE LINE 137
        __M_writer(u'                    </fieldset>\n                </form>\n            </div><!-- row -->\n        </div>\n        </div><!-- browse -->\n    </div><!-- section wrapper -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_scope(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def change_scope():
            return render_change_scope(context)
        def private():
            return render_private(context)
        def public():
            return render_public(context)
        __M_writer = context.writer()
        # SOURCE LINE 145
        __M_writer(u'\n    ')
        # SOURCE LINE 146

        if c.w['type'] == 'personal' or c.w['public_private'] == 'private':
            privateActive="active"
            publicActive="foo"
        else:
            privateActive="foo"
            publicActive="active"
            
        
        # SOURCE LINE 153
        __M_writer(u'\n        \n    <div class="section-wrapper">\n        <div class="browse">\n            <h4 class="section-header smaller">Participants</h4>\n            Specifiy if the workshop is public or private, and who may participate.\n            <br>\n            <br>\n             ')
        # SOURCE LINE 161
        __M_writer(escape(change_scope()))
        __M_writer(u'\n\n')
        # SOURCE LINE 163
        if c.w['public_private'] == 'private':
            # SOURCE LINE 164
            __M_writer(u'                <div class="tab-pane ')
            __M_writer(escape(privateActive))
            __M_writer(u'" id="private">')
            __M_writer(escape(private()))
            __M_writer(u'</div>\n')
            # SOURCE LINE 165
        elif c.w['public_private'] == 'public':
            # SOURCE LINE 166
            __M_writer(u'                <div class="tab-pane ')
            __M_writer(escape(publicActive))
            __M_writer(u'" id="public">')
            __M_writer(escape(public()))
            __M_writer(u'</div>\n')
            pass
        # SOURCE LINE 168
        __M_writer(u'\n        </div><!-- browse -->\n    </div><!-- section-wrapper -->              \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_public(context):
    context.caller_stack._push_frame()
    try:
        def emailInvite():
            return render_emailInvite(context)
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 361
        __M_writer(u'\n    <div class="container-fluid well">\n        <table class="boxOffsetParent">\n            <tr>\n                <td rowspan="2" class="scope-icon">\n                    <i class="icon-globe icon-4x"></i>\n                </td>\n                <td>\n                    <h4><lead>Public</lead></h4>\n                </td>\n            </tr>\n            <tr>\n                <td>\n                    <ul>\n                        <li>Public workshops are visible to everyone.</li>\n                        <li>Residents of the specified geographic area will be encouraged to participate.</li>\n                        <li>Unlimited participants.</li>\n                    </ul>\n                </td>\n            </tr>\n        </table>\n        <br>\n        <hr>\n        <strong>Geographic Area</strong><br> \n        <br>\n        <p>Specify the geographic area associated with your workshop:</p>\n        ')
        # SOURCE LINE 387
 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = getStateList("united-states")
            countyMessage = "or leave blank if your workshop is specific to the entire country."
        else:
            countrySelected = ""
        endif
                
        
        # SOURCE LINE 400
        __M_writer(u'\n        <form name="scope" id="scope" class="left" action = "/workshop/')
        # SOURCE LINE 401
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'/configurePublicWorkshopHandler" enctype="multipart/form-data" method="post" >  \n        <div class="row-fluid"><span id="planetSelect">\n            <div class="span1"></div><div class="span2">Planet:</div>\n            <div class="span9">\n                <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">\n                    <option value="0">Earth</option>\n                </select>\n            </div><!-- span9 -->\n        </span><!-- countrySelect -->\n        </div><!-- row-fluid -->     \n        <div class="row-fluid"><span id="countrySelect">\n            <div class="span1"></div><div class="span2">Country:</div>\n            <div class="span9">\n                <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">\n                    <option value="0">Select a country</option>\n                    <option value="United States" ')
        # SOURCE LINE 416
        __M_writer(escape(countrySelected))
        __M_writer(u'>United States</option>\n                </select>\n            </div><!-- span9 -->\n        </span><!-- countrySelect -->\n        </div><!-- row-fluid -->\n        <div class="row-fluid"><span id="stateSelect">\n')
        # SOURCE LINE 422
        if c.country != "0":
            # SOURCE LINE 423
            __M_writer(u'                <div class="span1"></div><div class="span2">State:</div><div class="span9">\n                <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">\n                <option value="0">Select a state</option>\n')
            # SOURCE LINE 426
            for state in states:
                # SOURCE LINE 427
                if state != 'District of Columbia':
                    # SOURCE LINE 428
                    if c.state == state['StateFullName']:
                        # SOURCE LINE 429
                        __M_writer(u'                            ')
                        stateSelected = "selected" 
                        
                        __M_writer(u'\n')
                        # SOURCE LINE 430
                    else:
                        # SOURCE LINE 431
                        __M_writer(u'                            ')
                        stateSelected = "" 
                        
                        __M_writer(u'\n')
                        pass
                    # SOURCE LINE 433
                    __M_writer(u'                        <option value="')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'" ')
                    __M_writer(escape(stateSelected))
                    __M_writer(u'>')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'</option>\n')
                    pass
                pass
            # SOURCE LINE 436
            __M_writer(u'                </select>\n                </div><!-- span9 -->\n')
            # SOURCE LINE 438
        else:
            # SOURCE LINE 439
            __M_writer(u'                or leave blank if your workshop is specific to the entire planet.\n')
            pass
        # SOURCE LINE 441
        __M_writer(u'        </span></div><!-- row-fluid -->\n        <div class="row-fluid"><span id="countySelect">\n')
        # SOURCE LINE 443
        if c.state != "0":
            # SOURCE LINE 444
            __M_writer(u'                ')
            counties = getCountyList("united-states", c.state) 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 445
            cityMessage = "or leave blank if your workshop is specific to the entire state." 
            
            __M_writer(u'\n                <div class="span1"></div><div class="span2">County:</div><div class="span9">\n                <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">\n                    <option value="0">Select a county</option>\n')
            # SOURCE LINE 449
            for county in counties:
                # SOURCE LINE 450
                if c.county == county['County'].title():
                    # SOURCE LINE 451
                    __M_writer(u'                            ')
                    countySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 452
                else:
                    # SOURCE LINE 453
                    __M_writer(u'                            ')
                    countySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 455
                __M_writer(u'                        <option value="')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'" ')
                __M_writer(escape(countySelected))
                __M_writer(u'>')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 457
            __M_writer(u'                </select>\n                </div><!-- span9 -->\n')
            # SOURCE LINE 459
        else:
            # SOURCE LINE 460
            __M_writer(u'                ')
            cityMessage = "" 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 461
            __M_writer(escape(countyMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 463
        __M_writer(u'        </span></div><!-- row -->\n        <div class="row-fluid"><span id="citySelect">\n')
        # SOURCE LINE 465
        if c.county != "0":
            # SOURCE LINE 466
            __M_writer(u'                ')
            cities = getCityList("united-states", c.state, c.county) 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 467
            postalMessage = "or leave blank if your workshop is specific to the entire county." 
            
            __M_writer(u'\n                <div class="span1"></div><div class="span2">City:</div><div class="span9">\n                <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">\n                <option value="0">Select a city</option>\n')
            # SOURCE LINE 471
            for city in cities:
                # SOURCE LINE 472
                if c.city == city['City'].title():
                    # SOURCE LINE 473
                    __M_writer(u'                            ')
                    citySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 474
                else:
                    # SOURCE LINE 475
                    __M_writer(u'                            ')
                    citySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 477
                __M_writer(u'                        <option value="')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'" ')
                __M_writer(escape(citySelected))
                __M_writer(u'>')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 479
            __M_writer(u'                </select>\n                </div><!-- span9 -->\n')
            # SOURCE LINE 481
        else:
            # SOURCE LINE 482
            __M_writer(u'                ')
            postalMessage = "" 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 483
            __M_writer(escape(cityMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 485
        __M_writer(u'            </span></div><!-- row-fluid -->\n        <div class="row-fluid"><span id="postalSelect">\n')
        # SOURCE LINE 487
        if c.city != "0":
            # SOURCE LINE 488
            __M_writer(u'                ')
            postalCodes = getPostalList("united-states", c.state, c.county, c.city) 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 489
            underPostalMessage = "or leave blank if your workshop is specific to the entire city." 
            
            __M_writer(u'\n                <div class="span1"></div><div class="span2">Postal Code:</div><div class="span9">\n                <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">\n                <option value="0">Select a postal code</option>\n')
            # SOURCE LINE 493
            for pCode in postalCodes:
                # SOURCE LINE 494
                if c.postal == str(pCode['ZipCode']):
                    # SOURCE LINE 495
                    __M_writer(u'                            ')
                    postalSelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 496
                else:
                    # SOURCE LINE 497
                    __M_writer(u'                            ')
                    postalSelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 499
                __M_writer(u'                        <option value="')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'" ')
                __M_writer(escape(postalSelected))
                __M_writer(u'>')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 501
            __M_writer(u'                </select>\n                </div><!-- span9 -->\n')
            # SOURCE LINE 503
        else:
            # SOURCE LINE 504
            __M_writer(u'                ')
            underPostalMessage = "" 
            
            __M_writer(u'\n                ')
            # SOURCE LINE 505
            __M_writer(escape(postalMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 507
        __M_writer(u'            </span></div><!-- row-fluid -->\n        <div class="row-fluid"><span id="underPostal">')
        # SOURCE LINE 508
        __M_writer(escape(underPostalMessage))
        __M_writer(u'</span><br /></div><!-- row -->\n        <br />\n        ')
        # SOURCE LINE 510
 
        buttonMsg = "Save Geographic Area"
                
        
        # SOURCE LINE 512
        __M_writer(u'\n        <div class="row-fluid">\n                <button type="submit" class="btn btn-warning">')
        # SOURCE LINE 514
        __M_writer(escape(buttonMsg))
        __M_writer(u'</button>\n        </div><!-- row -->\n        </form>\n        <hr>\n        <strong>Invite Participants</strong><br>\n        <br>\n        <span class="help-inline">Share this Link:  </span>\n        <input type="text" class="span9" value="')
        # SOURCE LINE 521
        __M_writer(escape(c.shareURL))
        __M_writer(u'"></input>\n        <br>\n        <!--\n        <br>\n        <strong>Share on Facebook; Tweet</strong>\n        <br> -->\n        <br>\n        <div class="row-fluid centered"><strong><em>OR</em></strong></div>\n        <br>\n        ')
        # SOURCE LINE 530
        __M_writer(escape(emailInvite()))
        __M_writer(u'\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_publish(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 535
        __M_writer(u'\n')
        # SOURCE LINE 536
        if not c.started and c.basicConfig and c.slideConfig and c.backConfig and c.tagConfig and c.participantsConfig:
            # SOURCE LINE 537
            __M_writer(u'        <div>\n            <form name="edit_issue" id="edit_issue" class="left form-inline no-bottom" action = "/workshop/')
            # SOURCE LINE 538
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'/configureStartWorkshopHandler" enctype="multipart/form-data" method="post" >\n            <button type="submit" class="btn btn-warning btn-block btn-large" name="startWorkshop" value="Start" >Publish Workshop</button>\n            </form>\n        </div>\n\n')
            # SOURCE LINE 543
        elif c.w['startTime'] == '0000-00-00':
            # SOURCE LINE 544
            __M_writer(u'        <button class="btn btn-warning btn-block btn-large disabled publishButton" rel="tooltip" data-placement="bottom" data-original-title="You must complete all steps before publishing your workshop">Publish Workshop</button>\n\n')
            # SOURCE LINE 546
        else:
            # SOURCE LINE 547
            __M_writer(u'        <form class="no-bottom" action="/workshop/')
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'/publish/handler" method=POST>\n')
            # SOURCE LINE 548
            if workshopLib.isPublished(c.w):
                # SOURCE LINE 549
                __M_writer(u'                <button type="submit" class="btn btn-warning btn-block btn-large publishButton" value="unpublish" rel="tooltip" data-placement="bottom" data-original-title="This will temporarily unpublish your workshop, removing it from listings and activity streams.">Unpublish Workshop</button>\n')
                # SOURCE LINE 550
            else:
                # SOURCE LINE 551
                __M_writer(u'                <button type="submit" class="btn btn-warning btn-block btn-large publishButton" value="publish" rel="tooltip" data-placement="bottom" data-original-title="Republishes your workshop, making it visible in listings and activity streams.">Publish Workshop</button>\n')
                pass
            # SOURCE LINE 553
            __M_writer(u'        </form>\n\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


