<%!
    from pylowiki.lib.db.surveySlide import getSurveySlideByID, getSurveySlideByName
    from pylowiki.lib.db.surveyAnswer import getSurveyAnswer
    
    import logging
    log = logging.getLogger(__name__)
%>

<%def name='showSlide(survey, slide)'>
    <% 
        answer = getSurveyAnswer(survey, slide, c.authuser)
    %>
    <div class="thumbnail slideFrame">
        ${showHeader(survey, slide)}
        <%
            ignoreImage = False
            if 'ignore' in slide.keys():
                if int(slide['ignore']) == 1:
                    ignoreImage = True
            if slide['image'] == '':
                ignoreImage = True
        %>
        % if not ignoreImage:                    
            <img src="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${slide['image']}">
        % else:
            <div style="height:25px;" class="row"></div>
        % endif
        
        % if 'title' in slide.keys():
            ${showSlideTitle(slide)}
        % endif
        
        <%
            if slide['type'] == 'checkbox':
                if slide['checkboxType'] == 'exclusive':
                    radioButtons(survey, slide, answer)
                else:
                    checkBoxes(survey, slide, answer)
               
            elif slide['type'] == 'info':
                if int(slide['numhAnswerBoxes']) > 0:
                    hAnswerBoxes(survey, slide, answer)
                if int(slide['numhCheckboxes']) > 0:
                    if slide['hCheckboxType'] == 'exclusive':
                        hRadioButtons(survey, slide, aswer)
                    elif slide['hCheckboxType'] == 'inclusive':
                        hCheckBoxes(survey, slide, answer)
                if int(slide['numhLinks']) > 0:
                    hLinks(survey, slide)
                
            elif slide['type'] == 'itemRanking':
                if int(slide['numRankItems']) > 0:
                    itemRanking(survey, slide, answer)
                
            elif slide['type'] == 'multi-slider':
                if int(slide['numSliders']) > 0:
                    multiSlider(survey, slide, answer)
                
            elif slide['type'] == 'slider':
                slider(survey, slide, answer)
            elif slide['type'] == 'feedback':
                feedback(survey, slide, answer)
        %>
        
        <%
            if 'caption' in slide.keys():
                showCaption(slide)
        %>
        
        <div class="message"></div>
        ${spacer()}
    </div>
</%def>

<%def name='showSlideTitle(slide)'>
    <h1 class="slideTitle">${slide['title']}</h3>
</%def>

<%def name='showCaption(survey)'>
    <p class="caption">${survey['caption']}</p>
</%def>
    
<%def name='showPrevSliderHelp()'>
    <h4>Previously visited slides</h4>
</%def>
    
<%def name='radioButtons(survey, slide, answer)'>
    <%
        numButtons = int(slide['numCheckboxes'])
        buttons = []
        if not answer:
            for i in range(numButtons):
                description = slide['checkbox_description_%s' % (i + 1)]
                label = slide['checkbox_label_%s' % (i + 1)]
                buttons.append({'description':description, 'label':label, 'checked':False})
        else:
            for i in range(numButtons):
                description = slide['checkbox_description_%s' % (i + 1)]
                label = slide['checkbox_label_%s' % (i + 1)]
                if label == answer['answer']:
                    buttons.append({'description':description, 'label':label, 'checked':True})
                else:
                    buttons.append({'description':description, 'label':label, 'checked':False})
    %>
    <form class="form-horizontal" id="radioForm">
        <fieldset>
            ##<div class="control-group" style="position:absolute;display:block;top:31%;left:24%;">
            <div class="control-group">
                <div class="controls" style="float:left;">
                    % for button in buttons:
                        <label class="radio">
                            % if button['checked']:
                                <input type = "radio" value = "${button['label']}" name="radioButton" id="option_${button['label']}" class="radioButton" checked = "">
                                <%
                                    log.info(button)
                                %>
                            % else:
                                <input type = "radio" value = "${button['label']}" name="radioButton" id="option_${button['label']}" class="radioButton">
                            % endif
                            ${button['description']}
                        </label>
                    % endfor
                </div>
            </div>
            ##<a style="position:absolute;display:block;top:66%;left:45%;" class="btn btn-primary radioSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
            <a class="btn btn-primary radioSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
        </fieldset>
    </form>
</%def>

