from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my-codes/$', views.codes, name='codes'),
    url(r'^my-codes-get/$', views.codes_get, name='codes_get'),
    url(r'^result/(?P<hash_id>\w{10})/$', views.result, name='result'),
    url(r'^success/(?P<hash_id>\w{10})/$', views.success, name='success'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^contact-form/', views.contact_form, name='contact_form'),

]