from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/(?P<hash_id>\w{10})/$', views.result, name='result'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
]
