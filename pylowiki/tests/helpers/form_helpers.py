# -*- coding: utf-8 -*-
from pylowiki.tests import *
    
def fillPaymentForm(paymentForm, **kwargs):
    """Fill in the submit fields as needed for the workshop upgrade stripe payment form"""
    #: set the parameters as needed
    params = {}
    if 'name' in kwargs:
        name = kwargs['name']
    else:
        name = 'Test Name'
    if 'email' in kwargs:
        email = kwargs['email']
    else:
        email = 'test@civinomics.com'
    if 'test' in kwargs:
        if kwargs['test'] == True:
            ccnumber = '4242424242424242'
        elif 'ccnumber' in kwargs:
            ccnumber = kwargs['ccnumber']
        else:
            ccnumber = ''
    elif 'ccnumber' in kwargs:
        ccnumber = kwargs['ccnumber']
    else:
        ccnumber = ''
    if 'month' in kwargs:
        month = kwargs['month']
    else:
        month = '1'
    if 'year' in kwargs:
        year = kwargs['year']
    else:
        year = '2020'
    if 'coupon' in kwargs:
        coupon = kwargs['coupon']
    else:
        coupon = ''
    #: go through the form's submit fields and supply what's necessary for now
    for key, value in paymentForm.submit_fields():
        if key == 'name':
            params[key] = name
        if key == 'email':
            params[key] = email
        if key == 'coupon':
            params[key] = coupon
    #: not sure yet how to get a legit token from stripe, so just supplying a spoof token for now
    params['stripeToken'] = 'tok_1DGCyKtb2lYoF0'
    return params

def loadWithSubmitFields(webtestForm):
    params = {}
    for key, value in webtestForm.submit_fields():
        params[key] = value
    return params
