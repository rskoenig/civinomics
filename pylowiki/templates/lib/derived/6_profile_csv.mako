<%!
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
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="uploadCsv()">
    % if 'user' in session and (c.authuser.id == c.user.id) and not c.privs['provisional']:
        <form id="fileupload" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/csv/upload/handler" method="POST" enctype="multipart/form-data">
            <div id="fileinput-button-div" class="row-fluid fileupload-buttonbar collapse in">
                <div class="span10 offset1">
                    <!-- The fileinput-button span is used to style the file input field as button -->
                    <span class="pull-left">Upload the CSV with the information on the users.  (5MB max, please)</span>
                    
                    
                    <!-- The loading indicator is shown during file processing -->
                    <div class="fileupload-loading">
	                    
                    </div>
                </div><!-- span10 -->
                <!-- The global progress information -->
            </div><!-- row-fluid -->
            <div class="row-fluid">
                <div class="span10 offset1 fade">
                    <!-- The global progress bar -->
                    <div class="progress progress-success progress-striped"><div class="bar" ng-style="{width: num + '%'}"></div></div>
                    <!-- The extended global progress information -->
                    <div class="progress-extended">&nbsp;</div>
                </div><!- span10 -->
            </div><!-- row-fluid -->
            <div id="progressbox" >
            <div id="file_accepted" style="display:none">
            			<button type="submit" id="submit_button" type="submit" class="btn btn-primary start" value="process">
                        <i class="icon-upload icon-white"></i>
                        <span>Process</span>
                        </button>

						<button id="cancel_button" type="button" class="btn btn-warning cancel" >
                        <i class="icon-ban-circle icon-white"></i>
                        <span>Cancel</span>
                        </button>
            <div id="progressbar"></div >
			</div>
            </div><!--file_accepted-->
            <span class="btn btn-success pull-right">
                        <i class="icon-plus icon-white"></i>
                        <span>CSV</span>
                        <input id="fileUploadButton" type="file" name="files[]">
                    </span>
        </form>
    % endif
</%def>

<%def name="showCsv()">
	<div ng-app="myApp">
		<div ng-controller="MyCtrl">
			<div ng-grid="gridOptions">
			</div>
		</div>
	</div>
</%def>