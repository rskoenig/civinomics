# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

from pylowiki.lib.db.user import get_user, getUserByID, isAdmin
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.workshop import Workshop, getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.motd import MOTD
from pylowiki.lib.db.account import Account, getUserAccount, getAccountByCode, getAccountByName, getUserAccounts, isAccountAdmin
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.images import saveImage, resizeImage
from pylowiki.lib.utils import urlify
from pylowiki.lib.db.user import get_user, getUserByEmail


from hashlib import md5

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def accountAdmin(self, id1):
        code = id1
        c.account = getAccountByCode(code)
        if 'confTab' in session:
            c.tab = session['confTab']
            session.pop('confTab')
            session.save()
        c.events = getParentEvents(c.account)
        adminList = c.account['admins'].split('|')
        c.admins = []
        c.emails = []
        for admin in adminList:
            if admin and admin != '':
                user = getUserByEmail(admin)
                if user:
                    c.admins.append(user)
                else:
                    c.emails.append(admin)

        if isAccountAdmin(c.authuser, c.account) or isAdmin(c.authuser.id):
            return render("/derived/account_admin.bootstrap")
        else:
            return redirect("/")
            
    @h.login_required
    def accountCreateHandler(self, id1, id2):
        urlCode = id1
        url = urlify(id2)
        
        user = get_user(urlCode, url)
        accounts = getUserAccounts(user)
        if accounts:
            for account in accounts:
                if account.owner == user.id and account['type'] == 'trial':
                    alert = {'type':'error'}
                    alert['title'] = 'You already have a trial account. Upgrade it to add workshops or participants.'
                    alert['content'] = ''
                    session['alert'] = alert
                    session.save()
                    return redirect("/profile/" + urlCode + "/" + url )
                    
        a = Account(user, '1', '10', '0', 'trial')
        w = Workshop(user['name'], a.a, 'trial')
        MOTD('Welcome to the workshop!', w.w.id, w.w.id)
        return redirect("/workshop/" + w.w['urlCode'] + "/" + w.w['url'] + "/configure" )
        
    @h.login_required
    def accountAdminHandler(self, id1):
        code = id1
        c.account = getAccountByCode(code)
        
        if not isAdmin(c.authuser.id) and not isAccountAdmin(c.authuser, c.account):
           alert = {'type':'error'}
           alert['title'] = 'You are not authorized.'
           alert['content'] = ''
           session['alert'] = alert
           session.save()
           return redirect("/" )
        
        c.events = getParentEvents(c.account)
        
        adminList = c.account['admins'].split('|')
        c.admins = []
        c.emails = []
        for admin in adminList:
            if admin and admin != '':
                user = getUserByEmail(admin)
                if user:
                    c.admins.append(user)
                c.emails.append(admin)
                   
        changeMsg = ''
        change = 0
        error = 0
        errorMsg = ''

        if 'pictureFile' in request.POST:
            session['confTab'] = "tab2"
            session.save()
            picture = request.POST['pictureFile']
            if picture == "":
                picture = False
        else:
            picture = False

        if picture != False:
           identifier = 'avatar'
           imageFile = picture.file
           filename = picture.filename
           hash = saveImage(imageFile, filename, c.authuser, 'avatar', c.account)
           c.account['pictureHash'] = hash
           resizeImage(identifier, hash, 200, 200, 'profile')
           resizeImage(identifier, hash, 25, 25, 'thumbnail')
           change = 1
           changeMsg = changeMsg + "Logo updated. "


        if 'orgName' in request.params:
            session['confTab'] = "tab2"
            session.save()
            orgName = request.params['orgName']
            url = urlify(orgName)
            if orgName == '' or orgName == 'none':
                errorMsg = "Organization Name required. "
                error = 1 
            elif orgName != c.account['orgName']:
                nameTest = getAccountByName(orgName)
                if nameTest:
                    error = 1
                    errorMsg = errorMsg + "Organization name already in use by another account. "
                else:
                    change = 1
                    changeMsg = changeMsg + "Organization name updated. "
                    c.account['orgName'] = orgName
                    c.account['url'] = url
                    

        if 'orgEmail' in request.params:
            session['confTab'] = "tab2"
            session.save()
            orgEmail = request.params['orgEmail']
            if orgEmail == '':
                errorMsg = "Organization Email contact required. "
                error = 1 
            else:
                if orgEmail != c.account['orgEmail']:
                    change = 1
                    changeMsg = changeMsg + "Organization contact email updated. "
                    c.account['orgEmail'] = orgEmail

        if 'orgLink' in request.params:
            session['confTab'] = "tab2"
            session.save()
            orgLink = request.params['orgLink']
            if orgLink != c.account['orgLink']:
                change = 1
                changeMsg = changeMsg + "Organization web site updated. "
                c.account['orgLink'] = orgLink
                
        if 'orgLinkDesc' in request.params:
            session['confTab'] = "tab2"
            session.save()
            orgLinkDesc = request.params['orgLinkDesc']
            if orgLinkDesc != c.account['orgLinkDesc']:
                change = 1
                changeMsg = changeMsg + "Organization web site description updated. "
                c.account['orgLinkDesc'] = orgLinkDesc

        if 'orgMessage' in request.params:
            session['confTab'] = "tab2"
            session.save()
            orgMessage = request.params['orgMessage']
            if orgMessage != c.account['orgMessage']:
                change = 1
                changeMsg = changeMsg + "Organization welcome message updated. "
                c.account['orgMessage'] = orgMessage
                
        if 'adminEmail' in request.params:
            session['confTab'] = "tab3"
            session.save()
            adminEmail = request.params['adminEmail']
            if adminEmail and adminEmail != '' and adminEmail not in c.emails:
                adminList = '|' + adminEmail + '|'
                change = 1
                changeMsg = changeMsg + "Admin email " + adminEmail + " added. "
                for email in c.emails:
                    adminList = adminList + '|' + email + '|'
                    
                c.account['admins'] = adminList
                
        if 'deleteAdmin' in request.params:
            session['confTab'] = "tab3"
            session.save()
            deleteAdmin = request.params['deleteAdmin']
            adminList = ''
            if 'confirmAdmin|' + deleteAdmin in request.params:
                for email in c.emails:
                    if deleteAdmin != email:
                        adminList = adminList + '|' + email + '|'
                    
                c.account['admins'] = adminList
                change = 1
                changeMsg = changeMsg + "Admin email " + deleteAdmin + " deleted. "
                
            else:
                error = 1
                errorMsg = errorMsg + 'Please confirm delete of admin.'


        if change:
            if errorMsg:
               changeMsg = changeMsg + 'Errors: ' + errorMsg
            alert = {'type':'success'}
            alert['title'] = 'Account updated.'
            alert['content'] = changeMsg
            session['alert'] = alert
            session.save()
            Event('Account Updated', changeMsg, c.account, c.account)
        elif error:
            alert = {'type':'error'}
            alert['title'] = 'Errors were found.'
            alert['content'] = errorMsg
            session['alert'] = alert
            session.save()

        else:
            alert = {'type':'success'}
            alert['title'] = 'No changes submitted.'
            alert['content'] = ''
            session['alert'] = alert
            session.save()

        return redirect("/account/" + code )

    @h.login_required
    def accountUpgradeHandler(self, id1):
        code = id1

        c.account = getAccountByCode(code)
        c.events = getParentEvents(c.account)
        adminList = c.account['admins'].split('|')
        authorized = 0
        c.admins = []
        for admin in adminList:
            log.info('admin is %s'%admin)
            if admin and admin != '':
               user = getUserByEmail(admin)
               if user:
                   c.admins.append(user)
                   if user.id == c.authuser.id:
                       authorized = 1
                       
        if isAdmin(c.authuser.id):
            authorized = 1

        if authorized == 0:
            alert = {'type':'error'}
            alert['title'] = 'You are not authorized.'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect("/" )

        if 'upgrade' in request.params:
            uButton = request.params['upgrade']
            numUsed = int(c.account['numHost']) - int(c.account['numRemaining'])
            if c.account['type'] == 'trial':
                c.account['url'] = 'none'
                c.account['orgName'] = 'none'
                
            if uButton == 'basic':
               c.account['type'] = 'basic'
               c.account['numHost'] = '5'
               c.account['numParticipants'] = '100'
               c.account['numRemaining'] = '4'
            elif uButton == 'plus':
               c.account['type'] = 'plus'
               c.account['numRemaining'] = 10 - numUsed
               c.account['numHost'] = '10'
               c.account['numParticipants'] = '500'
            elif uButton == 'premium':
               c.account['type'] = 'premium'
               c.account['numRemaining'] = 20 - numUsed
               c.account['numHost'] = '20'
               c.account['numParticipants'] = '1000'

            commit(c.account)
            user = getUserByID(c.authuser.id)
            Event('Account Updated', '%s updated account to %s'%(user['name'], c.account['type']), c.account, c.account) 
            return render("/derived/account_admin.bootstrap")
        else:
            return render("/derived/account_upgrade.bootstrap")
