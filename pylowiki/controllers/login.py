# -*- coding: utf-8 -*-
import logging, time

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers as h
import pylowiki.lib.db.user as userLib
import pylowiki.lib.mail as mailLib
from pylowiki.lib.auth import login_required
from pylowiki.lib.db.dbHelpers import commit

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def loginHandler(self):
        """ Display and Handle Login """
        c.title = c.heading = "Login"  
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'

        try:
            email = request.params["email"].lower()
            password = request.params["password"]
                
            log.info('user %s attempting to log in' % email)
            if email and password:
                user = userLib.getUserByEmail( email )
         
                if user: # not none or false
                    if user['activated'] == '0':
                        splashMsg['content'] = "This account has not yet been activated. An email with information about activating your account has been sent. Check your junk mail folder if you don't see it in your inbox."
                        baseURL = c.conf['activation.url']
                        url = '%s/activate/%s__%s'%(baseURL, user['activationHash'], user['email'])
                        mailLib.sendActivationMail(user['email'], url)
                        
                    elif user['disabled'] == '1':
                        log.warning("disabled account attempting to login - " + email )
                        splashMsg['content'] = 'This account has been disabled by the Civinomics administrators.'
                    elif userLib.checkPassword( user, password ): # if pass is True
                        # todo logic to see if pass change on next login, display reset page
                        user['laston'] = time.time()
                        loginTime = time.localtime(float(user['laston']))
                        loginTime = time.strftime("%Y-%m-%d %H:%M:%S", loginTime)
                        commit(user)
                        session["user"] = user['name']
                        session["userCode"] = user['urlCode']
                        session["userURL"] = user['url']
                        session.save()
                        
                        if 'afterLoginURL' in session:
                            # look for accelerator cases: workshop home, item listing, item home
                            loginURL = session['afterLoginURL']
                            session.pop('afterLoginURL')
                            session.save()
                        else:
                            loginURL = "/"
                        
                        return redirect(loginURL)
                    else:
                        log.warning("incorrect username or password - " + email )
                        splashMsg['content'] = 'incorrect username or password'
                else:
                    log.warning("incorrect username or password - " + email )
                    splashMsg['content'] = 'incorrect username or password'
            else:
                splashMsg['content'] = 'missing username or password'
            
            session['splashMsg'] = splashMsg
            session.save()
            
            return redirect("/login")

        except KeyError:
            if "user" in session:
                return redirect( "/" )
            else:
                return redirect('/')

    @login_required
    def logout(self):
        """ Action will logout the user. """
        return_url = '/'
        username = session['user']
        log.info( "Successful logout by - " + username )
        session.delete()
        return redirect( return_url )

    def forgot(self):
        """ Action will display a forgot password form. """
        c.title = c.heading = "Forgot password"  
        return render( "/derived/forgot.mako" )

    def forgot_handler(self):
        c.title = c.heading = "Forgot Password"
        c.splashMsg = False
        splashMsg = {}
        splashMsg['type'] = 'error'
        splashMsg['title'] = 'Error'
        email = request.params["email"].lower()
        user = userLib.getUserByEmail( email ) 
        if user:
            if email != config['app_conf']['admin.email']:
                password = generatePassword() 
                userLib.changePassword( user, password )
                commit( user ) # commit database change

                toEmail = user['email']
                frEmail = c.conf['contact.email'] 
                subject = 'Password Recovery'
                message = '''We have created a new password for you.\n\n 
                Please use this password to login.\n\n
                You can change your password to something you prefer on your profile page.\n\n
                We have reset your password to: ''' + password

                mailLib.send( toEmail, frEmail, subject, message )

                log.info( "Successful forgot password for " + email )
                splashMsg['type'] = 'success'
                splashMsg['title'] = 'Success'
                splashMsg['content'] = '''A new password was emailed to you.'''
                c.splashMsg = splashMsg
                return render('/derived/forgotPassword.bootstrap')
            else:
                log.info( "Failed forgot password for " + email )
                splashMsg['content'] = "Sorry email not found!"
                c.splashMsg = splashMsg 
                return render('/derived/forgotPassword.bootstrap')
        else:
            log.info( "Failed forgot password for " + email )
            splashMsg['content'] = "Sorry email not found!"
            c.splashMsg = splashMsg 
            return render('/derived/forgotPassword.bootstrap')

    """ This code moved to controllers/activate.py/activate()
    def activateHandler(self):
        email = request.params["email"].lower()
        user = get_user_by_email( email)
        if user:
            password = user.generate_password()
            user.change_password(password)
            activateHash = user.generateActivationHash()
            user.activationHash = activateHash
            commit(user)

            toEmail = user.email
            frEmail = c.conf['contact.email']
            url = 'http://www.greenocracy.org/activate/%s__%s' % (activateHash, email)
            subject = "Account Activation"
            message = '''Please click on the following link to activate your account: \n\n
            %s''' %(url)
            send(toEmail, frEmail, subject, message)
            log.info("Successful password reset and account creation (deactivated) for %s" %(email))
            return redirect('/')
    """

    @login_required
    def changepass(self):
        """ Action will display a change password form. """
        user = session['user']
        c.title = c.heading = "Change password for " + user  
        return render( "/derived/changepass.mako" )

    """ This code deprecated
    @login_required
    def changepass_handler(self):
        user = userLib.get_user( session['user'] )
        c.title = c.heading = "Change password for " + user.name  
        try:
            password1 = request.params["password1"]
            password2 = request.params["password2"]
            
            if password1 == password2 and password1 != '':
                user.change_password( password1 )
                commit( user )
                log.info( "Successful password change for " + user.name )
                h.flash( "Password change successful! ", "success" )
                return redirect(session['return_to'])
            else:
                h.flash( "The password and confirmation do not match", "warning" )
 
        except KeyError:
            h.flash( "Please fill all fields", "warning" )
            
        return render("/derived/changepass.mako" )
    """ 

    def loginDisplay(self, workshopCode, workshopURL, thing, thingCode, thingURL):
        if workshopCode != 'None' and workshopURL != 'None':
            afterLoginURL = "/workshop/%s/%s"%(workshopCode, workshopURL)
            if thing != 'None':
                afterLoginURL += "/" + thing
                if thingCode != 'None' and thingURL != 'None':
                    afterLoginURL += "/%s/%s"%(thingCode, thingURL)
            session['afterLoginURL'] = afterLoginURL
            session.save()
            log.info('loginDisplay afterLoginURL is %s'%afterLoginURL)
        
        if 'splashMsg' in session:
            c.splashMsg = session['splashMsg']
            session.pop('splashMsg')
            session.save()
            
        return render("/derived/login.bootstrap")

    def forgotPassword(self):
        return render("/derived/forgotPassword.bootstrap")
