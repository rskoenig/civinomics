import logging
import stripe
import time

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.account      as accountLib
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.helpers         as h
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.mail            as mailLib

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def __before__(self, action, accountCode = None, workshopCode = None, workshopURL = None):
        if accountCode is None and workshopCode is None:
            abort(404)
        c.stripePublicKey = config['app_conf']['stripePublicKey'].strip()
        c.stripePrivateKey = config['app_conf']['stripePrivateKey'].strip()
        stripe.api_key = c.stripePrivateKey
        if action == 'manageAccount':
            c.w = workshopLib.getWorkshopByCode(workshopCode)
            account = accountLib.getAccountsForWorkshop(c.w, deleted = '0')
            c.account = account[0] # kludge, ugh.
        else:
            c.account = accountLib.getAccountByCode(accountCode)
            c.w = workshopLib.getWorkshopByCode(c.account['workshopCode'])
        
            workshopLib.setWorkshopPrivs(c.w)
            if not c.privs['admin'] and not c.privs['facilitator']:
                return(redirect("/"))

        if accountLib.isComp(c.account):
            c.stripCustomer = ''
        else:
            c.stripeCustomer = stripe.Customer.retrieve(c.account['stripeID'])
        
        c.mainImage = mainImageLib.getMainImage(c.w)
        workshopLib.setWorkshopPrivs(c.w)

    def manageAccount(self):
        c.stripeKey = c.stripePublicKey
        if c.account:
            c.accountInvoices = accountLib.getInvoicesForAccount(c.account)
        else:
            return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/preferences")

        if c.w['public_private'] == 'public':
            c.scope = geoInfoLib.getPublicScope(c.w)

        return render('/derived/6_account.bootstrap')
        
    def updateBillingContactHandler(self):
        stripe.api_key = c.stripePrivateKey
        if 'billingName' in request.params:
            billingName = request.params['billingName']
        else:
            billingName = ''
            
        if 'billingEmail' in request.params:
            billingEmail = request.params['billingEmail']
        else:
            billingEmail = ''
            
        if not billingName and not billingEmail:
            alert = {'type':'danger'}
            alert['title'] = 'No information submitted.'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/manage/account")
            
        c.account['billingName'] = billingName
        c.account['billingEmail'] = billingEmail
        dbHelpers.commit(c.account)
        title = 'Account information updated.'
        data = 'Billing contact information updated by ' + c.authuser['name']
        eventLib.Event(title, data, c.account)
        alert = {'type':'success'}
        alert['title'] = title
        alert['content'] = ''
        session['alert'] = alert
        session.save()
        return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/manage/account")

    def updatePaymentInfoHandler(self):
        stripe.api_key = c.stripePrivateKey
        if 'stripeToken' in request.params:
            stripeToken = request.params['stripeToken']
            c.stripeCustomer.card = stripeToken
            c.stripeCustomer.save()
            alert = {'type':'success'}
            title =  'Account Payment Information Updated.'
            alert['title'] = title
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            data = "Payment information updated by " + c.authuser['name']
            eventLib.Event(title, data, c.account)
            return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/manage/account")
        else:
            alert = {'type':'danger'}
            alert['title'] = 'No information submitted.'
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/manage/account")

    def closeHandler(self):
        stripe.api_key = c.stripePrivateKey
        if 'confirmCloseAccount' in request.params:
            c.w['type'] = 'personal'
            c.w['public_private'] = 'private'
            title = "Workshop account closed."
            data = "Workshop account closed by " + c.authuser['name'] + ". Workshop converted to a personal private workshop."
            eventLib.Event(title, data, c.w)
            dbHelpers.commit(c.w)
            c.stripeCustomer.delete()
            c.account['deleted'] = '1'
            c.account['closedWorkshopCode'] = c.account['workshopCode']
            c.account['workshopCode'] = '|CLOSED|'
            dbHelpers.commit(c.account)
            alert = {'type':'success'}
            alert['title'] = title
            alert['content'] = ''
            session['alert'] = alert
            session.save()
            eventLib.Event(title, data, c.account)
            self.emailInvoicesHandler(c.account['billingEmail'])
            return redirect("/workshop/" + c.w['urlCode'] + "/" + c.w['url'] + "/preferences")     
        else:
            return(redirect("/"))
            
    def emailInvoicesHandler(self, recipient):
        c.accountInvoices = accountLib.getInvoicesForAccount(c.account)
        invoiceList = c.accountInvoices['data']
        invoices = ''
        for invoice in invoiceList:
                invoices += "\nInvoice Date: " + time.ctime(invoice['date']) + " Amount Due: " + str(invoice['amount_due']/100) + " Paid: "
                if invoice['ending_balance'] == 0:
                    invoices += "Yes"
                else:
                    invoices += "No"

                invoices += "\n   Line items:\n"
                for line in invoice['lines']['data']:
                    invoices += "   " + line['plan']['name'] + " for period of " + time.ctime(line['period']['start']) + " through " + time.ctime(line['period']['end']) + "\n"

        workshopName = c.w['title']
        senderName = 'Civinomics Accounts'
        senderEmail = 'billing@civinomics.com'
        subject = 'Account Summary for: ' + workshopName
    
        emailDir = config['app_conf']['emailDirectory']
        myURL = config['app_conf']['site_base_url']
        
        txtFile = emailDir + "/invoices.txt"

        # open and read the text file
        fp = open(txtFile, 'r')
        textMessage = fp.read()
        fp.close()
    
        # do the substitutions
        textMessage = textMessage.replace('${c.sender}', senderName)
        textMessage = textMessage.replace('${c.workshopName}', workshopName)
        textMessage = textMessage.replace('${c.invoices}', invoices)

        fromEmail = 'Civinomics Billing <billing@civinomics.com>'
        toEmail = recipient

        mailLib.send(toEmail, fromEmail, subject, textMessage)
        

        