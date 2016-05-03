# -*- coding: utf-8 -*-
import json

import urllib
import urllib2


from django.http import HttpResponse

from django.shortcuts import render

from django.template.loader import render_to_string
from django.template import RequestContext

# from django.utils.translation import ugettext_lazy as _

from django import forms

from django.core.mail import EmailMultiAlternatives
# from django.core.mail import EmailMessage


from .forms import TariffOrderForm

from .models import SiteConfig
from .models import Tariff
from .models import FormConfig


def urlencode(string):
	string = urllib.unquote(string)
	string = u'' + urllib.quote(string.encode('utf-8'))
	return string


def tariff(request, id):
	context = {}

	tariff = Tariff.objects.get(id=id)
	site_config = SiteConfig.objects.get(site=request.site)
	context['form'] = TariffOrderForm(request.POST or None)
	context['tariff'] = tariff
	context['additions'] = tariff.public_additions()

	context['form'].fields['additions'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=context['additions'], required=False)

	if context['form'].is_valid():
		new_order = context['form'].save()
		new_order.tariff = tariff
		new_order.site = request.site
		new_order.referrer = request.META.get('HTTP_REFERER', None)
		new_order.ip = request.META.get('REMOTE_ADDR', None)
		new_order.total_price = tariff.new_price
		for addition in new_order.additions.all():
			new_order.total_price += addition.price
		new_order.save()

		context['new_order'] = new_order

		# Send admin E-Mail
		# try:
		admin_content = render_to_string('email/tariff_order.html', context, context_instance=RequestContext(request))
		sendmsg = EmailMultiAlternatives(tariff.title, admin_content, site_config.email, [site_config.email])
		sendmsg.attach_alternative(admin_content, "text/html")
		sendmsg.send()


		# except:
		# 	pass

		context['ok'] = True

	return render(request, 'lp/tariff_order.html', context)
