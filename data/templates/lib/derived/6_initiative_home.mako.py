# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.224514
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_initiative_home.mako'
_template_uri = u'/lib/derived/6_initiative_home.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showDescription', 'showCost', 'editInitiative', 'showAuthor', 'showBackground', 'showUpdateList', 'showResource', 'listResources', 'addResourceButton', 'showProposal', 'initiativeModerationPanel', 'listInitiative', 'editResource', 'watchButton', 'showFunding_Summary', 'editUpdate', 'coAuthorInvite', 'geoSelect']


# SOURCE LINE 1

import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.generic      as genericLib
import pylowiki.lib.utils           as utils
import misaka as m

import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

import logging
log = logging.getLogger(__name__)

from pylowiki.lib.db.geoInfo import getGeoTitles, getStateList, getCountyList, getCityList, getPostalList


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 17
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u'\n\n')
        # SOURCE LINE 17
        __M_writer(u'\n\n')
        # SOURCE LINE 86
        __M_writer(u'\n\n')
        # SOURCE LINE 97
        __M_writer(u'\n                        \n\n')
        # SOURCE LINE 104
        __M_writer(u'\n\n')
        # SOURCE LINE 110
        __M_writer(u'\n\n\n')
        # SOURCE LINE 117
        __M_writer(u'\n\n')
        # SOURCE LINE 123
        __M_writer(u'\n\n')
        # SOURCE LINE 137
        __M_writer(u'\n\n')
        # SOURCE LINE 155
        __M_writer(u'\n\n')
        # SOURCE LINE 191
        __M_writer(u'\n\n')
        # SOURCE LINE 219
        __M_writer(u'\n\n')
        # SOURCE LINE 264
        __M_writer(u'\n\n')
        # SOURCE LINE 495
        __M_writer(u'\n\n')
        # SOURCE LINE 556
        __M_writer(u'\n\n')
        # SOURCE LINE 594
        __M_writer(u'\n\n')
        # SOURCE LINE 627
        __M_writer(u'\n\n')
        # SOURCE LINE 751
        __M_writer(u'\n\n')
        # SOURCE LINE 774
        __M_writer(u'\n\n')
        # SOURCE LINE 862
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showDescription(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 100
        __M_writer(u'\n    <div class="initiative-info">\n        ')
        # SOURCE LINE 102
        __M_writer(m.html(c.initiative['description'], render_flags=m.HTML_SKIP_HTML) )
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showCost(context,item):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 753
        __M_writer(u'\n    ')
        # SOURCE LINE 754
 
        currency = '$'
        cost = int(item['cost']) 
        if cost <= -1:
            cost = cost * -1
            currency = '- $'
            
        
        # SOURCE LINE 760
        __M_writer(u'\n    <h4 class="initiative-title">\n        <div class="span6 pull-left">\n            Cost Estimate\n        </div>\n        <div class="span6">\n            <table class="pull-right">\n                <tr>\n                    <td>')
        # SOURCE LINE 768
        __M_writer(escape(currency))
        __M_writer(u'</td>\n                    <td>')
        # SOURCE LINE 769
        __M_writer(escape(locale.format("%d", cost, grouping=True)))
        __M_writer(u'</td>\n                <tr>\n            </table>\n        </div>\n    </h4>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editInitiative(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def coAuthorInvite():
            return render_coAuthorInvite(context)
        def geoSelect():
            return render_geoSelect(context)
        __M_writer = context.writer()
        # SOURCE LINE 266
        __M_writer(u'\n    ')
        # SOURCE LINE 267
 
        tagList = workshopLib.getWorkshopTagCategories()
        postalCodeSelected = ""
        citySelected = ""
        countySelected = ""
        if c.initiative:
            iScope = c.initiative['scope']
        else:
            iScope = "0|0|0|0|0|0|0|0|0|0"
        scopeList = iScope.split('|')
        if scopeList[9] == '0' and scopeList[8] == '0':
            countySelected = "selected"
        elif scopeList[9] == '0' and scopeList[8] != '0':
            citySelected = "selected"
        else:
            postalCodeSelected = "selected"
        
            
        
        # SOURCE LINE 284
        __M_writer(u'\n')
        # SOURCE LINE 285
        if c.saveMessage and c.saveMessage != '':
            # SOURCE LINE 286
            __M_writer(u'        <div class="alert ')
            __M_writer(escape(c.saveMessageClass))
            __M_writer(u'">\n        <button type="button" class="close" data-dismiss="alert">&times;</button>\n        ')
            # SOURCE LINE 288
            __M_writer(escape(c.saveMessage))
            __M_writer(u'\n        </div>\n')
            pass
        # SOURCE LINE 291
        __M_writer(u'    <div class="row-fluid edit-initiative" id="basics">\n        <div class="span12">\n        <form method="POST" name="edit_initiative_summary" id="edit_initiative_summary" action="/initiative/')
        # SOURCE LINE 293
        __M_writer(escape(c.initiative['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.initiative['url']))
        __M_writer(u'/editHandler" ng-controller="initiativeCtrl" ng-init="cost = \'')
        __M_writer(escape(c.initiative['cost']))
        __M_writer(u'\'">\n            <div class="row-fluid">\n                <h3 class="initiative-title edit no-top">1. Basics</h3>\n            </div><!-- row-fluid -->\n            <br>\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="title" class="control-label" required><strong>Initiative Title:</strong></label>\n                    <input type="text" name="title" class="span12" ng-model="initiativeTitle" value="{{initiativeTitle}}" ng-click="clearTitle()" ng-cloak>\n                </div><!-- span6 -->\n                <div class="span6">\n                    <div class="alert alert-info">\n                        Keep it short and descriptive. 10 words or less.\n                    </div><!-- alert -->\n                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="title" class="control-label" required><strong>Geographic Region:</strong></label>\n                    ')
        # SOURCE LINE 312
        __M_writer(escape(geoSelect()))
        __M_writer(u'\n                </div><!-- span6 -->\n                <div class="span6">\n                    <div class="alert alert-info">\n                        The region or legal jurisdiction associated with your initiative.\n                    </div><!-- alert -->\n                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="tag" class="control-label" required><strong>Initiative category:</strong></label>\n                    <div class="span3"></div>\n                    <div class="span8 no-left">\n                        <select name="tag" id="tag">\n')
        # SOURCE LINE 326
        if c.initiative['public'] == '0':
            # SOURCE LINE 327
            __M_writer(u'                            <option value="">Choose one</option>\n')
            pass
        # SOURCE LINE 329
        for tag in tagList:
            # SOURCE LINE 330
            __M_writer(u'                            ')
 
            selected = ""
            if c.initiative['tags'] == tag:
                selected = "selected"
                                        
            
            # SOURCE LINE 334
            __M_writer(u'\n                            <option value="')
            # SOURCE LINE 335
            __M_writer(escape(tag))
            __M_writer(u'" ')
            __M_writer(escape(selected))
            __M_writer(u'/> ')
            __M_writer(escape(tag))
            __M_writer(u'</option>\n')
            pass
        # SOURCE LINE 337
        __M_writer(u'                        </select>\n                    </div><!-- span8 -->\n                </div><!-- span6 -->\n                <div class="span6">\n                    <div class="alert alert-info">\n                        The topic area associated with your initiative.\n                    </div><!-- alert -->\n                </div><!-- span6 -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid" id="summary">\n                <h3 class="initiative-title edit">2. Summary</h3>\n            </div><!-- row-fluid -->\n            <br>\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="description" class="control-label" required><strong>Summary:</strong></label>\n                    <textarea rows="8" type="text" name="description" class="span12">')
        # SOURCE LINE 353
        __M_writer(escape(c.initiative['description']))
        __M_writer(u'</textarea>\n                </div>\n                <div class="span6">\n                    <div class="alert alert-info">\n                        Used in search listings and displayed at the top of your initiative.\n                    </div>\n                </div>\n            </div>\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="funding_summary" class="control-label" required><strong>Estimate Net Fiscal Impact:</strong></label>\n                    <textarea rows="8" type="text" name="funding_summary" class="span12">')
        # SOURCE LINE 364
        __M_writer(escape(c.initiative['funding_summary']))
        __M_writer(u'</textarea>\n                </div>\n                <div class="span6">\n                    <label class="control-label"></label>\n                    <div class="alert alert-info">\n                        What are the costs and benefits of your intiative? What will you have to spend money on? What will the fiscal impacts be for the associated region? For example, if your intiative will lead to increased tax revenues for your City, mention that here.\n                    </div>\n                </div>\n            </div>\n            <div class="row-fluid">\n                <div class="span6">\n                    <label for="description" class="control-label" required><strong>Cost Estimate:</strong></label>\n                    <div class="input-prepend input-append">\n                      <span class="add-on">$</span>\n                      <input type="text" name="cost" value="{{cost}}" ng-model="cost" ng-pattern="costRegex">\n                      <span class="add-on">.00</span>\n                    </div>\n                    <span class="error help-text" ng-show="edit_initiative_summary.cost.$error.pattern" ng-cloak>Invalid cost value</span>\n                </div>\n                <div class="span6">\n                    <label class="control-label"></label>\n                    <div class="alert alert-info">\n                        Acceptable formats include: 500,000  or  500000.\n                    </div>\n                </div>\n            </div>\n            <div class="row-fluid" id="detail">\n                <h3 class="initiative-title edit">3. Detail</h3>\n            </div><!-- row-fluid -->\n\n            <div class="row-fluid">\n                <div class="span3">\n                    <label for="background" class="control-label" required><strong>Background:</strong></label>\n                    ')
        # SOURCE LINE 397
        __M_writer(escape(lib_6.formattingGuide()))
        __M_writer(u'\n                </div>\n                <div class="span9">\n                    <div class="alert alert-info">\n                        What are the conditions that make this initaitive needed? Cite statistics and existing policies or programs in the effected region wherever possible.\n                    </div>\n                </div>\n            </div>\n            <textarea rows="10" id="background" name="background" class="span12">')
        # SOURCE LINE 405
        __M_writer(escape(c.initiative['background']))
        __M_writer(u'</textarea>\n\n            <div class="row-fluid">\n                <div class="span3">\n                    <label for="proposal" class="control-label" required><strong>Proposal:</strong></label>\n                    ')
        # SOURCE LINE 410
        __M_writer(escape(lib_6.formattingGuide()))
        __M_writer(u'\n                </div>\n                <div class="span9">\n                    <div class="alert alert-info">\n                        What are the details of your initiative? How will it work? What will it do? What won\'t it do? Address the financial impacts as well.\n                    </div>\n                </div>\n            </div>\n            <textarea rows="10" id="proposal" name="proposal" class="span12">')
        # SOURCE LINE 418
        __M_writer(escape(c.initiative['proposal']))
        __M_writer(u'</textarea>\n            <button type="submit" class="btn btn-warning btn-large pull-right" name="submit_summary">Save Changes</button>\n        </form>\n        <div class="row-fluid" id="photo">\n            <h3 class="initiative-title edit">4. Photo</h3>\n        </div><!-- row-fluid -->\n        <form id="fileupload" action="/initiative/')
        # SOURCE LINE 424
        __M_writer(escape(c.initiative['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.initiative['url']))
        __M_writer(u'/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: \'fileupload-processing\'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">\n            <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">\n                <!-- The fileinput-button span is used to style the file input field as button -->\n')
        # SOURCE LINE 427
        if 'directoryNum_photos' in c.initiative and 'pictureHash_photos' in c.initiative:
            # SOURCE LINE 428
            __M_writer(u'                    ')
            thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(c.initiative['directoryNum_photos'], c.initiative['pictureHash_photos']) 
            
            __M_writer(u'\n                    <span class="pull-left">Current Initiative Picture\n                    <div class="spacer"></div>\n                    <img src="')
            # SOURCE LINE 431
            __M_writer(escape(thumbnail_url))
            __M_writer(u'">\n                    </span>\n')
            # SOURCE LINE 433
        else:
            # SOURCE LINE 434
            __M_writer(u'                    <span class="pull-left">Upload a Picture (Required)</span>\n')
            pass
        # SOURCE LINE 436
        __M_writer(u'                <span class="btn btn-success btn-large fileinput-button pull-right"  data-toggle="collapse" data-target="#fileinput-button-div">\n                <i class="icon-plus icon-white"></i>\n                <span>Picture</span>\n                <input type="file" name="files[]">\n                </span>\n                <!-- The loading indicator is shown during file processing -->\n                <div class="fileupload-loading"></div>\n                <!-- The global progress information -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span10 offset1 fade" data-ng-class="{true: \'in\'}[!!active()]">\n                    <!-- The global progress bar -->\n                    <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + \'%\'}"></div></div>\n                    <!-- The extended global progress information -->\n                    <div class="progress-extended">&nbsp;</div>\n                </div><!-- span10 -->\n            </div><!-- row-fluid -->\n            <!-- The table listing the files available for upload/download -->\n            <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">\n                <tbody><tr data-ng-repeat="file in queue">\n                    <td data-ng-switch="" on="!!file.thumbnail_url">\n                        <div class="preview" data-ng-switch-when="true">\n                            <script type="text/javascript">\n                                function setAction(imageHash) {\n                                    actionURL = "/profile/')
        # SOURCE LINE 460
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'/photo/" + imageHash + "/update/handler";\n                                    document.getElementById(\'fileupload\').action = actionURL;\n                                }\n                            </script>\n                            <div class="row-fluid">\n                                <img src="{{file.thumbnail_url}}">\n                                New Picture Uploaded and Saved\n                                <a href="/initiative/')
        # SOURCE LINE 467
        __M_writer(escape(c.initiative['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.initiative['url']))
        __M_writer(u'/editHandler" class="btn btn-warning btn-large pull-right" name="submit_photo">Save Changes</a>\n                            </div><!-- row-fluid -->\n                            </form>\n\n                        </div><!-- preview -->\n                        <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>\n                            </td>\n                            <td>\n                                <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>\n                            </td>\n                            <td>\n                                <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">\n                                <i class="icon-upload icon-white"></i>\n                                <span>Save</span>\n                                </button>\n                                <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">\n                                <i class="icon-ban-circle icon-white"></i>\n                                <span>Cancel</span>\n                                </button>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </form>\n\n        ')
        # SOURCE LINE 492
        __M_writer(escape(coAuthorInvite()))
        __M_writer(u'\n    </div><!-- span12 -->\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showAuthor(context,item):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 19
        __M_writer(u'\n    <div class="tabbable">\n        <div class="tab-content">\n            <div class="tab-pane active" id="abrv">\n                <table>\n                    <tr>\n                        ')
        # SOURCE LINE 25

        showNum = 3
        remaining = len(c.authors) - showNum
                                
        
        # SOURCE LINE 28
        __M_writer(u'\n')
        # SOURCE LINE 29
        for author in c.authors[:showNum]:
            # SOURCE LINE 30
            __M_writer(u'                            <td>\n                                ')
            # SOURCE LINE 31
            __M_writer(escape(lib_6.userImage(author, className="avatar small-avatar")))
            __M_writer(u'\n                            </td>\n')
            pass
        # SOURCE LINE 34
        __M_writer(u'                        <td>\n                            <span class="grey">Authored by\n')
        # SOURCE LINE 36
        for author in c.authors[:showNum]:
            # SOURCE LINE 37
            if author != c.authors[0] and len(c.authors) >= 3:
                # SOURCE LINE 38
                __M_writer(u'                                    ,\n')
                pass
            # SOURCE LINE 40
            if author == c.authors[-1]:
                # SOURCE LINE 41
                __M_writer(u'                                    and\n')
                pass
            # SOURCE LINE 43
            __M_writer(u'                                ')
            __M_writer(escape(lib_6.userLink(author)))
            __M_writer(u'\n                                ')
            # SOURCE LINE 44
            __M_writer(escape(lib_6.userGreetingMsg(author)))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 46
        if remaining >= 1:
            # SOURCE LINE 47
            __M_writer(u'                                , and <a href="#allAuthors" data-toggle="tab">')
            __M_writer(escape(remaining))
            __M_writer(u' more.</a>\n')
            pass
        # SOURCE LINE 49
        __M_writer(u'                            </span>\n                        </td>\n                    </tr>\n                </table>\n            </div>\n            <div class="tab-pane" id="allAuthors">\n                <span class="pull-right">\n                    <a href="#abrv" data-toggle="tab">close</a>\n                </span>\n                <h4 class="initiative-title">\n                    Authors\n                </h4>\n                <table>\n')
        # SOURCE LINE 62
        for author in c.authors:
            # SOURCE LINE 63
            __M_writer(u'                        <tr>\n                            <td>\n                                ')
            # SOURCE LINE 65
            __M_writer(escape(lib_6.userImage(author, className="avatar small-avatar")))
            __M_writer(u'\n                            </td>\n                            <td>\n                                <span class="grey">\n                                    ')
            # SOURCE LINE 69
            __M_writer(escape(lib_6.userLink(author)))
            __M_writer(u'\n                                    ')
            # SOURCE LINE 70
            __M_writer(escape(lib_6.userGreetingMsg(author)))
            __M_writer(u'\n                                </span>\n                            </td>\n                        </tr>\n')
            pass
        # SOURCE LINE 75
        __M_writer(u'                </table>            \n            </div><!-- tab-pane -->\n        </div><!-- tabcontent -->\n    </div><!-- tabbable -->\n    ')
        # SOURCE LINE 79

        if 'views' in item:
            numViews = str(item['views'])
        else:
            numViews = "0"
            
        
        # SOURCE LINE 84
        __M_writer(u'\n    Published on ')
        # SOURCE LINE 85
        __M_writer(escape(item.date))
        __M_writer(u' <i class="icon-eye-open"></i> Views ')
        __M_writer(escape(numViews))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showBackground(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 113
        __M_writer(u'\n    <div class="initiative-info">\n        ')
        # SOURCE LINE 115
        __M_writer(m.html(c.initiative['background'], render_flags=m.HTML_SKIP_HTML) )
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showUpdateList(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 88
        __M_writer(u'\n')
        # SOURCE LINE 89
        if c.updates:
            # SOURCE LINE 90
            __M_writer(u'        Progress Reports:<br />\n        <ul>\n')
            # SOURCE LINE 92
            for update in c.updates:
                # SOURCE LINE 93
                __M_writer(u'            <li><a href="/initiative/')
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['url']))
                __M_writer(u'/updateShow/')
                __M_writer(escape(update['urlCode']))
                __M_writer(u'">')
                __M_writer(escape(update.date))
                __M_writer(u' ')
                __M_writer(escape(update['title']))
                __M_writer(u'</a></li>\n')
                pass
            # SOURCE LINE 95
            __M_writer(u'        </ul>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showResource(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 193
        __M_writer(u'\n        ')
        # SOURCE LINE 194
 
        link = ""
        rURL = "/initiative/" + c.initiative['urlCode'] + "/" + c.initiative['url'] + "/resource/" + c.thing['urlCode'] + "/" + c.thing['url']
        title = '<a href="%s" class="listed-item-title">%s</a>' %(rURL, c.thing['title'])
        if c.thing.objType == 'resource':
                link = '<small>(<a href=%s target=_blank>%s</a>)</small>' %(c.thing['link'], lib_6.ellipsisIZE(c.thing['link'], 75))
                if c.thing['type'] == 'rich' or c.thing['type'] == 'video':
                    link = link + '<div class="spacer"></div>' + c.thing['info']
                if c.thing['type'] == 'photo':
                    link = link + '<div class="spacer"></div><img src="' + c.thing['info'] + '">'
                
        
        # SOURCE LINE 204
        __M_writer(u'\n        <h4>')
        # SOURCE LINE 205
        __M_writer(title )
        __M_writer(u'</h4>\n        ')
        # SOURCE LINE 206
        __M_writer(link )
        __M_writer(u'\n        ')
        # SOURCE LINE 207
        __M_writer(m.html(c.thing['text']) )
        __M_writer(u'\n')
        # SOURCE LINE 208
        if c.revisions:
            # SOURCE LINE 209
            __M_writer(u'            <div class="spacer"></div>\n            <ul class="unstyled">\n')
            # SOURCE LINE 211
            for revision in c.revisions:
                # SOURCE LINE 212
                __M_writer(u'                <li>Revision: <a href="/initiative/')
                __M_writer(escape(revision['initiativeCode']))
                __M_writer(u'/')
                __M_writer(escape(revision['initiative_url']))
                __M_writer(u'/resource/')
                __M_writer(escape(revision['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(revision['url']))
                __M_writer(u'">')
                __M_writer(escape(revision.date))
                __M_writer(u'</a></li>\n')
                pass
            # SOURCE LINE 214
            __M_writer(u'            </ul>\n')
            pass
        # SOURCE LINE 216
        if c.thing.objType == 'revision':
            # SOURCE LINE 217
            __M_writer(u'            This is a revision dated ')
            __M_writer(escape(c.thing.date))
            __M_writer(u'<br />\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_listResources(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        len = context.get('len', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 157
        __M_writer(u'\n')
        # SOURCE LINE 158
        if len(c.resources) <= 0:
            # SOURCE LINE 159
            __M_writer(u'        <div class="alert alert-info">\n            There are no resources yet! Be the first to add one.\n        </div>\n')
            # SOURCE LINE 162
        else:
            # SOURCE LINE 163
            for item in c.resources:
                # SOURCE LINE 164
                __M_writer(u'            ')
 
                iconClass = ""
                if item['type'] == 'link' or item['type'] == 'general':
                    iconClass="icon-link"
                elif item['type'] == 'photo':
                    iconClass="icon-picture"
                elif item['type'] == 'video':
                    iconClass="icon-youtube-play"
                elif item['type'] == 'rich':
                    iconClass="icon-file"
                endif
                rURL = "/initiative/" + c.initiative['urlCode'] + "/" + c.initiative['url'] + "/resource/" + item['urlCode'] + "/" + item['url']
                            
                
                # SOURCE LINE 176
                __M_writer(u'\n            <div class="row-fluid bottom-space-med">\n                <div class="span1">\n                        <i class="')
                # SOURCE LINE 179
                __M_writer(escape(iconClass))
                __M_writer(u' icon-3x"></i>\n                </div><!-- span1 -->\n                <div class="span11">\n                    <h5 class="no-bottom no-top">\n                    ')
                # SOURCE LINE 183
                itemTitle = '<a href="%s" class="listed-item-title">%s</a>' %(rURL, lib_6.ellipsisIZE(item['title'], 150)) 
                
                __M_writer(u'\n                    ')
                # SOURCE LINE 184
                __M_writer(itemTitle )
                __M_writer(u'\n                    </h5>\n                    <a href="')
                # SOURCE LINE 186
                __M_writer(escape(item['link']))
                __M_writer(u'" target="_blank">')
                __M_writer(escape(lib_6.ellipsisIZE(item['link'], 150)))
                __M_writer(u'</a>\n                </div><!-- span10 -->\n            </div><!-- row-fluid -->\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addResourceButton(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 139
        __M_writer(u'\n    ')
        # SOURCE LINE 140
 
        printStr = ''
        if c.initiative.objType == 'initiative':
            if 'user' in session:
                printStr = '<a id="addButton" href="/initiative/%s/%s/resourceEdit/new"' %(c.initiative['urlCode'], c.initiative['url'])
            elif not c.privs['provisional']:
                printStr = '<a href="#signupLoginModal" data-toggle="modal"'
        
            printStr += ' title="Click to add a resource to this initiative" class="btn btn-success btn-mini pull-right right-space"><i class="icon icon-plus"></i></a>'
            
            if 'user' in session and c.privs['provisional']:
                printStr = ''
        
            
        
        # SOURCE LINE 153
        __M_writer(u'\n    ')
        # SOURCE LINE 154
        __M_writer(printStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showProposal(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 119
        __M_writer(u'\n    <div class="initiative-info">\n        ')
        # SOURCE LINE 121
        __M_writer(m.html(c.initiative['proposal'], render_flags=m.HTML_SKIP_HTML) )
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_initiativeModerationPanel(context,thing):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 497
        __M_writer(u'\n    ')
        # SOURCE LINE 498

        if 'user' not in session or thing.objType == 'revision' or c.privs['provisional']:
            return
        flagID = 'flag-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
            
        
        # SOURCE LINE 505
        __M_writer(u'\n    <div class="btn-group">\n')
        # SOURCE LINE 507
        if thing['disabled'] == '0' and thing.objType != 'initiativeUnpublished':
            # SOURCE LINE 508
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(flagID))
            __M_writer(u'">flag</a>\n')
            pass
        # SOURCE LINE 510
        if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'initiativeUnpublished':
            # SOURCE LINE 511
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(unpublishID))
            __M_writer(u'">unpublish</a>\n')
            # SOURCE LINE 512
        elif thing.objType == 'initiativeUnpublished' and thing['unpublished_by'] != 'parent':
            # SOURCE LINE 513
            if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 514
                __M_writer(u'                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(publishID))
                __M_writer(u'">publish</a>\n')
                # SOURCE LINE 515
            elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                # SOURCE LINE 516
                __M_writer(u'                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(publishID))
                __M_writer(u'">publish</a>\n')
                pass
            pass
        # SOURCE LINE 519
        if c.revisions:
            # SOURCE LINE 520
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#revisions">revisions (')
            __M_writer(escape(len(c.revisions)))
            __M_writer(u')</a>\n')
            pass
        # SOURCE LINE 522
        __M_writer(u'\n')
        # SOURCE LINE 523
        if userLib.isAdmin(c.authuser.id):
            # SOURCE LINE 524
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(adminID))
            __M_writer(u'">admin</a>\n')
            pass
        # SOURCE LINE 526
        __M_writer(u'    </div>\n    \n')
        # SOURCE LINE 528
        if thing['disabled'] == '0':
            # SOURCE LINE 529
            if thing.objType != 'initiativeUnpublished':
                # SOURCE LINE 530
                __M_writer(u'            ')
                __M_writer(escape(lib_6.flagThing(thing)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 532
            if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
                # SOURCE LINE 533
                if thing.objType == 'initiativeUnpublished':
                    # SOURCE LINE 534
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.publishThing(thing)))
                    __M_writer(u'\n')
                    # SOURCE LINE 535
                else:
                    # SOURCE LINE 536
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.unpublishThing(thing)))
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 538
                if userLib.isAdmin(c.authuser.id):
                    # SOURCE LINE 539
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.adminThing(thing)))
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 542
        else:
            # SOURCE LINE 543
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 544
                __M_writer(u'            ')
                __M_writer(escape(lib_6.adminThing(thing)))
                __M_writer(u'\n')
                pass
            pass
        # SOURCE LINE 547
        if c.revisions:
            # SOURCE LINE 548
            __M_writer(u'        <div id="revisions" class="collapse">\n            <ul class="unstyled">\n')
            # SOURCE LINE 550
            for revision in c.revisions:
                # SOURCE LINE 551
                __M_writer(u'                <li>Revision: <a href="/initiative/')
                __M_writer(escape(revision['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(revision['url']))
                __M_writer(u'/show">')
                __M_writer(escape(revision.date))
                __M_writer(u'</a></li>\n')
                pass
            # SOURCE LINE 553
            __M_writer(u'            </ul>\n        </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_listInitiative(context,item,ltitle):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        def watchButton(i,**kwargs):
            return render_watchButton(context,i,**kwargs)
        __M_writer = context.writer()
        # SOURCE LINE 221
        __M_writer(u'\n    <div class="media profile-workshop">\n        <a class="pull-left" href="/initiative/')
        # SOURCE LINE 223
        __M_writer(escape(item['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(item['url']))
        __M_writer(u'/show">\n')
        # SOURCE LINE 224
        if 'directoryNum_photos' in item and 'pictureHash_photos' in item:
            # SOURCE LINE 225
            __M_writer(u'            ')
            thumbnail_url = "/images/photos/%s/thumbnail/%s.png"%(item['directoryNum_photos'], item['pictureHash_photos']) 
            
            __M_writer(u'\n')
            # SOURCE LINE 226
        else:
            # SOURCE LINE 227
            __M_writer(u'            ')
            thumbnail_url = "/images/icons/generalInitiative.jpg" 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 229
        __M_writer(u'        <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(')
        __M_writer(escape(thumbnail_url))
        __M_writer(u'); background-size: cover; background-position: center center;"></div>\n        </a>\n        <div class="media-body">\n            <div class="span10">\n                <a href="/initiative/')
        # SOURCE LINE 233
        __M_writer(escape(item['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(item['url']))
        __M_writer(u'/show" class="listed-item-title media-heading lead bookmark-title">')
        __M_writer(escape(item['title']))
        __M_writer(u'</a>\n                <br>\n                <span class="grey">Initiative for</span> ')
        # SOURCE LINE 235
        __M_writer(lib_6.showScope(item) )
        __M_writer(u'\n')
        # SOURCE LINE 236
        if 'user' in session:
            # SOURCE LINE 237
            if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 238
                if item['public'] == '0':
                    # SOURCE LINE 239
                    __M_writer(u'                            <span class="badge badge-warning">Not yet public</span>\n')
                    # SOURCE LINE 240
                else:
                    # SOURCE LINE 241
                    __M_writer(u'                            <span class="badge badge-success">Public</span>\n')
                    pass
                pass
            pass
        # SOURCE LINE 245
        __M_writer(u'            </div>\n')
        # SOURCE LINE 246
        if ltitle == 'Bookmarked':
            # SOURCE LINE 247
            __M_writer(u'                <span>\n                  ')
            # SOURCE LINE 248
            __M_writer(escape(watchButton(item, following = True)))
            __M_writer(u'\n                </span>\n')
            # SOURCE LINE 250
        else:
            # SOURCE LINE 251
            if 'user' in session:
                # SOURCE LINE 252
                if c.user.id == c.authuser.id or userLib.isAdmin(c.authuser.id):
                    # SOURCE LINE 253
                    __M_writer(u'                        <div class="row-fluid" ng-controller="followerController">\n                            <div class="span9"></div>\n                            <div class="span3">\n                                <a class="btn pull-right" href="/initiative/')
                    # SOURCE LINE 256
                    __M_writer(escape(item['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(item['url']))
                    __M_writer(u'/edit"><strong>Edit Initiative</strong></a> &nbsp;\n                            </div><!-- span3 -->\n                        </div><!-- row-fluid -->\n')
                    pass
                pass
            pass
        # SOURCE LINE 262
        __M_writer(u'        </div><!-- media-body -->\n    </div><!-- media -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editResource(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 558
        __M_writer(u'\n    ')
        # SOURCE LINE 559

        if not c.resource:
            resourceTitle = ""
            resourceLink = ""
            resourceText = ""
        else:
            resourceTitle = c.resource['title']
            resourceLink = c.resource['link']
            resourceText = c.resource['text']
            
            
        
        # SOURCE LINE 569
        __M_writer(u'\n')
        # SOURCE LINE 570
        if not c.resource:
            # SOURCE LINE 571
            __M_writer(u'        <form ng-controller="resourceController" ng-init="rType = \'initiative\'; parentCode = \'')
            __M_writer(escape(c.initiative['urlCode']))
            __M_writer(u"'; parentURL = '")
            __M_writer(escape(c.initiative['url']))
            __M_writer(u'\'; addResourceURLResponse=\'\'; addResourceResponse=\'\';"  id="addResourceForm" name="addResourceForm" ng-submit="submitResourceForm(addResourceForm)">\n            <fieldset>\n                <label>Resource title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>\n                <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>\n                <span ng-show="addResourceTitleShow"><div class="alert alert-danger" ng-cloak>{{addResourceTitleResponse}}</div></span>\n            </fieldset>\n            <fieldset>\n                <label>Resource URL</label>\n                <input type="url" class="input-block-level" name="link" ng-model="link" placeholder="http://" required>\n                <span ng-show="addResourceURLShow"><div class="alert alert-danger" ng-cloak>{{addResourceURLResponse}}</div></span>\n            </fieldset>\n            <fieldset>\n                <label><strong>Additional information</strong><br>\n                <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>\n                <textarea name="text" rows="3" class="input-block-level" ng-model="text"></textarea>\n                <span class="help-block"> (Any additional information you want to include.  This is optional.) </span>\n            </fieldset>\n            <span ng-show="addResourceShow">{{addResourceResponse}}</span>\n            <fieldset>\n                <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>\n            </fieldset>\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_watchButton(context,i,**kwargs):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 125
        __M_writer(u'\n')
        # SOURCE LINE 126
        if 'user' in session and not c.privs['provisional']:
            # SOURCE LINE 127
            if c.isFollowing or 'following' in kwargs:
                # SOURCE LINE 128
                __M_writer(u'            <button class="btn btn-civ pull-right followButton following" data-URL-list="initiative_')
                __M_writer(escape(i['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(i['url']))
                __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="this initiative" id="initiativeBookmark">\n            <span><i class="icon-bookmark btn-height icon-light"></i><strong> Bookmarked </strong></span>\n            </button>\n')
                # SOURCE LINE 131
            else:
                # SOURCE LINE 132
                __M_writer(u'            <button class="btn pull-right followButton" data-URL-list="initiative_')
                __M_writer(escape(i['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(i['url']))
                __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="this initiative" id="initiativeBookmark">\n             <span><i class="icon-bookmark med-green"></i><strong> Bookmark </strong></span>\n            </button>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showFunding_Summary(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 106
        __M_writer(u'\n    <div class="initiative-info">\n        ')
        # SOURCE LINE 108
        __M_writer(m.html(c.initiative['funding_summary'], render_flags=m.HTML_SKIP_HTML) )
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editUpdate(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 596
        __M_writer(u'\n    ')
        # SOURCE LINE 597

        if not c.update:
            updateTitle = ""
            updateText = ""
            updateCode = "new"
        else:
            updateTitle = c.update['title']
            updateText = c.update['text']
            updateCode = c.update['urlCode']
            
            
        
        # SOURCE LINE 607
        __M_writer(u'\n')
        # SOURCE LINE 608
        if not c.update:
            # SOURCE LINE 609
            __M_writer(u'        <form ng-controller="updateController" ng-init="parentCode = \'')
            __M_writer(escape(c.initiative['urlCode']))
            __M_writer(u"'; parentURL = '")
            __M_writer(escape(c.initiative['url']))
            __M_writer(u"'; updateCode = '")
            __M_writer(escape(updateCode))
            __M_writer(u'\'; addUpdateTitleResponse=\'\'; addUpdateTextResponse=\'\'; addUpdateResponse=\'\';"  id="addUpdateForm" name="addUpdateForm" ng-submit="submitUpdateForm(addUpdateForm)">\n            <fieldset>\n                <label>Progress Report Title</label><span class="help-block"> (Try to keep your title informative, but concise.) </span>\n                <input type="text" class="input-block-level" name="title" ng-model="title" maxlength = "120" required>\n                <span ng-show="addUpdateTitleShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTitleResponse}}</div></span>\n            </fieldset>\n            <fieldset>\n                <label><strong>Progress Report Text</strong>\n                <a href="#" class="btn btn-mini btn-info" onclick="window.open(\'/help/markdown.html\',\'popUpWindow\',\'height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes\');"><i class="icon-list"></i> <i class="icon-photo"></i> View Formatting Guide</a></label>\n                <textarea name="text" rows="3" class="input-block-level" ng-model="text" required></textarea>\n                <span ng-show="addUpdateTextShow"><div class="alert alert-danger" ng-cloak>{{addUpdateTextResponse}}</div></span>\n                <span class="help-block"> (A description of the progress made on implementing the initiative since the last progress report.) </span>\n            </fieldset>\n            <fieldset>\n                <button class="btn btn-large btn-civ pull-right" type="submit" name="submit">Submit</button>\n            </fieldset>\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_coAuthorInvite(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 776
        __M_writer(u'\n    <div class="row-fluid" id="coauthors">\n        <h3 class="initiative-title edit">5. Coauthors</h3>\n    </div><!-- row-fluid -->\n    <strong>Invite CoAuthors:</strong>\n')
        # SOURCE LINE 781
        if 'user' in session and c.authuser:
            # SOURCE LINE 782
            __M_writer(u'        <div ng-init="urlCode = \'')
            __M_writer(escape(c.initiative['urlCode']))
            __M_writer(u"'; url = '")
            __M_writer(escape(c.initiative['url']))
            __M_writer(u"'; authuserCode = '")
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'\'">\n            <div ng-controller="userLookupCtrl">\n                <div class="row-fluid">\n                    <form ng-submit="lookup()">\n                        <div class="input-append">\n                          <input type="text" ng-submit="lookup()" name="userValue" ng-model="userValue" placeholder="Type a user\'s name...">\n                          <button type="submit" class="btn"><i class="icon-search"></i></button>\n                        </div>\n                    </form>\n                        <table class="table-striped full-width" ng-cloak>\n                            <tr ng-repeat="user in users | limitTo:10">\n                                <td>\n                                    <a href="/profile/{{user.urlCode}}/{{user.url}}">\n                                        <img class="media-object avatar med-avatar" ng-src="{{user.photo}}" alt="{{user.name}}" title="{{user.name}}">\n                                    </a>\n                                </td>\n                                <td class="span8 grey"><a class="green green-hover" href="/profile/{{user.urlCode}}/{{user.url}}">{{user.name}}</a> from <a href="{{user.cityURL}}">{{user.cityTitle}}</a>, <a href="{{user.stateURL}}">{{user.stateTitle}}</a></td>\n                                <td>\n                                    <button ng-click="submitInvite(user.urlCode)" class="btn btn-primary pull-right">Invite to Coauthor</button>\n                                </td>\n                            </tr>\n                        </table>\n                </div><!-- row-fluid -->\n                <div ng-if="alertMsg != \'\'" class="alert alert-{{alertType}} {{alertDisplay}}" ng-cloak>\n                    <button type="button" class="close" ng-click="hideShowAlert()">&times;</button>\n                    {{alertMsg}}\n                </div>\n                <br>\n                <strong>Author and Coauthors:</strong>\n                <!-- \n                <div class="centered" ng-show="loading" ng-cloak>\n                    <i class="icon-spinner icon-spin icon-4x" style="color: #333333"></i>\n                </div>\n                <div class="row-fluid" ng-show="!loading"> -->\n                    <table class="table-striped full-width" ng-cloak>\n                        <tr>\n                            <td>\n                                ')
            # SOURCE LINE 819
            __M_writer(escape(lib_6.userImage(c.user, className="avatar med-avatar")))
            __M_writer(u'\n                            </td>\n                            <td>\n                                <a class="green green-hover" href="/profile/')
            # SOURCE LINE 822
            __M_writer(escape(c.user['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.user['url']))
            __M_writer(u'">')
            __M_writer(escape(c.user['name']))
            __M_writer(u'</a>\n                                <span class="grey">from <a href="')
            # SOURCE LINE 823
            __M_writer(escape(c.authorGeo['cityURL']))
            __M_writer(u'" class="orange oreange-hover">')
            __M_writer(escape(c.authorGeo['cityTitle']))
            __M_writer(u'</a>, <a href="')
            __M_writer(escape(c.authorGeo['stateURL']))
            __M_writer(u'" class="orange orange-hover">')
            __M_writer(escape(c.authorGeo['stateTitle']))
            __M_writer(u'</a></span>\n                            </td>\n                            <td>\n                                <span class="badge badge-inverse">Original Author</span>\n                            </td>\n                            <td></td>\n                            <td></td>\n                        </tr>\n                        <tr ng-repeat="a in authors">\n                            <td>\n                                <a class="pull-left" href="/profile/{{a.urlCode}}/{{a.url}}">\n                                    <img class="media-object avatar med-avatar" ng-src="{{a.photo}}" alt="{{a.name}}" title="{{a.name}}">\n                                </a>\n                            </td>\n                            <td>\n                                <a class="green green-hover" href="/profile/{{a.urlCode}}/{{a.url}}">{{a.name}}</a>\n                                <span class="grey">from <a href="{{a.cityURL}}" class="orange oreange-hover">{{a.cityTitle}}</a>, <a href="{{a.stateURL}}" class="orange orange-hover">{{a.stateTitle}}</a></span>\n                            </td>\n                            <td>\n                                <span ng-if="a.pending == \'1\'"  class="badge badge-info">Invitation Pending</span>\n                            </td>\n                            <td>\n                                <button type="button" ng-if="a.pending == \'1\'" ng-click="resendInvite(a.urlCode)" class="btn btn-primary pull-right">Resend Invite</button>\n                            </td>\n                            <td ng-if="a.urlCode != authuserCode">\n                                <button type="button" ng-click="removeCoA(a.urlCode)" class="btn btn-danger pull-right">Remove</button>\n                            </td>\n                            <td ng-if="a.urlCode == authuserCode">\n                                <form class="no-bottom" action="/initiative/')
            # SOURCE LINE 851
            __M_writer(escape(c.initiative['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.initiative['url']))
            __M_writer(u'/{{a.urlCode}}/facilitate/resign/handler" ng-cloak>\n                                    <input type="hidden" name="resign" value="resign">\n                                    <button type="submit" class="btn btn-danger pull-right">Resign</button>\n                                </form>\n                            </td>\n                        </tr>\n                    </table>\n                <!-- ng-loading </div> -->\n            </div><!-- ng-controller -->\n        </div><!-- ng-init -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_geoSelect(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 629
        __M_writer(u"\n    <!-- need to get the c.initiative['scope'] and update the selects accordingly -->\n    ")
        # SOURCE LINE 631
 
        countrySelected = ""
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
        if c.country!= "0":
            countrySelected = "selected"
            states = c.states
            countyMessage = "Leave 'State' blank if your initiative applies to the entire country."
        endif
            
        
        # SOURCE LINE 642
        __M_writer(u'\n    <div class="row-fluid"><span id="planetSelect">\n        <div class="span3">Planet:</div>\n        <div class="span8">\n            <select name="geoTagPlanet" id="geoTagPlanet" class="geoTagCountry">\n                <option value="0">Earth</option>\n            </select>\n        </div><!-- span8 -->\n    </span><!-- countrySelect -->\n    </div><!-- row-fluid -->     \n    <div class="row-fluid"><span id="countrySelect">\n        <div class="span3">Country:</div>\n        <div class="span8">\n            <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry">\n                <option value="0">Select a country</option>\n                <option value="United States" ')
        # SOURCE LINE 657
        __M_writer(escape(countrySelected))
        __M_writer(u'>United States</option>\n            </select>\n        </div><!-- span8 -->\n    </span><!-- countrySelect -->\n    </div><!-- row-fluid -->\n    <div class="row-fluid"><span id="stateSelect">\n')
        # SOURCE LINE 663
        if c.country != "0":
            # SOURCE LINE 664
            __M_writer(u'            <div class="span3">State:</div><div class="span8">\n            <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">\n            <option value="0">Select a state</option>\n')
            # SOURCE LINE 667
            for state in states:
                # SOURCE LINE 668
                if state != 'District of Columbia':
                    # SOURCE LINE 669
                    if c.state == state['StateFullName']:
                        # SOURCE LINE 670
                        __M_writer(u'                        ')
                        stateSelected = "selected" 
                        
                        __M_writer(u'\n')
                        # SOURCE LINE 671
                    else:
                        # SOURCE LINE 672
                        __M_writer(u'                        ')
                        stateSelected = "" 
                        
                        __M_writer(u'\n')
                        pass
                    # SOURCE LINE 674
                    __M_writer(u'                    <option value="')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'" ')
                    __M_writer(escape(stateSelected))
                    __M_writer(u'>')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'</option>\n')
                    pass
                pass
            # SOURCE LINE 677
            __M_writer(u'            </select>\n            </div><!-- span8 -->\n')
            # SOURCE LINE 679
        else:
            # SOURCE LINE 680
            __M_writer(u"            Leave 'Country' blank if your initiative applies to the entire planet.\n")
            pass
        # SOURCE LINE 682
        __M_writer(u'    </span></div><!-- row-fluid -->\n    <div class="row-fluid"><span id="countySelect">\n')
        # SOURCE LINE 684
        if c.state != "0":
            # SOURCE LINE 685
            __M_writer(u'            ')
            counties = getCountyList("united-states", c.state) 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 686
            cityMessage = "Leave blank 'County' blank if your initiative applies to the entire state." 
            
            __M_writer(u'\n            <div class="span3">County:</div><div class="span8">\n            <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">\n                <option value="0">Select a county</option>\n')
            # SOURCE LINE 690
            for county in counties:
                # SOURCE LINE 691
                if c.county == county['County'].title():
                    # SOURCE LINE 692
                    __M_writer(u'                        ')
                    countySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 693
                else:
                    # SOURCE LINE 694
                    __M_writer(u'                        ')
                    countySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 696
                __M_writer(u'                    <option value="')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'" ')
                __M_writer(escape(countySelected))
                __M_writer(u'>')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 698
            __M_writer(u'            </select>\n            </div><!-- span8 -->\n')
            # SOURCE LINE 700
        else:
            # SOURCE LINE 701
            __M_writer(u'            ')
            cityMessage = "" 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 702
            __M_writer(escape(countyMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 704
        __M_writer(u'    </span></div><!-- row -->\n    <div class="row-fluid"><span id="citySelect">\n')
        # SOURCE LINE 706
        if c.county != "0":
            # SOURCE LINE 707
            __M_writer(u'            ')
            cities = getCityList("united-states", c.state, c.county) 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 708
            postalMessage = "Leave 'City' blank if your initiative applies to the entire county." 
            
            __M_writer(u'\n            <div class="span3">City:</div><div class="span8">\n            <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">\n            <option value="0">Select a city</option>\n')
            # SOURCE LINE 712
            for city in cities:
                # SOURCE LINE 713
                if c.city == city['City'].title():
                    # SOURCE LINE 714
                    __M_writer(u'                        ')
                    citySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 715
                else:
                    # SOURCE LINE 716
                    __M_writer(u'                        ')
                    citySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 718
                __M_writer(u'                    <option value="')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'" ')
                __M_writer(escape(citySelected))
                __M_writer(u'>')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 720
            __M_writer(u'            </select>\n            </div><!-- span8 -->\n')
            # SOURCE LINE 722
        else:
            # SOURCE LINE 723
            __M_writer(u'            ')
            postalMessage = "" 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 724
            __M_writer(escape(cityMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 726
        __M_writer(u'        </span></div><!-- row-fluid -->\n    <div class="row-fluid"><span id="postalSelect">\n')
        # SOURCE LINE 728
        if c.city != "0":
            # SOURCE LINE 729
            __M_writer(u'            ')
            postalCodes = getPostalList("united-states", c.state, c.county, c.city) 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 730
            underPostalMessage = "or leave blank if your initiative is specific to the entire city." 
            
            __M_writer(u'\n            <div class="span3">Zip Code:</div><div class="span8">\n            <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal" onChange="geoTagPostalChange(); return 1;">\n            <option value="0">Select a zip code</option>\n')
            # SOURCE LINE 734
            for pCode in postalCodes:
                # SOURCE LINE 735
                if c.postal == str(pCode['ZipCode']):
                    # SOURCE LINE 736
                    __M_writer(u'                        ')
                    postalSelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 737
                else:
                    # SOURCE LINE 738
                    __M_writer(u'                        ')
                    postalSelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 740
                __M_writer(u'                    <option value="')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'" ')
                __M_writer(escape(postalSelected))
                __M_writer(u'>')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 742
            __M_writer(u'            </select>\n            </div><!-- span8 -->\n')
            # SOURCE LINE 744
        else:
            # SOURCE LINE 745
            __M_writer(u'            ')
            underPostalMessage = "" 
            
            __M_writer(u'\n            ')
            # SOURCE LINE 746
            __M_writer(escape(postalMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 748
        __M_writer(u'        </span></div><!-- row-fluid -->\n    <div class="row-fluid"><span id="underPostal">')
        # SOURCE LINE 749
        __M_writer(escape(underPostalMessage))
        __M_writer(u'</span><br /></div><!-- row -->\n    <br/>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