<%def name='checkBoxes(survey, slide, answer)'>
    <%
        numButtons = int(slide['numCheckboxes'])
        buttons = []
        if not answer:
            for i in range(numButtons):
                description = slide['checkbox_description_%s' % (i + 1)]
                label = slide['checkbox_label_%s' % (i + 1)]
                buttons.append({'description':description, 'label':label, 'checked':False})
        else:
            for i in range(numButtons):
                description = slide['checkbox_description_%s' % (i + 1)]
                label = slide['checkbox_label_%s' % (i + 1)]
                if label == answer['answer']:
                    buttons.append({'description':description, 'label':label, 'checked':True})
                else:
                    buttons.append({'description':description, 'label':label, 'checked':False})
    %>
    <form class="form-horizontal" id="radioForm">
        <fieldset>
            <div class="control-group" style="position:absolute;display:block;top:31%;left:24%;">
                <div class="controls">
                    % for button in buttons:
                        <label class="checkbox">
                            % if button['checked']:
                                <input type = "checkbox" value = "${button['label']}" name="checkboxButton" id="option_${button['label']}" class="checkboxButton" checked = "">
                                <%
                                    log.info(button)
                                %>
                            % else:
                                <input type = "checkbox" value = "${button['label']}" name="checkboxButton" id="option_${button['label']}" class="checkboxButton">
                            % endif
                            ${button['description']}
                        </label>
                    % endfor
                </div>
            </div>
            <a style="position:absolute;display:block;top:66%;left:45%;" class="btn btn-primary radioSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
        </fieldset>
    </form>
</%def>

<%def name='hAnswerBoxes(survey, slide, answer)'>
    <%
        numTextBoxes = int(slide['numhAnswerBoxes'])
        textBoxes = []
        for i in range(numTextBoxes):
            coords = slide['hAnswerBox_coords_%s' % (i + 1)]
            coordList = coords.split(',')
            percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
            percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
            percentW = "{0:.0f}%".format(float(coordList[2])/1024 * 100)
            percentH = "{0:.0f}%".format(float(coordList[3])/768 * 100)
            label = slide['hAnswerBox_label_%s' % (i + 1)]
            alignment = slide['hAnswerBox_alignment_%s' % (i + 1)]
            textSize = slide['hAnswerBox_textSize_%s' % (i + 1)]
            textBoxes.append({'label':label, 'alignment':alignment, 'textSize':textSize, 'percentX':percentX, 'percentY':percentY, 'percentW':percentW, 'percentH':percentH, 'answer':answer})
    %>
    <form class="form-horizontal" id="radioForm">
    	<fieldset>
            <div class="control-group">
                <div class="controls">
			        % for textBox in textBoxes:
			            <textarea rows="2" cols="30" style="position:absolute;display:block;top:${textBox['percentY']};left:${textBox['percentX']};font-size:${textBox['textSize']}px;">${textBox['answer']}</textarea>
			        % endfor
			    </div>
			</div>
    		<a style="position:absolute;display:block;top:70%;left:46%;" class="btn btn-primary checkboxSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
		</fieldset>
    </form>
</%def>

<%def name='hRadioButtons(survey, slide, answer)'>
    <%
        numButtons = int(slide['numhCheckboxes'])
        buttons = []
        if not answer:
            for i in range(numButtons):
                coords = slide['hCheckbox_coords_%s' % (i + 1)]
                coordList = coords.split(',')
                percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
                percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
                label = slide['hCheckbox_label_%s' % (i + 1)]
                link = slide['hCheckbox_link_%s' % (i + 1)]
                buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':False})
        else:
            for i in range(numButtons):
                coords = slide['hCheckbox_coords_%s' % (i + 1)]
                coordList = coords.split(',')
                percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
                percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
                label = slide['hCheckbox_label_%s' % (i + 1)]
                link = slide['hCheckbox_link_%s' % (i + 1)]
                if label == answer['answer']:
                    buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':True})
                else:
                    buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':False})
    %>
    <form class="form-horizontal" id="radioForm">
    	<fieldset>
            <div class="control-group">
                <div class="controls">
			        % for button in buttons:
			            <label class="radio">
			                % if button['checked']:
			                    <input type = "radio" value = "${button['label']}" name="radioButton" id="option_${button['label']}" class="radioButton" checked = "" style="position:absolute;display:block;top:${button['percentX']};left:${button['percentY']};">
			                    <%
			                        log.info(button)
			                    %>
			                % else:
			                    <input type = "radio" value = "${button['label']}" name="radioButton" id="option_${button['label']}" class="radioButton" style="position:absolute;display:block;top:${button['percentX']};left:${button['percentY']};">
			                % endif
			            </label>
			        % endfor
				</div>
            </div>
    		<a style="position:absolute;display:block;top:70%;left:46%;" class="btn btn-primary radioSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
    	</fieldset>
    </form>
