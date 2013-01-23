import logging
import stripe

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.account      as accountLib
import pylowiki.lib.helpers         as h
import pylowiki.lib.db.dbHelpers    as dbHelpers

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def __before__(self, action, accountCode = None):
        if accountCode is None:
            abort(404)
        c.stripePublicKey = config['app_conf']['stripePublicKey'].strip()
        c.stripePrivateKey = config['app_conf']['stripePrivateKey'].strip()
        stripe.api_key = c.stripePrivateKey
        c.account = accountLib.getAccountByCode(accountCode)
        c.workshop = workshopLib.getWorkshopByCode(c.account['workshopCode'])
        c.stripeCustomer = stripe.Customer.retrieve(c.account['stripeID'])

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
            alert = {'type':'error'}
            alert['title'] = 'No information submitted.'
            session['alert'] = alert
            session.save()
            return redirect("/workshop/" + c.workshop['urlCode'] + "/" + c.workshop['url'] + "/dashboard")
            
        c.account['billingName'] = billingName
        c.account['billingEmail'] = billingEmail
        dbHelpers.commit(c.account)
        title = 'Account information updated.'
        data = 'Billing contact information updated by ' + c.authuser['name']
        eventLib.Event(title, data, c.account)
        alert = {'type':'success'}
        alert['title'] = title
        session['alert'] = alert
        session.save()
        return redirect("/workshop/" + c.workshop['urlCode'] + "/" + c.workshop['url'] + "/dashboard")

    def updatePaymentInfoHandler(self):
        stripe.api_key = c.stripePrivateKey
        if 'stripeToken' in request.params:
            stripeToken = request.params['stripeToken']
            c.stripeCustomer.card = stripeToken
            c.stripeCustomer.save()
            alert = {'type':'success'}
            title =  'Account Payment Information Updated.'
            alert['title'] = title
            session['alert'] = alert
            session.save()
            eventLib.Event(title, data, c.account)
            return redirect("/workshop/" + c.workshop['urlCode'] + "/" + c.workshop['url'] + "/dashboard")
        else:
            alert = {'type':'error'}
            alert['title'] = 'No information submitted.'
            session['alert'] = alert
            session.save()
            return redirect("/workshop/" + c.workshop['urlCode'] + "/" + c.workshop['url'] + "/dashboard")
