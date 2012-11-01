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
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopsByOwner
from pylowiki.lib.db.account import Account, getUserAccount, getAccountByCode
from pylowiki.lib.db.event import Event, getParentEvents
from pylowiki.lib.images import saveImage, resizeImage
from pylowiki.lib.utils import urlify


from hashlib import md5

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def accountAdmin(self, id1):
        code = id1
        authorized = 0
        c.account = getAccountByCode(code)
        c.events = getParentEvents(c.account)
        adminList = c.account['admins'].split('|')
        c.admins = []
        for admin in adminList:
            if admin and admin != '':
                user = getUserByID(admin)
                if user:
                    c.admins.append(user)
                    if user.id == c.authuser.id:
                        authorized = 1

        # update legacy objects
        if 'orgName' not in c.account:
            c.account['orgName'] = c.authuser['name']
            c.account['url'] = urlify(c.acount['orgName'])
            commit(c.account)

        if 'orgEmail' not in c.account:
            c.account['orgEmail'] = c.authuser['email'] 
            commit(c.account)

        if 'orgMessage' not in c.account:
            c.account['orgMessage'] = c.authuser['tagline'] 
            commit(c.account)


        if authorized or isAdmin(c.authuser.id):
            return render("/derived/account_admin.bootstrap")
        else:
            return redirect("/")

    @h.login_required
    def accountAdminHandler(self, id1):
        code = id1
        if not isAdmin(c.authuser.id):
           alert = {'type':'error'}
           alert['title'] = 'You are not authorized.'
           alert['content'] = ''
           session['alert'] = alert
           session.save()
           return redirect("/" )

        c.account = getAccountByCode(code)
        c.events = getParentEvents(c.account)
        changeMsg = ''
        change = 0
        error = 0
        errorMsg = ''

        if 'pictureFile' in request.POST:
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
            orgName = request.params['orgName']
            url = urlify(orgName)
            if orgName == '':
                errorMsg = "Organization Name required. "
                error = 1 
            else:
                if orgName != c.account['orgName']:
                    change = 1
                    changeMsg = changeMsg + "Organization name updated. "
                    c.account['orgName'] = orgName
                    c.account['url'] = url

        if 'orgEmail' in request.params:
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
            orgLink = request.params['orgLink']
            if orgLink != c.account['orgLink']:
                change = 1
                changeMsg = changeMsg + "Organization web site updated. "
                c.account['orgLink'] = orgLink

        if 'orgMessage' in request.params:
            orgMessage = request.params['orgMessage']
            if orgMessage != c.account['orgMessage']:
                change = 1
                changeMsg = changeMsg + "Organization welcome message updated. "
                c.account['orgMessage'] = orgMessage

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
            if admin and admin != '':
               user = getUserByID(admin)
               if user:
                   c.admins.append(user)
                   if int(admin) == c.authuser.id:
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