</%def>

<%def name='hCheckBoxes(survey, slide, answer)'>
    <%
        numButtons = int(slide['numhCheckboxes'])
        buttons = []
        if not answer:
            for i in range(numButtons):
                coords = slide['hCheckbox_coords_%s' % (i + 1)]
                coordList = coords.split(',')
                percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
                percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
                label = slide['hCheckbox_label_%s' % (i + 1)]
                link = slide['hCheckbox_link_%s' % (i + 1)]
                buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':False})
        else:
            for i in range(numButtons):
                coords = slide['hCheckbox_coords_%s' % (i + 1)]
                coordList = coords.split(',')
                percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
                percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
                label = slide['hCheckbox_label_%s' % (i + 1)]
                link = slide['hCheckbox_link_%s' % (i + 1)]
                if label == answer['answer']:
                    buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':True})
                else:
                    buttons.append({'label':label, 'link':link, 'percentX':percentX, 'percentY':percentY, 'checked':False})
    %>
    <form class="form-horizontal" id="radioForm">
    	<fieldset>
            <div class="control-group">
                <div class="controls">
			        % for button in buttons:
			            <label class="checkbox">
			                % if button['checked']:
			                    <input type = "checkbox" value = "${button['label']}" name="checkboxButton" id="option_${button['label']}" class="checkboxButton" checked = "" style="position:absolute;display:block;top:${button['percentX']};left:${button['percentY']};">
			                    <%
			                        log.info(button)
			                    %>
			                % else:
			                    <input type = "checkbox" value = "${button['label']}" name="checkboxButton" id="option_${button['label']}" class="checkboxButton" style="position:absolute;display:block;top:${button['percentX']};left:${button['percentY']};">
			                % endif
			            </label>
			        % endfor
			    </div>
			</div>
    		<a style="position:absolute;display:block;top:70%;left:46%;" class="btn btn-primary checkboxSubmit" type="submit" href="/survey/submit/radio/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
		</fieldset>
    </form>
</%def>

<%def name='hLinks(survey, slide)'>
    <%
        numButtons = int(slide['numhLinks'])
        buttons = []
        for i in range(numButtons):
            coords = slide['hLink_coords_%s' % (i + 1)]
            coordList = coords.split(',')
            percentX = "{0:.0f}%".format(float(coordList[0])/1024 * 100)
            percentY = "{0:.0f}%".format(float(coordList[1])/768 * 100)
            ## assuming the clear image (if none is provided) is 10% of the screen and 100% width means it should take the whole screen, multiply by a factor of 10
            percentW = "{0:.0f}%".format(float(coordList[2])/1024 * 100)
            percentH = "{0:.0f}%".format(float(coordList[3])/768 * 100)            
            image = slide['hLink_image_%s' % (i + 1)]
            link = slide['hLink_link_%s' % (i + 1)]
            linkedSlide = getSurveySlideByName(link, survey)
            log.info(linkedSlide)
            ##linkedSlide = getSurveySlideByID(link)
            hash = linkedSlide['hash']
            buttons.append({'image':image, 'hash':hash, 'percentX':percentX, 'percentY':percentY, 'percentW':percentW, 'percentH':percentH})
    %>
    % for button in buttons:
    	<a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${button['hash']}" >
    		% if button['image'] != '':
    			<div class="thumbnail noBorder" style="position:absolute;display:block;left:${button['percentX']};top:${button['percentY']};width:${button['percentW']};height:${button['percentH']};">
    				<img src="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${button['image']}">
    			</div>
    		% else:
    			<div class="thumbnail noBorder" style="position:absolute;display:block;left:${button['percentX']};top:${button['percentY']};width:${button['percentW']};height:${button['percentH']};">
    				<img src="/images/exampleClear.png" />
    			</div>
    		% endif
    	</a>
    % endfor
</%def>

