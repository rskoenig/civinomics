from pylons import tmpl_context as c, config, session
from pylowiki.model import Thing, meta, Data
from pylowiki.lib.utils import toBase62
from pylowiki.lib.db.dbHelpers import commit
from dbHelpers import with_characteristic as wc
import generic
import stripe
import pylowiki.lib.mail            as mailLib

def getAccountByCode(accountCode):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'account')\
            .filter(Thing.data.any(wc('urlCode', accountCode)))\
            .one()
    except:
        return False

def getAccountsForWorkshop(workshop, deleted = '0', suspended = '0'):
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'account')\
            .filter(Thing.data.any(wc('workshopCode', workshop['urlCode'])))\
            .filter(Thing.data.any(wc('deleted', deleted)))\
            .filter(Thing.data.any(wc('suspended', suspended)))\
            .all()
    except:
        return False

def getInvoicesForAccount(account):
    if isComp(account):
        accountInvoices = {}
        accountInvoices['count'] = 0
        accountInvoices['data'] = ''
        return accountInvoices

    stripe.api_key = config['app_conf']['stripePrivateKey'].strip()
    stripeCustomer = stripe.Customer.retrieve(account['stripeID'])
    return stripe.Invoice.all(customer = stripeCustomer['id'])

def isComp(account):
    if 'comp' in account:
        if account['comp'] == '1':
            return True
            
    return False

def Account(billingName, billingEmail, stripeToken, workshop, plan, coupon = 'None'):
    stripe.api_key = config['app_conf']['stripePrivateKey'].strip()
    description = "Civinomics account for customer " + billingName + " " + billingEmail + " workshop code " + workshop['urlCode']
    plan = "BETAPRO1"
    error = 0
    errorTitle = 'There was error an processing your payment information.'
    errorMsg = ''
    if stripeToken != 'ADMINCOMP':
        try:
            if coupon and coupon != '':
                customer = stripe.Customer.create( 
                        description = description, 
                        card = stripeToken,
                        plan = plan,
                        coupon = c.coupon,
                        email = billingEmail)
            else:
                customer = stripe.Customer.create( 
                        description = description, 
                        card = stripeToken,
                        plan = plan,
                        email = billingEmail)
                        
        except stripe.CardError, e:
            # Since it's a decline, stripe.CardError will be caught
            error = 1
            body = e.json_body
            err  = body['error']
            errorMsg = err['message']

            #print "Status is: #{e.http_status}\n"
            #print "Type is: #{err['type']}\n"
            #print "Code is: #{err['code']}\n"
            # param is '' in this case
            #print "Param is: #{err['param']}\n"
            #print "Message is: #{err['message']}\n"
        except stripe.InvalidRequestError, e:
            # Invalid parameters were supplied to Stripe's API
            error = 1
            errorMsg = 'Invalid API parameters.'
            pass
        except stripe.AuthenticationError, e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            error = 1
            errorMsg = 'Authentication error.'
            pass
        except stripe.APIConnectionError, e:
            # Network communication with Stripe failed
            error = 1
            errorMessage = 'Communication to the payment gateway is down.'
        except stripe.StripeError, e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            error = 1
            errorMsg = 'We cannot process your payment at this time.'
            pass
        except e:
            # Something else happened, completely unrelated to Stripe
            error = 1
            errorMsg = 'A system error has occured.'
            pass
        
        
        if error:
            errorMsg += ' Please try upgrading your workshop when the issue has been resolved.'
            alert = {'type':'error'}
            alert['title'] = errorTitle
            alert['content'] = errorMsg
            session['alert'] = alert
            session.save()
            workshop['type'] = 'personal'
            dbHelpers.commit(workshop)
            return redirect('/workshop/%s/%s/dashboard'%(c.w['urlCode'], c.w['url']))
  
    account = Thing('account')
    account['billingName'] = billingName
    account['billingEmail'] = billingEmail
    if stripeToken == 'ADMINCOMP':
        account['stripeID'] = stripeToken
        account['comp'] = '1'
    else:
        account['stripeID'] = customer['id']
        account['comp'] = '0'
    account['plan'] = plan
    account['coupon'] = coupon
    account['suspended'] = '0'
    account['deleted'] = '0'
    commit(account)
    account['urlCode'] = toBase62(account)
    account = generic.linkChildToParent(account, workshop)
    commit(account)

    if not isComp(account):
        mailLib.sendAccountMail(billingEmail)
    
    return account

def AccountTest(billingName, billingEmail, stripeToken, workshop, plan, coupon = 'None'):
    stripe.api_key = config['app_conf']['stripePrivateKey'].strip()
    description = "Civinomics test account for customer " + billingName + " " + billingEmail + " workshop code " + workshop['urlCode']
    plan = "PRO"
    error = 0
    errorTitle = 'There was an error processing your payment information.'
    errorMsg = ''

    account = Thing('account')
    account['billingName'] = billingName
    account['billingEmail'] = billingEmail
    account['stripeID'] = "customer['id']"
    account['plan'] = plan
    account['coupon'] = coupon
    account['suspended'] = '0'
    account['deleted'] = '0'
    commit(account)
    account['urlCode'] = toBase62(account)
    account = generic.linkChildToParent(account, workshop)
    commit(account)
    return account
