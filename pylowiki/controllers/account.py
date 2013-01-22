import logging
import stripe

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.account      as accountLib

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AccountController(BaseController):

    @h.login_required
    def __before__(self, action, workshopCode = None):
	c.stripePublicKey = config['app_conf']['stripePublicKey'].strip()
	c.stripePrivateKey = config['app_conf']['stripePrivateKey'].strip()
	c.workshop = workshopLib.getWorkshopByCode(workshopCode)
	c.account = accountLib.getAccountsForWorkshop(workshop, deleted = '0')
    c.stripeCustomer = stripe.Customer.retrieve(c.account['stripeID')

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

    def updatePaymentInfoHandler(self):
        stripe.api_key = c.stripePrivateKey
        if 'stripeToken' in request.params:
            stripeToken = request.params['stripeToken']
        else:
            alert = {'type':'error'}
            alert['title'] = 'No information submitted.'
            session['alert'] = alert
            session.save()
            return redirect("/workshop/" + c.workshop['urlCode'] + "/" + c.workshop['url'] + "/dashboard")