<%def name="itemRanking(survey, slide, answer)">
	<%
		itemRankingHeader = {'title':slide['rankItemTitleText'], 'header':slide['rankItemHeader']}
		numRankItems = int(slide['numRankItems'])
		rankItems = []
		for i in range(numRankItems):
			title = slide['rankItem_title_%s' % (i + 1)]
			label = slide['rankItem_label_%s' % (i + 1)]
			rankItems.append({'title':title, 'label':label})
	%>
	${spacer()}
	<form>
		<fieldset>
			<table class="table-bordered" style="position:absolute;display:block;top:15%;left:25%;">
				<thead>
					<tr style="background-color:#ccc;">
						<th>${itemRankingHeader['header']}</th>
						<th>${itemRankingHeader['title']}</th>
					</tr>
				</thead>
				<tbody>
					%for i in range(numRankItems):
						<tr style="background-color:#fff;">
							<td style="padding-bottom:8px;">Rank ${(i + 1)}</td>
							<td>
								<select name="${i + 1}">
									<option value="0" selected="SELECTED">...</option>
									% for rankItem in rankItems:
										<option value="${rankItem['label']}" class="itemRank">${rankItem['title']}</option>
									% endfor
								</select>
							</td>
						</tr>
					% endfor
				</tbody>
			</table>
		</fieldset>
        <a style="position:absolute;display:block;top:70%;left:46%;" class="btn btn-primary itemRankingSubmit" href="/survey/submit/itemRank/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
    </form>
</%def>

<%def name="multiSlider(survey, slide, answer)">
    <%
    	titleText = slide['sliderTitleText']
    	leftSlider = slide['leftSliderText']
    	middleSlider = slide['middleSliderText']
    	rightSlider = slide['rightSliderText']
        sliderHeader = {'title':titleText, 'left':leftSlider, 'middle':middleSlider, 'right':rightSlider}
        numSliders = int(slide['numSliders'])
        sliders = []
        for i in range(numSliders):
            title = slide['slider_title_%s' % (i + 1)]
            label = slide['slider_label_%s' % (i + 1)]

            sliders.append({'title':title, 'label':label})
    %>

    <table class="table">
        <thead>
            <tr>
                % if 'title' in sliderHeader.keys():
                    <th> ${sliderHeader['title']} </th>
                % else:
                    <th></th>
                % endif

                % if 'left' in sliderHeader.keys():
                    <th style="text-align:left;"> ${sliderHeader['left']} </th>
                % else:
                    <th></th>
                % endif

                % if 'middle' in sliderHeader.keys():
                    <th style="text-align:center;"> ${sliderHeader['middle']} </th>
                % else:
                    <th></th>
                % endif

                % if 'right' in sliderHeader.keys():
                    <th style="text-align:right;"> ${sliderHeader['right']} </th>
                % else:
                    <th></th>
                % endif
            </tr>
        </thead>

        <tbody>
            % for slider in sliders:
                <tr>
                    <td style="height:50px;">${slider['title']}</td>
                    <td colspan="3">
                        <div id="overall_slider" class="ui-slider-container" >
                            % if not answer:
                                <div id="${survey['urlCode']}_${survey['url']}" class="survey_multiSlider" 
                                surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                                slideCode = "${slide['hash']}" sliderLabel = "${slider['label']}" rating = "50" isRated = "False"
                                href = "survey/submit/multiSlider">
                                </div>
                            % else:
                                <div id="urlCode_url" class="survey_multiSlider" 
                                surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                                slideCode = "${slide['hash']}" sliderLabel = "${slider['label']}" rating = "${answer['answer_%s'%slider['label']]}" 
                                isRated = "true" href = "survey/submit/multiSlider">
                                </div>
                            % endif
                        </div>
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>

    <%doc>
    ${spacer()}
    ##<div style="position:absolute;display:block;top:25%;left:1%;">
    <div>
    <div class="row-fluid">
        % if slide['sliderTitleText'] == '':
        	<div class="span4" style="text-align:center;">&nbsp;</div>
        % else:
        	<div class="span4" style="text-align:center;font-weight:bold;">${sliderHeader['title']}</div>
        % endif
        % if slide['leftSliderText'] == '':
        	<div class="span2" style="text-align:center;">&nbsp;</div>
        % else:
        	<div class="span2" style="text-align:center;font-weight:bold;">${sliderHeader['left']}</div>
        % endif
        % if not slide['middleSliderText']:
        	<div class="span2" style="text-align:left;">&nbsp;</div>
        % else:
        	<div class="span2" style="text-align:left;font-weight:bold;">&nbsp;&nbsp;&nbsp;${sliderHeader['middle']}</div>
        % endif
        % if slide['rightSliderText'] == '':
        	<div class="span2" style="text-align:left;">&nbsp;</div>
        % else:
        	<div class="span2" style="text-align:left;font-weight:bold;">${sliderHeader['right']}</div>
        % endif
    </div>
    ${spacer()}
    ${spacer()}
    ${spacer()}
    % for slider in sliders:
        <div class="row-fluid">
            <div class="span4">${slider['title']}</div>
            <div class="span6">
                <div id="overall_slider" class="span9 ui-slider-container" style="padding-left:25px">
                    % if not answer:
                        <div id="${survey['urlCode']}_${survey['url']}" class="survey_multiSlider" 
                        surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                        slideCode = "${slide['hash']}" sliderLabel = "${slider['label']}" rating = "50" isRated = "False"
                        href = "survey/submit/multiSlider"
                        ></div>
                    % else:
                        <div id="urlCode_url" class="survey_multiSlider" 
                        surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                        slideCode = "${slide['hash']}" sliderLabel = "${slider['label']}" rating = "${answer['answer_%s'%slider['label']]}" 
                        isRated = "true" href = "survey/submit/multiSlider"
                        ></div>
                    % endif
                </div>
            </div>
        </div>
        ${spacer()}
        ${spacer()}
    % endfor
	</div>
    </%doc>
