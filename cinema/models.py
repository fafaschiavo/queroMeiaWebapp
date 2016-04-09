from __future__ import unicode_literals

from django.db import models

# Create your models here.
class members(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	email_paypal = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	zip_code = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email

	def __email_paypal__(self):
		return self.email_paypal

	def __phone__(self):
		return self.phone

	def __zip_code__(self):
		return self.zip_code

	def __address__(self):
		return self.address

	def __city__(self):
		return self.city

	def __state__(self):
		return self.state

	def __country__(self):
		return self.country

class orders(models.Model):
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	member_id = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	paid_at = models.DateTimeField(auto_now=False, auto_now_add=False)
	status_paypal = models.CharField(max_length=200)
	id_paypal = models.CharField(max_length=200)
	payment_fee = models.DecimalField(max_digits=7, decimal_places=2)
	pending_reason = models.CharField(max_length=200)
	quantity = models.IntegerField(default=1)

	def __amount__(self):
		return self.amount

	def __member_id__(self):
		return self.member_id

	def __email__(self):
		return self.email

	def __status__(self):
		return self.status

	def __created_at__(self):
		return self.created_at

	def __paid_at__(self):
		return self.paid_at

	def __status_paypal__(self):
		return self.status_paypal

	def __id_paypal__(self):
		return self.id_paypal

	def __payment_fee__(self):
		return self.payment_fee

	def __pending_reason__(self):
		return self.pending_reason

	def __quantity__(self):
		return self.quantity

class products(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def __price__(self):
		return self.price

	def __created_at__(self):
		return self.created_at

	def __description__(self):
		return self.description

class tickets(models.Model):
	is_used = models.IntegerField(default=0)
	order_id = models.IntegerField(default=0)
	product_id = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __is_used__(self):
		return self.is_used

	def __order_id__(self):
		return self.order_id

	def __product_id__(self):
		return self.product_id

	def __created_at__(self):
		return self.created_at

class bad_requests(models.Model):
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __created_at__(self):
		return self.created_at