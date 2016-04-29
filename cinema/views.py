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
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
import string
import random

# Create your procedures here.

def hash_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def create_new_order(product_id):

	product = products.objects.get(id = product_id)
	value = product.price

	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator(10)
		new_hash_id = new_hash_id.lower()
		try:
			order = orders.objects.get(hash_id = new_hash_id)
		except:
			verify_existence = False

	new_order = orders(hash_id = new_hash_id, amount = value, product_id = product_id)
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
		order.id_paypal = ipn_obj.txn_id
	except :
		order.payment_fee = 0

	try:
		order.pending_reason = ipn_obj.pending_reason
	except :
		order.pending_reason = 'paid'
	order.save()
	return None

def consume_ticket_code(hash_id):
	order = orders.objects.get(hash_id = hash_id)
	product = order.product_id
	available_tickets = tickets.objects.filter(product_id = product).exclude(is_used = 1)
	ticket = available_tickets[0]
	code = ticket.code

	ticket.is_used = 1
	ticket.order_id = order.id
	ticket.save()

	return code

def verify_ticket_availability(id):
	available_tickets = tickets.objects.filter(product_id = id).exclude(is_used = 1)
	is_available = len(available_tickets)
	if is_available > 0:
		return True
	else:
		return False

def mandrill_success(email, code):
	msg = EmailMessage(subject="Seu ingresso chegou!", from_email="QueroMeia <atendimento@queromeia.com>", to=[email])
	msg.template_name = "success"
	msg.global_merge_vars = {'CODE': str(code)}
	msg.send()
	return None

def mandrill_recovery(email, code):
	msg = EmailMessage(subject="Seu ingresso voltou!", from_email="QueroMeia <atendimento@queromeia.com>", to=[email])
	msg.template_name = "recovery"
	msg.global_merge_vars = {'CODE': str(code)}
	msg.send()
	return None

def mandrill_bad_request(error, id):
	msg = EmailMessage(subject="Bad Request QueroMeia", from_email="QueroMeia <atendimento@queromeia.com>", to=["fayschiavo@gmail.com"])
	msg.template_name = "bad-request"
	msg.global_merge_vars = {'ERROR': error, 'ID': id}
	msg.send()
	return None


def bad_request_tickets_not_available(order_id):
	order_id_request = order_id
	bad_request = bad_requests(problem_type = 'Ticket not available', order_id = order_id_request)
	bad_request.save()
	mandrill_bad_request(bad_request.problem_type, bad_request.id)
	return None

# Create your views here.

def index(request):
    product1 = products.objects.get(id = settings.PRODUCT_ID_1)
    value1 = product1.price
    availability1 = verify_ticket_availability(product1.id)

    product2 = products.objects.get(id = settings.PRODUCT_ID_2)
    value2 = product2.price
    availability2 = verify_ticket_availability(product2.id)

    hash_id = create_new_order(settings.PRODUCT_ID_1)
    hash_id2 = create_new_order(settings.PRODUCT_ID_2)

    context = {'hash_id': hash_id, 'hash_id2': hash_id2, 'email_receiver': settings.EMAIL_PAYPAL_ACCOUNT, 'value': value1, 'value2': value2, 'availability1': availability1, 'availability2': availability2}
    return render(request, "index.html", context)

@csrf_exempt
def success(request, hash_id):
    hash_id_request = hash_id
    context = {'hash_id': hash_id_request}
    return render(request, "success.html", context)

@csrf_exempt
def result(request, hash_id):
	#verify the order exists
    try:
    	order = orders.objects.get(hash_id = hash_id)
    except:
    	return HttpResponse(400)

    #if the order was not paid return - 401
    #if there is no available  ticket returne - 402
    #if everything is fine return the ticket code
    try:
    	if order.status == 1:
    		ticket = tickets.objects.get(order_id = order.id)
    		return HttpResponse(ticket.code)
    	else:
    		return HttpResponse(401)
    except:
    	return HttpResponse(402)

def codes(request):
	context = {}
	return render(request, "codes.html", context)

def codes_get(request):
	context = {}
	email = request.POST['email-form']
	try:
		member = members.objects.get(email = email)
		member_id = member.id
		order = orders.objects.filter(member_id = member_id).order_by('-created_at')[0]
		ticket = tickets.objects.get(order_id = order.id)
		mandrill_recovery(email, ticket.code)
	except:
		pass
	return render(request, "message-sent.html", context)

@csrf_exempt
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print 'flag1'
    if ipn_obj.payment_status == ST_PP_COMPLETED:
    	print 'flag2'
    	print 'status' + ipn_obj.payment_status
    	print 'hash_id' + ipn_obj.custom
    	print 'amount' + str(ipn_obj.mc_gross)
    	order = orders.objects.get(hash_id = ipn_obj.custom)
    	if order.hash_id == ipn_obj.custom and order.amount <= ipn_obj.mc_gross and settings.EMAIL_PAYPAL_ACCOUNT == ipn_obj.receiver_email:
    		print 'flag3'
    		try:
    			member_exist = members.objects.get(email = ipn_obj.payer_email)
    			member_id = member_exist.id
    		except:
    			member_id = create_new_member(ipn_obj)
    		update_order_success_payment(ipn_obj, member_id)
    		try:
    			print 'flag4'
    			code = consume_ticket_code(order.hash_id)
    			mandrill_success(ipn_obj.payer_email, code)
    		except:
    			bad_request_tickets_not_available(order.id)

        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != settings.EMAIL_PAYPAL_ACCOUNT:
            # Not a valid payment
            return None

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

def contact_form(request):
	context = {}
	msg = EmailMultiAlternatives(subject="Contato - Form - <" + request.POST['contact-email'] , body=request.POST['contact-message'] + '      -      ' + request.POST['contact-name'] + ' - ' + request.POST['contact-email'], from_email=request.POST['contact-name'] + "<atendimento@queromeia.com>",to=["atendimento@queromeia.com"])
	msg.send()
	return HttpResponse(200)

payment_was_successful.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money_invalid)