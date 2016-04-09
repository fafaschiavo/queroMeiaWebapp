from django.shortcuts import render
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.ipn.signals import payment_was_flagged
from paypal.standard.ipn.signals import payment_was_successful
from paypal.standard.ipn.signals import invalid_ipn_received
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import string
import random

# Create your views here.

def hash_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def index(request):
    link = 'https://kdxoptnrjo.localtunnel.me/paypal/'

    hash_id = hash_id_generator(10)
    hash_id = hash_id.lower()
    context = {'hash_id': hash_id, 'link': link}
    print 'valor do hash atribuido:'
    print hash_id
    print '<<<<<<<<<<<<<<<<<<<<<<<<'
    return render(request, "index.html", context)

@csrf_exempt
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print 'hello'
    if ipn_obj.payment_status == ST_PP_COMPLETED:
    	print 'flag'
    	print ipn_obj.payer_email
    	print ipn_obj.custom
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != settings.EMAIL_PAYPAL_ACCOUNT:
            # Not a valid payment
            print 'Email pagador'
            print ipn_obj.payer_email
            print 'flag2'
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            Users.objects.update(paid=True)
    else:
    	print 'flag3'
        #...

@csrf_exempt
def show_me_the_money2(sender, **kwargs):
    ipn_obj = sender
    print 'hello2'
    if ipn_obj.payment_status == ST_PP_COMPLETED:
    	print 'flag'
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "receiver_email@example.com":
            print 'flag2'
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            Users.objects.update(paid=True)
    else:
    	print 'flag3'
        #...

# valid_ipn_received.connect(show_me_the_money)
payment_was_successful.connect(show_me_the_money)
# payment_was_flagged.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money2)