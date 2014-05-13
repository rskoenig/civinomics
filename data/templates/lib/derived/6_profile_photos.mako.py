# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398540607.353271
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_profile_photos.mako'
_template_uri = u'/lib/derived/6_profile_photos.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['editPhoto', 'photoModerationPanel', 'showPhoto', 'uploadPhoto']


# SOURCE LINE 1

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.db.photo        as photoLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.geoInfo      as geoLib


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 14
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 14
        __M_writer(u'\n\n')
        # SOURCE LINE 169
        __M_writer(u'\n\n')
        # SOURCE LINE 232
        __M_writer(u'\n\n')
        # SOURCE LINE 313
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_editPhoto(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="span8">\n')
        # SOURCE LINE 19
        if not c.photo:
            # SOURCE LINE 20
            __M_writer(u'                <a data-ng-href="{{file.url}}" title="{{file.name}}" data-gallery="gallery" download="{{file.name}}"><img data-ng-src="{{file.thumbnail_url}}"></a>\n                <br />1/3 size thumbnail\n                <div class="spacer"></div>\n')
            pass
        # SOURCE LINE 24
        __M_writer(u'            <fieldset>\n            <label for="title" class="control-label" required>Title:</label>\n            <input type="text" name="title" value="')
        # SOURCE LINE 26
        __M_writer(escape(c.photoTitle))
        __M_writer(u'">\n            <label for="description" class="control-label" required>Description:</label>\n            <textarea name="description">')
        # SOURCE LINE 28
        __M_writer(escape(c.description))
        __M_writer(u'</textarea>\n\n            <label for="scope" class="control-label" required>Where was picture taken:</label>\n            ')
        # SOURCE LINE 31
 
        countyMessage = ""
        cityMessage = ""
        postalMessage = ""
        underPostalMessage = ""
                    
        
        # SOURCE LINE 36
        __M_writer(u'\n            <div class="row-fluid"><span id="countrySelect">\n                <div class="span1"></div>\n                <div class="span2">Country:</div>\n                <div class="span9">\n                    <select name="geoTagCountry" id="geoTagCountry" class="geoTagCountry" onChange="geoTagCountryChange(); return 1;">\n                    <option value="0" selected>Select a country</option>\n')
        # SOURCE LINE 43
        if c.country == '0':
            # SOURCE LINE 44
            __M_writer(u'                        <option value="United States">United States</option>\n')
            # SOURCE LINE 45
        else:
            # SOURCE LINE 46
            __M_writer(u'                        <option value="United States" selected>United States</option>\n')
            pass
        # SOURCE LINE 48
        __M_writer(u'                    </select>\n                </div><!-- span9 -->\n                </span><!-- countrySelect -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid"><span id="stateSelect">\n')
        # SOURCE LINE 53
        if c.country != "0":
            # SOURCE LINE 54
            __M_writer(u'                    ')
            states = geoLib.getStateList(c.country) 
            
            __M_writer(u'\n                    <div class="span1"></div>\n                    <div class="span2">State:</div>\n                    <div class="span9">\n                        <select name="geoTagState" id="geoTagState" class="geoTagState" onChange="geoTagStateChange(); return 1;">\n                        <option value="0">Select a state</option>\n')
            # SOURCE LINE 60
            for state in states:
                # SOURCE LINE 61
                if state != 'District of Columbia':
                    # SOURCE LINE 62
                    if c.state == state['StateFullName']:
                        # SOURCE LINE 63
                        __M_writer(u'                                    ')
                        stateSelected = "selected" 
                        
                        __M_writer(u'\n')
                        # SOURCE LINE 64
                    else:
                        # SOURCE LINE 65
                        __M_writer(u'                                    ')
                        stateSelected = "" 
                        
                        __M_writer(u'\n')
                        pass
                    # SOURCE LINE 67
                    __M_writer(u'                                <option value="')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'" ')
                    __M_writer(escape(stateSelected))
                    __M_writer(u'>')
                    __M_writer(escape(state['StateFullName']))
                    __M_writer(u'</option>\n')
                    pass
                pass
            # SOURCE LINE 70
            __M_writer(u'                        </select>\n                    </div><!-- span9 -->\n')
            # SOURCE LINE 72
        else:
            # SOURCE LINE 73
            __M_writer(u'                    or leave blank if your photo is specific to the entire planet.\n')
            pass
        # SOURCE LINE 75
        __M_writer(u'            </span></div><!-- row-fluid -->\n            <div class="row-fluid"><span id="countySelect">\n')
        # SOURCE LINE 77
        if c.state != "0":
            # SOURCE LINE 78
            __M_writer(u'                    ')
            counties = geoLib.getCountyList("united-states", c.state) 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 79
            cityMessage = "or leave blank if your photo is specific to the entire state." 
            
            __M_writer(u'\n                    <div class="span1"></div>\n                    <div class="span2">County:</div>\n                    <div class="span9">\n                        <select name="geoTagCounty" id="geoTagCounty" class="geoTagCounty" onChange="geoTagCountyChange(); return 1;">\n                        <option value="0">Select a county</option>\n')
            # SOURCE LINE 85
            for county in counties:
                # SOURCE LINE 86
                if c.county == county['County'].title():
                    # SOURCE LINE 87
                    __M_writer(u'                                ')
                    countySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 88
                else:
                    # SOURCE LINE 89
                    __M_writer(u'                                ')
                    countySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 91
                __M_writer(u'                            <option value="')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'" ')
                __M_writer(escape(countySelected))
                __M_writer(u'>')
                __M_writer(escape(county['County'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 93
            __M_writer(u'                        </select>\n                    </div><!-- span9 -->\n')
            # SOURCE LINE 95
        else:
            # SOURCE LINE 96
            __M_writer(u'                    ')
            cityMessage = "" 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 97
            __M_writer(escape(countyMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 99
        __M_writer(u'            </span></div><!-- row -->\n            <div class="row-fluid"><span id="citySelect">\n')
        # SOURCE LINE 101
        if c.county != "0":
            # SOURCE LINE 102
            __M_writer(u'                    ')
            cities = geoLib.getCityList("united-states", c.state, c.county) 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 103
            postalMessage = "or leave blank if your photo is specific to the entire county." 
            
            __M_writer(u'\n                    <div class="span1"></div>\n                    <div class="span2">City:</div>\n                    <div class="span9">\n                        <select name="geoTagCity" id="geoTagCity" class="geoTagCity" onChange="geoTagCityChange(); return 1;">\n                        <option value="0">Select a city</option>\n')
            # SOURCE LINE 109
            for city in cities:
                # SOURCE LINE 110
                if c.city == city['City'].title():
                    # SOURCE LINE 111
                    __M_writer(u'                                ')
                    citySelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 112
                else:
                    # SOURCE LINE 113
                    __M_writer(u'                                ')
                    citySelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 115
                __M_writer(u'                            <option value="')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'" ')
                __M_writer(escape(citySelected))
                __M_writer(u'>')
                __M_writer(escape(city['City'].title()))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 117
            __M_writer(u'                        </select>\n                    </div><!-- span9 -->\n')
            # SOURCE LINE 119
        else:
            # SOURCE LINE 120
            __M_writer(u'                    ')
            postalMessage = "" 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 121
            __M_writer(escape(cityMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 123
        __M_writer(u'            </span></div><!-- row-fluid -->\n            <div class="row-fluid"><span id="postalSelect">\n')
        # SOURCE LINE 125
        if c.city != "0":
            # SOURCE LINE 126
            __M_writer(u'                    ')
            postalCodes = geoLib.getPostalList("united-states", c.state, c.county, c.city) 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 127
            underPostalMessage = "or leave blank if your photo is specific to the entire city." 
            
            __M_writer(u'\n                    <div class="span1"></div>\n                    <div class="span2">Postal Code:</div>\n                    <div class="span9">\n                        <select name="geoTagPostal" id="geoTagPostal" class="geoTagPostal">\n                        <option value="0">Select a postal code</option>\n')
            # SOURCE LINE 133
            for pCode in postalCodes:
                # SOURCE LINE 134
                if c.postal == str(pCode['ZipCode']):
                    # SOURCE LINE 135
                    __M_writer(u'                                ')
                    postalSelected = "selected" 
                    
                    __M_writer(u'\n')
                    # SOURCE LINE 136
                else:
                    # SOURCE LINE 137
                    __M_writer(u'                                ')
                    postalSelected = "" 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 139
                __M_writer(u'                            <option value="')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'" ')
                __M_writer(escape(postalSelected))
                __M_writer(u'>')
                __M_writer(escape(pCode['ZipCode']))
                __M_writer(u'</option>\n')
                pass
            # SOURCE LINE 141
            __M_writer(u'                        </select>\n                    </div><!-- span9 -->\n')
            # SOURCE LINE 143
        else:
            # SOURCE LINE 144
            __M_writer(u'                    ')
            underPostalMessage = "" 
            
            __M_writer(u'\n                    ')
            # SOURCE LINE 145
            __M_writer(escape(postalMessage))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 147
        __M_writer(u'            </span></div><!-- row-fluid -->\n            <div class="row-fluid">\n                <span id="underPostal">')
        # SOURCE LINE 149
        __M_writer(escape(underPostalMessage))
        __M_writer(u'</span><br />\n            </div><!-- row-fluid -->\n        </fieldset>\n        </div><!-- span8 -->\n        <div class="span4">\n            ')
        # SOURCE LINE 154
        tagList = workshopLib.getWorkshopTagCategories() 
        
        __M_writer(u'\n            <fieldset>\n            Category Tags\n')
        # SOURCE LINE 157
        for tag in tagList:
            # SOURCE LINE 158
            __M_writer(u'                <label class="checkbox">\n')
            # SOURCE LINE 159
            if tag in c.categories:
                # SOURCE LINE 160
                __M_writer(u'                    <input type="checkbox" name="categoryTags" value="')
                __M_writer(escape(tag))
                __M_writer(u'" checked /> ')
                __M_writer(escape(tag))
                __M_writer(u'\n')
                # SOURCE LINE 161
            else:
                # SOURCE LINE 162
                __M_writer(u'                    <input type="checkbox" name="categoryTags" value="')
                __M_writer(escape(tag))
                __M_writer(u'" /> ')
                __M_writer(escape(tag))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 164
            __M_writer(u'                </label>\n')
            pass
        # SOURCE LINE 166
        __M_writer(u'            </fieldset>\n        </div><!-- span4 -->\n    </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_photoModerationPanel(context,thing):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 234
        __M_writer(u'\n    ')
        # SOURCE LINE 235

        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        publishID = 'publish-%s' % thing['urlCode']
        unpublishID = 'unpublish-%s' % thing['urlCode']
            
        
        # SOURCE LINE 243
        __M_writer(u'\n    <div class="btn-group">\n')
        # SOURCE LINE 245
        if thing['disabled'] == '0' and thing.objType != 'photoUnpublished':
            # SOURCE LINE 246
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(flagID))
            __M_writer(u'">flag</a>\n')
            pass
        # SOURCE LINE 248
        if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'photoUnpublished':
            # SOURCE LINE 249
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(editID))
            __M_writer(u'">edit</a>>\n')
            pass
        # SOURCE LINE 251
        if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)) and thing.objType != 'photoUnpublished':
            # SOURCE LINE 252
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(unpublishID))
            __M_writer(u'">unpublish</a>\n')
            # SOURCE LINE 253
        elif thing.objType == 'photoUnpublished' and thing['unpublished_by'] != 'parent':
            # SOURCE LINE 254
            if thing['unpublished_by'] == 'admin' and userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 255
                __M_writer(u'                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(publishID))
                __M_writer(u'">publish</a>\n')
                # SOURCE LINE 256
            elif thing['unpublished_by'] == 'owner' and c.authuser.id == thing.owner:
                # SOURCE LINE 257
                __M_writer(u'                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(publishID))
                __M_writer(u'">publish</a>\n')
                pass
            pass
        # SOURCE LINE 260
        if userLib.isAdmin(c.authuser.id):
            # SOURCE LINE 261
            __M_writer(u'            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(adminID))
            __M_writer(u'">admin</a>\n')
            pass
        # SOURCE LINE 263
        __M_writer(u'\n    </div>\n    \n')
        # SOURCE LINE 266
        if thing['disabled'] == '0':
            # SOURCE LINE 267
            if thing.objType != 'photoUnpublished':
                # SOURCE LINE 268
                __M_writer(u'            ')
                __M_writer(escape(lib_6.flagThing(thing)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 270
            if (c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id)):
                # SOURCE LINE 271
                if thing.objType != 'photoUnpublished':
                    # SOURCE LINE 272
                    __M_writer(u'                ')
                    editID = 'edit-%s'%thing['urlCode'] 
                    
                    __M_writer(u'\n                <div class="row-fluid collapse" id="')
                    # SOURCE LINE 273
                    __M_writer(escape(editID))
                    __M_writer(u'">\n                    <div class="span11 offset1">\n                        <div class="spacer"></div>\n                        <form action="/profile/')
                    # SOURCE LINE 276
                    __M_writer(escape(c.user['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.user['url']))
                    __M_writer(u'/photo/')
                    __M_writer(escape(c.photo['pictureHash_photos']))
                    __M_writer(u'/update/handler" method="post" class="form">\n                            ')
                    # SOURCE LINE 277
                    __M_writer(escape(self.editPhoto()))
                    __M_writer(u'\n                            <div class="row-fluid">\n                                <button class="btn btn-success" type="Submit">Save Changes</button>\n                            </div><!-- row-fluid -->\n                        </form>\n                    </div><!-- span11 -->\n                </div><!-- row-fluid -->\n')
                    pass
                # SOURCE LINE 285
                if thing.objType == 'photoUnpublished':
                    # SOURCE LINE 286
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.publishThing(thing)))
                    __M_writer(u'\n')
                    # SOURCE LINE 287
                else:
                    # SOURCE LINE 288
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.unpublishThing(thing)))
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 290
                if userLib.isAdmin(c.authuser.id):
                    # SOURCE LINE 291
                    __M_writer(u'                ')
                    __M_writer(escape(lib_6.adminThing(thing)))
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 294
        else:
            # SOURCE LINE 295
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 296
                __M_writer(u'            ')
                editID = 'edit-%s'%thing['urlCode'] 
                
                __M_writer(u'\n            <div class="row-fluid collapse" id="')
                # SOURCE LINE 297
                __M_writer(escape(editID))
                __M_writer(u'">\n                <div class="span11 offset1">\n                    <div class="spacer"></div>\n                    <form action="/profile/')
                # SOURCE LINE 300
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/photo/')
                __M_writer(escape(c.photo['pictureHash_photos']))
                __M_writer(u'/update/handler" method="post" class="form">\n                        ')
                # SOURCE LINE 301
                __M_writer(escape(self.editPhoto()))
                __M_writer(u'\n                        <div class="row-fluid">\n                            <button class="btn btn-success" type="Submit">Save Changes</button>\n                        </div><!-- row-fluid -->\n                    </form>\n                </div><!-- span11 -->\n            </div><!-- row-fluid -->\n')
                pass
            # SOURCE LINE 309
            if userLib.isAdmin(c.authuser.id):
                # SOURCE LINE 310
                __M_writer(u'            ')
                __M_writer(escape(lib_6.adminThing(thing)))
                __M_writer(u'\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showPhoto(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 315
        __M_writer(u'\n')
        # SOURCE LINE 316
        if c.photo['deleted'] == '0':
            # SOURCE LINE 317
            __M_writer(u'\n        ')
            # SOURCE LINE 318
            imgSrc = "/images/photos/" + c.photo['directoryNum_photos'] + "/orig/" + c.photo['pictureHash_photos'] + ".png" 
            
            __M_writer(u'\n        <img src="')
            # SOURCE LINE 319
            __M_writer(escape(imgSrc))
            __M_writer(u'" class="wrap-photo"><br />\n        <div class="spacer"></div>\n        <div class="centered">\n            ')
            # SOURCE LINE 322
            __M_writer(escape(c.photo['title']))
            __M_writer(u'<br />\n        </div><!-- centered -->\n        ')
            # SOURCE LINE 324
            tags = c.photo['tags'].split('|') 
            
            __M_writer(u'\n        Tags: \n')
            # SOURCE LINE 326
            for tag in tags:
                # SOURCE LINE 327
                if tag != '':
                    # SOURCE LINE 328
                    __M_writer(u'                ')
 
                    tTitle = tag.title()
                                    
                    
                    # SOURCE LINE 330
                    __M_writer(u'\n                <span class="label workshop-tag ')
                    # SOURCE LINE 331
                    __M_writer(escape(tag))
                    __M_writer(u'">')
                    __M_writer(escape(tTitle))
                    __M_writer(u'</span>\n')
                    pass
                pass
            # SOURCE LINE 334
            __M_writer(u'        <br />\n        Added: ')
            # SOURCE LINE 335
            __M_writer(escape(c.photo.date))
            __M_writer(u'\n        <br />\n        Views: ')
            # SOURCE LINE 337
            __M_writer(escape(c.photo['views']))
            __M_writer(u'\n        <br />\n')
            # SOURCE LINE 339
            if c.photo.objType == 'photoUnpublished':
                # SOURCE LINE 340
                __M_writer(u'            Unpublished by: ')
                __M_writer(escape(c.photo['unpublished_by']))
                __M_writer(u'<br />\n')
                pass
            # SOURCE LINE 342
            __M_writer(u'        Photo Location: ')
            __M_writer(escape(photoLib.getPhotoLocation(c.photo)))
            __M_writer(u'<br />\n        <div class="spacer"></div>\n        ')
            # SOURCE LINE 344
            __M_writer(escape(c.photo['description']))
            __M_writer(u'\n        <div class="spacer"></div>\n')
            # SOURCE LINE 346
        else:
            # SOURCE LINE 347
            __M_writer(u'        ')

            event = eventLib.getEventsWithAction(c.photo, 'deleted')[0]
            deleter = userLib.getUserByID(event.owner)
            reason = event['reason']
                    
            
            # SOURCE LINE 351
            __M_writer(u'\n        <div class="row-fluid">\n            This picture deleted by ')
            # SOURCE LINE 353
            __M_writer(escape(deleter['name']))
            __M_writer(u' because: ')
            __M_writer(escape(reason))
            __M_writer(u'\n        </div><!-- row-fluid -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_uploadPhoto(context):
    context.caller_stack._push_frame()
    try:
        def editPhoto():
            return render_editPhoto(context)
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 171
        __M_writer(u'\n')
        # SOURCE LINE 172
        if 'user' in session and (c.authuser.id == c.user.id) and not c.privs['provisional']:
            # SOURCE LINE 173
            __M_writer(u'        <form id="fileupload" action="/profile/')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'/photo/upload/handler" method="POST" enctype="multipart/form-data" data-ng-app="demo" data-fileupload="options" ng-class="{true: \'fileupload-processing\'}[!!processing() || loadingFiles]" class = "civAvatarUploadForm" ng-show="true">\n            <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">\n                <div class="span10 offset1">\n                    <!-- The fileinput-button span is used to style the file input field as button -->\n                    <span class="pull-left">Document your community with pictures.  (5MB max, please)</span>\n                    <span class="btn btn-success fileinput-button pull-right"  data-toggle="collapse" data-target="#fileinput-button-div">\n                        <i class="icon-plus icon-white"></i>\n                        <span>Picture</span>\n                        <input type="file" name="files[]">\n                    </span>\n                    <!-- The loading indicator is shown during file processing -->\n                    <div class="fileupload-loading"></div>\n                </div><!-- span10 -->\n                <!-- The global progress information -->\n            </div><!-- row-fluid -->\n            <div class="row-fluid">\n                <div class="span10 offset1 fade" data-ng-class="{true: \'in\'}[!!active()]">\n                    <!-- The global progress bar -->\n                    <div class="progress progress-success progress-striped active" data-progress="progress()"><div class="bar" ng-style="{width: num + \'%\'}"></div></div>\n                    <!-- The extended global progress information -->\n                    <div class="progress-extended">&nbsp;</div>\n                </div><!- span10 -->\n            </div><!-- row-fluid -->\n            <!-- The table listing the files available for upload/download -->\n            <table class="table table-striped files ng-cloak" data-toggle="modal-gallery" data-target="#modal-gallery">\n                <tbody><tr data-ng-repeat="file in queue">\n                    <td data-ng-switch="" on="!!file.thumbnail_url">\n                        <div class="preview" data-ng-switch-when="true">\n                            <script type="text/javascript">\n                                function setAction(imageHash) {\n                                    actionURL = "/profile/')
            # SOURCE LINE 203
            __M_writer(escape(c.user['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.user['url']))
            __M_writer(u'/photo/" + imageHash + "/update/handler";\n                                    document.getElementById(\'fileupload\').action = actionURL;\n                                }\n                            </script>\n                            ')
            # SOURCE LINE 207
            __M_writer(escape(editPhoto()))
            __M_writer(u'\n                            <div class="row-fluid">\n                                <button class="btn btn-success" type="Submit" onClick="setAction(\'{{file.image_hash}}\'); return 1;">Save Changes</button>\n                            </div><!-- row-fluid -->\n                            </form>\n                        </div><!-- preview -->\n                        <div class="preview" data-ng-switch-default="" data-preview="file" id="preview"></div>\n                    </td>\n                    <td>\n                        <div ng-show="file.error"><span class="label label-important">Error</span> {{file.error}}</div>\n                    </td>\n                    <td>\n                        <button type="button" class="btn btn-primary start" data-ng-click="file.$submit()" data-ng-hide="!file.$submit">\n                        <i class="icon-upload icon-white"></i>\n                        <span>Save</span>\n                        </button>\n                        <button type="button" class="btn btn-warning cancel" data-ng-click="file.$cancel()" data-ng-hide="!file.$cancel"  data-toggle="collapse" data-target="#fileinput-button-div">\n                        <i class="icon-ban-circle icon-white"></i>\n                        <span>Cancel</span>\n                        </button>\n                    </td>\n                </tr>\n            </tbody></table>\n        </form>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


