from cinema.models import members, orders, products, tickets, bad_requests
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

# Create your procedures here.

def hash_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def create_new_order():
	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator(10)
		new_hash_id = new_hash_id.lower()
		try:
			order = orders.objects.get(hash_id = new_hash_id)
		except:
			verify_existence = False

	new_order = orders(hash_id = new_hash_id, amount = settings.VALUE)
	new_order.save()

	return new_hash_id

def create_new_member(ipn_obj):
	try:
		new_member_first_name = ipn_obj.first_name
	except:
		new_member_first_name = '-'

	try:
		new_member_last_name = ipn_obj.last_name
	except:
		new_member_last_name = '-'

	try:
		new_member_email = ipn_obj.payer_email
	except:
		new_member_email = '-'

	try:
		new_member_phone = ipn_obj.contact_phone
	except:
		new_member_phone = '-'

	try:
		new_member_zip = ipn_obj.address_zip
	except:
		new_member_zip = '-'

	try:
		new_member_address = ipn_obj.address_street
	except:
		new_member_address = '-'

	try:
		new_member_city = ipn_obj.address_city
	except:
		new_member_city = '-'

	try:
		new_member_state = ipn_obj.address_state
	except:
		new_member_state = '-'

	try:
		new_member_country = ipn_obj.address_country
	except:
		new_member_country = '-'

	new_member = members(first_name = new_member_first_name, last_name = new_member_last_name, email = new_member_email, email_paypal = new_member_email, phone = new_member_phone, zip_code = new_member_zip, address = new_member_address, city = new_member_city, state = new_member_state, country = new_member_country)
	new_member.save()
	return new_member.id

def update_order_success_payment(ipn_obj, member_id):
	order = orders.objects.get(hash_id = ipn_obj.custom)
	order.member_id = member_id
	order.status_paypal = ipn_obj.payment_status
	if ipn_obj.payment_status == 'Completed':
		order.status = 1
	order.id_paypal = ipn_obj.auth_id
	try:
		order.payment_fee = ipn_obj.mc_fee
	except :
		order.payment_fee = 0

	try:
		order.pending_reason = ipn_obj.pending_reason
	except :
		order.pending_reason = 'paid'
	order.save()
	return None

# Create your views here.

def index(request):
    link = 'https://tufjuljpld.localtunnel.me'

    hash_id = create_new_order()
    context = {'hash_id': hash_id, 'link': link, 'email_receiver': settings.EMAIL_PAYPAL_ACCOUNT, 'value': settings.VALUE}
    return render(request, "index.html", context)

@csrf_exempt
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
    	order = orders.objects.get(hash_id = ipn_obj.custom)
    	if order.hash_id == ipn_obj.custom and order.amount == ipn_obj.mc_gross:
    		try:
    			member_exist = members.objects.get(email = ipn_obj.payer_email)
    			member_id = member_exist.id
    			print 'member id'
    			print member_id
    		except:
    			member_id = create_new_member(ipn_obj)
    		
    		update_order_success_payment(ipn_obj, member_id)
    		print ipn_obj.payer_email
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != settings.EMAIL_PAYPAL_ACCOUNT:
            # Not a valid payment
            print 'Email pagador'
            print ipn_obj.payer_email
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            Users.objects.update(paid=True)
    else:
    	pass

    return None
        #...

@csrf_exempt
def show_me_the_money_invalid(sender, **kwargs):
    return None

payment_was_successful.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money_invalid)