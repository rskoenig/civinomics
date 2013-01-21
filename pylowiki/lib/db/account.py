from pylons import tmpl_context as c, config, session
from pylowiki.model import Thing, meta, Data
from pylowiki.lib.utils import toBase62
from pylowiki.lib.db.dbHelpers import commit
from dbHelpers import with_characteristic as wc
import generic

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


def Account(billingName, billingEmail, stripeID, workshop, plan, coupon = 'None'):
    account = Thing('account')
    account['billingName'] = billingName
    account['billingEmail'] = billingEmail
    account['stripeID'] = stripeID
    account['plan'] = plan
    account['coupon'] = coupon
    account['suspended'] = '0'
    account['deleted'] = '0'
    commit(account)
    account['urlCode'] = toBase62(account)
    account = generic.linkChildToParent(account, workshop)
    commit(account)
    return account