</%def>

<%def name="slider(survey, slide, answer)">
    ${spacer()}
    ${spacer()}
    
    <div class="row-fluid">
        ${inlineSpacer(1)}
        <div class="span2">${slide['leftSliderText']}</div>
        ${inlineSpacer(2)}
        <div class="span2">${slide['middleSliderText']}</div>
        ${inlineSpacer(2)}
        <div class="span2">${slide['rightSliderText']}</div>
        ${inlineSpacer(1)}
    </div>
    
    <div class="row-fluid">
        ${inlineSpacer(1)}
        <div id="overall_slider" class="span9 ui-slider-container" style="padding-left:25px">
            % if not answer:
                <div id="${survey['urlCode']}_${survey['url']}" class="survey_slider" 
                surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                slideCode = "${slide['hash']}" sliderLabel = "" rating = "50" isRated = "False"
                href = "survey/submit/slider"
                ></div>
            % else:
                <div id="urlCode_url" class="survey_slider" 
                surveyCode = "${survey['urlCode']}" surveyURL = "${survey['url']}"
                slideCode = "${slide['hash']}" sliderLabel = "" rating = "${answer['answer']}" isRated = "true"
                href = "survey/submit/slider"
                ></div>
            % endif
        </div>
        ${inlineSpacer(1)}
    </div>
    ${spacer()}
    ${spacer()}
</%def>

<%def name="feedback(survey, slide, answer)">
    <div class="row"><p></p></div>
    <form class="form-horizontal">
        <fieldset>
            <div class="control-group">
                % if not answer:
                    <textarea name="feedback" class="input-xxlarge" id="textarea" rows="6"></textarea>
                % else:
                    <textarea name="feedback" class="input-xxlarge" id="textarea" rows="6" placeholder = "${answer['answer']}"></textarea>
                % endif
            </div>
        </fieldset>
        <a class="btn btn-primary textareaSubmit" href="/survey/submit/textarea/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Save</a>
    </form>
</%def>

<%def name='showVocalText(slide)'>
    % if slide['vocal'] != '':
        <div class="well" style="background-color:#D1CCC3;">
              ${slide['vocal']}
        </div>
    % endif
</%def>

<%def name='showNavElements(pageNum, totalPages, nextSlide, prevSlide, survey)'>
    ## The navigation buttons and numerical progress
    <h2>
    % if pageNum == 0:
        <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_224_thin_arrow_left.png">
    
        ${pageNum} / ${totalPages - 1}
        
        <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${nextSlide['hash']}">
            <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_223_thin_right_arrow.png">
        </a>
    % elif pageNum == totalPages - 1:
        <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${prevSlide['hash']}">
            <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_224_thin_arrow_left.png">
        </a>
    
        ${pageNum} / ${totalPages - 1}
        
        <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_223_thin_right_arrow.png">
    % else:
        <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${prevSlide['hash']}">
            <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_224_thin_arrow_left.png">
        </a>
    
        ${pageNum} / ${totalPages - 1}
        
        <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${nextSlide['hash']}">
            <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_223_thin_right_arrow.png">
        </a>
    % endif
    </h2>
    <br />
</%def>

<%def name='showProgressBar(pageNum, totalPages)'>
    <div class="progress" style="background-image:none; background-color:#D1CCC3;">
        <div class="bar" style="width: ${(float(pageNum)/float(totalPages - 1))*100}%;"></div>
    </div>
</%def>

<%def name='showTitle(survey)'>
    <h1> ${survey['title']} </h1>
</%def>

<%def name='spacer()'>
    ## A spacer
    <div class="row-fluid">
        <br />
    </div>
