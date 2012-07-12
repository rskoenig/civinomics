import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h

from pylowiki.lib.db.survey import Survey, getSurvey, getAllSurveys, getSurveysByMember, parseSurvey, getActiveSurveys
from pylowiki.lib.db.surveySlide import getSurveySlide, getSurveySlideByID
from pylowiki.lib.db.featuredSurvey import setFeaturedSurvey
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.event import Event
from pylowiki.lib.db.surveyAnswer import SurveyAnswer, getSurveyAnswer, editSurveyAnswer, getAllAnswersForSurvey
from pylowiki.lib.db.user import getUsersWithLevelGreater, getUserByID, getUserByEmail
#from pylowiki.lib.db.geoInfo import SurveyScope
from pylowiki.lib.utils import urlify

from hashlib import md5
from time import time, strftime, ctime

import simplejson as json
import os, shutil, tarfile, zipfile, gzip, datetime

numFilesInDirectory = 29000

def _generateHash(filename, user):
        s = '%s_%s_%s' %(filename, user['email'], int(time()))
        return md5(s).hexdigest()

class SurveyController(BaseController):

    @h.login_required
    def adminSurvey(self):
        if int(c.authuser['accessLevel']) < 200:
            log.info('user %s tried to access adminSurvey()'%c.authuser.id)
            return redirect('/')
        c.title = c.heading = 'Survey adminstration'
        c.facilitators = getUsersWithLevelGreater(99)
        c.surveys = getActiveSurveys()
        return render('/derived/admin_survey.bootstrap')

    @h.login_required
    def addSurvey(self):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        c.title = c.heading = 'Add Survey'
        
        return render('/derived/add_survey.bootstrap')
    
    @h.login_required
    def addSurveyHandler(self):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        message = {}
        """
            Super basic input checking.  No validation.
        """
        if request.params['surveyName'] == '':
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = "No name"
            c.message = message
            return render('/derived/add_survey.bootstrap')
        
        if request.params['description'] == '':
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = "No description"
            c.message = message
            return render('/derived/add_survey.bootstrap')
        
        if request.params['geoScope'] == '':
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = "No geographic scoping"
            c.message = message
            return render('/derived/add_survey.bootstrap')

        if request.params['estimatedTime'] == '':
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = 'No estimated time'
            c.message = message
            return render('/derived/add_survey.bootstrap')
        
        """
            Create the basic survey Thing.  We will add in an uploaded file's contents later.
        """
        surveyName = request.params['surveyName']
        description = request.params['description']
        geoScope = request.params['geoScope']
        estimatedTime = request.params['estimatedTime']

        survey = Survey(c.authuser, surveyName, description, 'public', estimatedTime)
        
        geoScope = geoScope.replace(' ', '')
        geoScope = geoScope.split(',')
        # look for range notation, replace with comma list
        finalGeo = []
        for thisGeo in geoScope:
            # if there is not a dash (-) in this entry, add it to final list
            if thisGeo.find('-') < 0:
                if int(thisGeo) not in finalGeo:
                    finalGeo.append(str(thisGeo))
            # if there is, replace it with a list of the numbers involved
            else:
                # create comma list from range here
                # e.g. 45000-45006
                rangeZips = thisGeo.split('-')
                # if it's an exact zip code, we need to leave it alone: 95060-0150 for example
                if len(rangeZips[0]) != len(rangeZips[1]):
                    #this doesn't seem to be a range entry
                    if len(rangeZips[0]) == 5 and len(rangeZips[1]) == 4:
                        # this is a zipcode of format 95060-0150
                        if thisGeo not in finalGeo:
                            finalGeo.append(str(thisGeo))
                        continue
                    else:
                        #this should throw an error
                        break
                elif len(rangeZips[0]) != 5 or len(rangeZips[1]) != 5:
                        #this should also throw an error
                        break
                rangeIterator = int(rangeZips[0])
                rangeMax = int(rangeZips[1])
                # just in case it's something like 45006-45000
                if rangeIterator > rangeMax:
                    rangeIterator = int(rangeZips[1])
                    rangeMax = int(rangeZips[0])
                elif rangeIterator == rangeMax:
                    if rangeIterator not in finalGeo:
                        finalGeo.append(str(rangeIterator))
                # if we're dealing with a correctly formatted range entry, add each number to the finalGeo list
                while rangeIterator <= rangeMax:
                    if rangeIterator not in finalGeo:
                        finalGeo.append(str(rangeIterator))
                    rangeIterator += 1

        
        for eachGeo in finalGeo:
            log.info("zip entry: "+eachGeo)
                
        # Later this will use the SurveyScope object, but right now storing a comma-separated list of zip codes
        # is OK and won't break any sort of cross/backwards compatability
        survey['publicPostalList'] = ','.join(map(str, finalGeo))
        
        commit(survey)
        message['type'] = 'success'
        message['title'] = 'SUCCESS: '
        message['content'] = "You have successfully created the basics for a new survey.  You should upload the compressed survey file next."
        c.message = message
        return redirect('/showSurveys')
    
    @h.login_required
    def edit(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = id2
        c.survey = getSurvey(code, urlify(url))
        if int(c.authuser['accessLevel']) < 200:
            if c.authuser.id != c.survey.owner:
                return redirect('/')
        c.title = c.header = 'Edit a survey'
        
        return render('/derived/edit_survey.bootstrap')
    
    @h.login_required
    def editHandler(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = id2
        survey = getSurvey(code, urlify(url))
        if int(c.authuser['accessLevel']) < 200:
            if c.authuser.id != survey.owner:
                return redirect('/')
        
        if request.params['surveyName'] != '':
            survey['title'] = request.params['surveyName']
            if survey['title'] > 20:
                survey['url'] = urlify(survey['title'][:20])
            else:
                survey['url'] = urlify(survey['title'])
        if request.params['description'] != '':
            survey['description'] = request.params['description']
        
        if request.params['geoScope'] != '':
            #geoScope = survey['publicPostalList']
            geoScope = request.params['geoScope']
            geoScope = geoScope.replace(' ', '')
            geoScope = geoScope.split(',')
            # Later this will use the SurveyScope object, but right now storing a comma-separated list of zip codes
            # is OK and won't break any sort of cross/backwards compatability
            survey['publicPostalList'] = ','.join(map(str, geoScope))
        
        if request.params['estimatedTime'] != '':
            survey['estimatedTime'] = request.params['estimatedTime']

        commit(survey)
        return redirect('/showSurveys')
    
    @h.login_required
    def upload(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = id2
        c.title = c.header = 'Upload a file'
        c.survey = getSurvey(code, urlify(url))
        return render('/derived/add_survey_upload.bootstrap')
    
    @h.login_required
    def uploadSurveyHandler(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = id2
        c.survey = survey = getSurvey(code, urlify(url))
        """
            Set up a basic scaling schema - no more than ~30k surveys in a given directory.
            Accept the file, create a hash for it, make all necessary directories, and extract the file.
        """
        if request.params['files[]'] != '':
            file = request.params['files[]']
            surveyArchive = file.file
            
            # This is quite hacky, and should instead be calling something like the unix utility 'file'
            filename = file.filename.split('.')
            extension = filename[-1]
            filetypes = ['tar', 'zip']
            if extension not in filetypes:
                l = []
                d = {}
                d['error'] = 'Incorrect file type'
                l.append(d)
                return json.dumps(l)
            else:
                identifier = 'normal' # In case we want to make different types of surveys
                baseDir = os.path.join(config['app_conf']['surveyDirectory'], identifier)
                if not os.path.exists(baseDir):
                    os.makedirs(baseDir)
                if len(os.listdir(baseDir)) == 0:
                    os.makedirs(os.path.join(baseDir, '0'))
                maxDir = str(max([int(name) for name in os.listdir(baseDir) if os.path.isdir(os.path.join(baseDir, name))]))
                curDir = os.path.join(baseDir, maxDir)
                numDirs = len([name for name in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, name))])
                if numDirs > numFilesInDirectory:
                    curDir = os.path.join(baseDir, str(int(curDir) + 1))
                    maxDir = int(maxDir) + 1
                    os.makedirs(curDir)
                    
                hash = _generateHash(filename, c.authuser)
                hashDir = os.path.join(curDir, hash)
                os.makedirs(hashDir)
                fullpath = os.path.join(hashDir, file.filename)
                localFile = open(fullpath, 'wb')
                shutil.copyfileobj(surveyArchive, localFile) # Write original archive to disk so we can uncompress
                localFile.close()
                
                survey['hash'] = hash
                survey['directoryNum'] = maxDir
                survey['origFileName'] = file.filename
                survey['uploadVersion'] = int(survey['uploadVersion']) + 1
                commit(survey)
                
                # Better to use python libraries or do a system call?
                if extension == 'tar':
                    tar = tarfile.open(fullpath)
                    tar.extractall(hashDir)
                    tar.close()
                elif extension == 'zip':
                    zip = zipfile.ZipFile(fullpath)
                    zip.extractall(hashDir)
                    zip.close()
            
            hashDirContents = os.listdir(hashDir)
            xmlPath = ''
            errorFound = False
            for item in hashDirContents:
                if item.endswith('.xml'):
                    xmlPath = os.path.join(hashDir, item)
                    break
            if xmlPath == '':
                survey['hash'] = 'flash'
                commit(survey)
                errorFound = True
                errorMessage = 'XML file not found'
            result, message = parseSurvey(xmlPath, survey)
            if not result:
                survey['hash'] = 'flash'
                commit(survey)
                errorFound = True
                errorMessage = message
                
            """
            Return a JSON-encoded string of the following format:
            
            [
              {
                "name":"picture1.jpg",
                "size":902604,
                "url":"\/\/example.org\/files\/picture1.jpg",
                "thumbnail_url":"\/\/example.org\/thumbnails\/picture1.jpg",
                "delete_url":"\/\/example.org\/upload-handler?file=picture1.jpg",
                "delete_type":"DELETE"
              },
              {
                "name":"picture2.jpg",
                "size":841946,
                "url":"\/\/example.org\/files\/picture2.jpg",
                "thumbnail_url":"\/\/example.org\/thumbnails\/picture2.jpg",
                "delete_url":"\/\/example.org\/upload-handler?file=picture2.jpg",
                "delete_type":"DELETE"
              }
            ]
            """
            l = []
            d = {}
            if errorFound:
                l = []
                d = {}
                d['error'] = errorMessage
                l.append(d)
                return json.dumps(l)
            else:
                d['name'] = file.filename
                d['size'] = os.stat(fullpath).st_size
                d['delete_type'] = "DELETE"
                d['-'] = hash
                d['type'] = 'file/%s' % extension
                l.append(d)
                return json.dumps(l)
            
        else:
            message = {}
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = 'You must upload a file'
            c.message = message
            c.title = c.heading = 'Upload a survey'
            return render('/derived/add_survey_upload.bootstrap')
            
    @h.login_required
    def display(self, id1, id2, id3):
        code = id1
        url = id2
        slideHash = id3
        
        c.survey = getSurvey(code, urlify(url))
        c.slide = getSurveySlide(slideHash, c.survey.id)
        
        # Now grab the correct list of slides
        if c.slide['surveySection'] == 'before':
            c.slides = slides = map(int, c.survey['slides'].split(','))
            c.surveySection = 'before'
        elif c.slide['surveySection'] == 'after':
            c.slides = slides = map(int, c.survey['extraSlides'].split(','))
            c.surveySection = 'after'
            
        c.numSlides = len(slides)
        c.slideNum = int(c.slide['slideNum'])
        
        if c.surveySection == 'before':
            c.title = c.header = 'Survey: %s (%s/%s)' %(c.survey['title'], c.slideNum, c.numSlides - 1)
            if int(c.slide['slideNum']) == 0:
                c.prevSlide = False
                curIndex = slides.index(c.slide.id)
                c.nextSlide = getSurveySlideByID(slides[curIndex + 1])
            elif int(c.slide['slideNum']) + 1 == len(c.survey['slides'].split(',')):
                c.nextSlide = False
                curIndex = slides.index(c.slide.id)
                c.prevSlide = getSurveySlideByID(slides[curIndex - 1])
            else:
                curIndex = slides.index(c.slide.id)
                c.nextSlide = getSurveySlideByID(slides[curIndex + 1])
                c.prevSlide = getSurveySlideByID(slides[curIndex - 1])
        else:
            c.title = c.header = 'Survey: %s (%s)' %(c.survey['title'], c.survey['extraSlidesName'])
        return render('/derived/show_survey.bootstrap')
    
    @h.login_required
    def showSurveys(self):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        c.title = c.header = 'Show my surveys'
        if int(c.authuser['accessLevel']) >= 200:
            c.surveys = getAllSurveys()
        else:
            c.surveys = getSurveysByMember(c.authuser)
        return render('/derived/list_owned_surveys.bootstrap')
    
    @h.login_required
    def activate(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        code = id1
        url = id2
        
        survey = getSurvey(code, urlify(url))
        state = int(survey['active'])
        if state == 0:
            survey['active'] = 1
            eventTitle = 'Survey activation'
            eventData = 'User %s activated survey %s' %(c.authuser.id, survey.id)
        else:
            survey['active'] = 0
            eventTitle = 'Survey deactivation'
            eventData = 'User %s deactivated survey %s' %(c.authuser.id, survey.id)
        commit(survey)
        
        e = Event(eventTitle, eventData, survey, c.authuser)
        
        return redirect('/showSurveys')
    
    @h.login_required
    def setFeaturedSurvey(self):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        result = request.params['radioButton']
        l = result.split('_')
        code = l[0]
        url = l[1]
        survey = getSurvey(code, url)
        if survey:
            setFeaturedSurvey(survey)
        return redirect('/surveyAdmin')
        # Now modify the featured survey object
    
    @h.login_required
    def viewResults(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        code = id1
        url = urlify(id2)
        c.survey = survey = getSurvey(code, url)
        if survey:
            results = getAllAnswersForSurvey(survey)
            if results:
                c.results = results
                c.title = c.header = 'Results for %s' % survey['title']
                
                # grab all csv file names for this survey
                path = os.path.join(config['app_conf']['surveyDirectory'], survey['surveyType'], survey['directoryNum'], survey['hash'])
                files = os.listdir(path)
                c.resultFiles = []
                for file in files:
                    if '.csv' in file:
                        thisTime = ctime(os.path.getctime(os.path.join(path, file)))
                        tup = (file, thisTime)
                        c.resultFiles.append(tup)
                c.resultFiles = sorted(c.resultFiles, key = lambda file:file[1])
                return render('/derived/view_results.bootstrap')
        
        # Silently fail here...should be changed
        return redirect('/')
    
    @h.login_required
    def generateResults(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = urlify(id2)
        survey = getSurvey(code, url)
        
        if int(c.authuser['accessLevel']) < 200:
            if c.authuser.id != survey.owner or c.authuser.id not in map(int, survey['facilitators'].split(',')):
                return redirect('/')
        
        results = getAllAnswersForSurvey(survey)
        # make a csv
        # s gets returned to the user
        # each line gets written to disk systematically
        directoryPath = os.path.join(config['app_conf']['surveyDirectory'], survey['surveyType'], survey['directoryNum'], survey['hash'])
        filename = '%s_Results_%s_%s.csv' %(survey['url'], datetime.date.today(), strftime('%H_%M_%S'))
        f = open(os.path.join(directoryPath, filename), 'w')
        s = ''
        
        # Go through all results creating entries about the slides involved.
        slideNumList = []
        for item in results:
            if not slideNumList:
                # Start the csv file with an entry about what slides have answers.
                line = '%s\t%s\t%s\t%s\t%s\t' %('slide #', 'header', 'title', 'name', 'type')
                s += '%s\n' % line
                f.write(line)
                
            # Write a line about this slide if we haven't yet, append slide # to the list.
            if int(item['slideNum']) not in slideNumList:
                slideNumList.append(int(item['slideNum']))
                slide = getSurveySlideByID(int(item['slide_id']))
                
                if 'header' in slide: 
                    slideHeader = slide['header'] 
                else:
                    slideHeader = ''
                if 'title' in slide:
                    slideTitle = slide['title']
                else:
                    slideTitle = ''
                line = '%s\t%s\t%s\t%s\t%s\t' %(slide['slideNum'], slideHeader, slideTitle, slide['name'], slide['type'])
                s += '%s\n' % line
                f.write(line)

        # Assuming there are results to print, this is the header for them
        #version 1
        line = '\n\n%s\t%s\t%s\t%s\t%s\t' %('entry #', 'time', 'slide number', 'key', 'answer')
        s += '%s\n' % line
        f.write(line)
        
        # Write all the results.
        userNum = 0
        userNumDict = {}
        for item in results:
            owner = getUserByID(item.owner)
            if owner['email'] not in userNumDict:
                userNum += 1
                userNumDict[owner['email']] = userNum
            thisUser = userNumDict[owner['email']]
            for key in item:
                #log.info("key: "+key+", val: "+item[key])
                if key.find('answer') >= 0:
                    line = '%s\t%s\t%s\t%s\t%s\t' %(thisUser, item.date, item['slideNum'], key, item[key])
                    s += '%s\n' % line
                    f.write(line)

        #version 2
        line = '\n\n%s\t%s\t%s\t%s\t%s\t' %('entry #', 'time', 'slide number', 'key', 'answer')
        s += '%s\n' % line
        f.write(line)

        for item in results:
            owner = getUserByID(item.owner)
            if owner['email'] not in userNumDict:
                userNum += 1
                userNumDict[owner['email']] = userNum
            thisUser = userNumDict[owner['email']]
            for key in item:
                log.info("key: "+key)
                log.info("val: "+item[key])
                if key.find('answer') >= 0:
                    thisKey = key
                    if thisKey.find('_') >= 0:
                        log.info("thisKey: "+thisKey)
                        thisKey = thisKey.replace('answer_','')
                        log.info("thisKey: "+thisKey)
                    line = '%s\t%s\t%s\t%s\t%s\t' %(thisUser, item.date, item['slideNum'], thisKey, item[key])
                    s += '%s\n' % line
                    f.write(line)

        #version 3
        line = '\n\n%s\t%s\t%s\t%s\t' %('entry #', 'time', 'slide number', 'answer')
        s += '%s\n' % line
        f.write(line)

        for item in results:
            owner = getUserByID(item.owner)
            if owner['email'] not in userNumDict:
                userNum += 1
                userNumDict[owner['email']] = userNum
            thisUser = userNumDict[owner['email']]
            allAnswers = ''
            for key in item:
                if key.find('answer') >= 0:
                    thisKey = key
                    if thisKey.find('_') >= 0:
                        thisKey = thisKey.replace('answer_','')
                    if not allAnswers:
                        allAnswers = '%s_%s' % (thisKey, item[key])
                    else:
                        allAnswers += ', %s_%s' % (thisKey, item[key])
            line = '%s\t%s\t%s\t%s\t' %(thisUser, item.date, item['slideNum'], allAnswers)
            s += '%s\n' % line
            f.write(line)

        f.close()
        response.headers['Content-disposition'] = 'attachment; filename=%s'%filename
        return s
    
    @h.login_required
    def addFacilitator(self):
        if int(c.authuser['accessLevel']) < 200:
            return redirect('/')
        
        email = request.params['email']
        user = getUserByEmail(email)
        if not user:
            # Needs to render a message here
            return redirect('/surveyAdmin')
        user['accessLevel'] = 100
        commit(user)
        return redirect('/surveyAdmin')
    
    @h.login_required
    def addAdmin(self):
        if int(c.authuser['accessLevel']) < 300:
            return redirect('/')
        
        email = request.params['email']
        user = getUserByEmail(email)
        if not user:
            # Needs to render a message here
            return redirect('/surveyAdmin')
        user['accessLevel'] = 200
        commit(user)
        return redirect('/surveyAdmin')
    
    @h.login_required
    def addFacilitatorToSurvey(self, id1, id2):
        if int(c.authuser['accessLevel']) < 100:
            return redirect('/')
        
        code = id1
        url = id2
        survey = getSurvey(code, url)
        
        if int(c.authuser['accessLevel']) < 200:
            if c.authuser.id not in map(int, survey['facilitators'].split(',')):
                return redirect('/')
        
        email = request.params['email']
        user = getUserByEmail(email)
        if not user:
            log.info('no user found with email %s' % email)
            message = {}
            message['type'] = 'error'
            message['title'] = 'ERROR: '
            message['content'] = 'Member with email %s not found' % email
            session['message'] = message
            session.save()
            return redirect(session['return_to'])
        
        facilitators = map(int, survey['facilitators'].split(','))
        if user.id not in facilitators:
            if user['accessLevel'] >= 100:
                survey['facilitators'] = survey['facilitators'] + ',' + str(user.id)
                commit(survey)
            else:
                message = {}
                message['type'] = ''
                message['title'] = 'ALERT: '
                message['content'] = 'Member with email %s not an existing facilitator' % email
                session['message'] = message
                session.save()
                return redirect(session['return_to'])
        return redirect(session['return_to'])
    
    """
        ##########################################
        #
        #    Survey answer submission handlers
        #
        ##########################################
    """
    def _basicSubmitSetup(self, id1, id2, id3):
        """
            Takes in the survey code, url-ified title, and page code.
            Returns the corresponding survey Thing and surveySlide Thing.
        """
        surveyCode = id1
        surveyURL = id2
        pageCode = id3
        survey = getSurvey(surveyCode, surveyURL)
        slide = getSurveySlide(pageCode, survey.id)
        
        return survey, slide
    
    def _basicAnswerCreation(self, survey, slide, answer, label = ''):
        """
            Handles creation of the surveyAnswer Thing.  If an answer for a given slide in a given
            survey has already been provided, instead of creating a new surveyAnswer Thing, the
            existing surveyAnswer Thing will get edited.
        """
        if not getSurveyAnswer(survey, slide, c.authuser):
            sa = SurveyAnswer(survey, slide, answer, label)
            result = 'create'
        else:
            sa = editSurveyAnswer(survey, slide, answer, label)
            result = 'modify'
        return sa, result
    
    def _basicMultiAnswerCreation(self, survey, slide, owner, label):
        """
            Handles creation of the surveyAnswer Thing for pages that have multiple inputs, e.g.
            multiple sliders, item rankings, checkboxes.
            
            If an answer for a given input is already given, the existing answer will
            get overwritten.
        """
        if not getSurveyAnswer(survey, slide, c.authuser):
            sa = SurveyAnswer(survey, slide, answer, label)
            result = 'create'
        else:
            sa = editSurveyAnswer(survey, slide, answer, label)
            result = 'modify'
        return sa, result
    
    def _basicReturnResult(self, result, answer):
        """
            Returns a message to be displayed on the page depending on the creation of a new
            answer or the update of a previously existing answer.
        """
        if result == 'create':
            return "Your answer has been saved"
        elif result == 'modify':
            return "Your answer has been updated"
        else:
            # Sliently fail...
            return "OK"
        
    @h.login_required
    def submitRadio(self, id1, id2, id3):
        """
            Handles radio button submission forms in a survey.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        answer = request.params['radioButton']
        sa, result = self._basicAnswerCreation(survey, slide, answer)
        return self._basicReturnResult(result, answer)
    
    @h.login_required
    def submitCheckbox(self, id1, id2, id3):
        """
            Handles checkbox submission forms in a survey.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        
        # This is not yet implemented in the templates
        #answer = request.params['']
        
        return self._basicReturnResult(result, answer)
    
    @h.login_required
    def submitSlider(self, id1, id2, id3, id4):
        """
            Handles slider submission forms in a survey.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        answer = id4
        sa, result = self._basicAnswerCreation(survey, slide, answer)
        return self._basicReturnResult(result, answer)
    
    @h.login_required
    def submitMultiSlider(self, id1, id2, id3, id4):
        """
            Handles multi-slider submission forms in a survey.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        answer = id4
        label = request.params['sliderLabel']
        sa, result = self._basicAnswerCreation(survey, slide, answer, label)
        return self._basicReturnResult(result, answer)
    
    @h.login_required
    def submitTextarea(self, id1, id2, id3):
        """
            Handles textarea (feedback in the XML) submission forms in a survey.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        answer = request.params['feedback']
        answer = answer.replace('\t','    ')
        sa, result = self._basicAnswerCreation(survey, slide, answer)
        return self._basicReturnResult(result, answer)
    
    @h.login_required
    def submitItemRank(self, id1, id2, id3):
        """
            Handles item ranking pages in a survey.
            Here the label is the form's value, and the ranking is the form's key/name.
        """
        survey, slide = self._basicSubmitSetup(id1, id2, id3)
        answer = ''
        for key in request.params.keys():
            try:
                # Some small validation to make sure the keys are numbers, as we expect
                int(key)
                label = request.params[key]
                rank = key
                if rank == 0:
                    continue
                answer += ' %s' % label
                sa, result = self._basicAnswerCreation(survey, slide, label, rank)
            except:
                log.info('User %s submitted bad value in submitItemRank() form' % c.authuser.id)
        return self._basicReturnResult(result, answer)