</%def>

<%def name='inlineSpacer(amount)'>
    <div class="span${amount}">
        <p></p>
    </div>
</%def>

<%def name="showPrevSlides(slides, slideNum, survey)">
    <% 
        if c.surveySection == 'after':
            slides = map(int, survey['slides'].split(','))
    %>
    <div class="span8">
        <div id="mcs5_container" class="outerMCS">
            <div class="customScrollBox">
                <div class="horWrapper">
                    <div class="containerMCS">
                        <div class="content">
                            <ul class="thumbnails">
                                % for slideID in slides:
                                    <%
                                        slide = getSurveySlideByID(slideID)
                                        if int(slide['slideNum']) > slideNum:
                                            break
                                    %>
                                    
                                    <li class="span1" style="display: inline;">
                                        <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}" class="thumbnail span1" style="margin-left:10px;">
                                            <%
                                                thumbnailFile = slide['image'].split('.')
                                                thumbnailFile.pop()
                                                thumbnailFile.insert(1, 'thumbnail')
                                                thumbnailFile = '.'.join(thumbnailFile)
                                            %>
                                            <img src = "/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${thumbnailFile}.thumbnail">
                                            <h5 style = "text-align:center;">Slide ${slide['slideNum']}</h5>
                                        </a>
                                    </li>
                                % endfor
                            </ul>
                        </div> <!-- div content -->
                    </div> <!-- div container MCS -->
                    <div class="dragger_container">
                        <div class="dragger"></div>
                    </div>
                </div> <!-- div hor wrapper -->
            </div> <!-- div custom scroll box -->
        </div>
    </div>
</%def>

<%def name="showFAQ(survey)">
    <%
        slides = map(int, survey['extraSlides'].split(','))
    %>
    
    <ul class="thumbnails" style="height:600px; overflow: scroll;">
        % for slideID in slides:
            <%
                slide = getSurveySlideByID(slideID)
            %>
            <div class="row-fluid">
                ${inlineSpacer(2)}
                <li class="span10">
                    <a href="/surveys/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}" class="thumbnail">
                        <%
                            thumbnailFile = slide['image'].split('.')
                            thumbnailFile.pop()
                            thumbnailFile.insert(1, 'thumbnail')
                            thumbnailFile = '.'.join(thumbnailFile)
                        %>
                        <img src = "/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${thumbnailFile}.thumbnail">
                        ##<h5 style = "text-align:center;">Slide ${slide['slideNum']}</h5>
                    </a>
                </li>
            </div>
        % endfor
    </ul>
</%def>

<%def name="returnButton(survey)">
    <%
        key = '%s_%s_currentPage' %(survey['urlCode'], survey['url'])
        slideIDs = map(int, survey['slides'].split(','))
        if key in session:
            slideID = slideIDs[session[key]]
        else:
            slideID = slideIDs[0]
        
        slide = getSurveySlideByID(slideID)
    %>
    <a class="btn btn-info" href="/surveys/${survey['urlCode']}/${survey['url']}/page/${slide['hash']}">Return</a>
</%def>

<%def name="showHeader(survey, slide)">
    % if 'noHeaderLogo' in slide.keys():
        % if int(slide['noHeaderLogo']) == 1:
            <% return %>
        % endif
    % endif
    % if 'header' in slide.keys():
        <div class="row-fluid">
            <div class="span8">
                % if 'lightColor' in survey.keys():
                    <div class="headerSurvey" style="background-image: -moz-linear-gradient(top, ${survey['lightColor']}, ${survey['darkColor']});
                    background-image: -ms-linear-gradient(top, ${survey['lightColor']}, ${survey['darkColor']});
                    background-image: -webkit-gradient(linear, 0 0, 0 100%, from(${survey['lightColor']}), to(${survey['darkColor']}));
                    background-image: -webkit-linear-gradient(top, ${survey['lightColor']}, ${survey['darkColor']});
                    background-image: -o-linear-gradient(top, ${survey['lightColor']}, ${survey['darkColor']});
                    background-image: linear-gradient(top, ${survey['lightColor']}, ${survey['darkColor']});
                    ">
                % else:
                    <div class="headerSurvey">
                % endif
                    ${slide['header']}
                </div>
            </div>
            <div class="span4">
                <div class="logoSurvey">
                    <img src="/surveys/${survey['surveyType']}/${survey['directoryNum']}/${survey['hash']}/${survey['imgDir']}/${survey['logo']}">
                </div>
            </div>
        </div>
    % endif
</%def>
