# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from tracker.models import HelpEmailForm


"""The send_email() function processes the HelpEmailForm and, on 
validation, sends it to the info@hbint.org.
"""
@login_required
def send_email(request):
	# If POST request, get and process form
	if (request.POST):
		help_form = HelpEmailForm(request.POST, request.FILES)

		if (help_form.is_valid()):
			saved_email = help_form.cleaned_data

			# Save form to variables to be used to populate email
			subject = saved_email['problem']
			message = saved_email['explanation']

			# For some reason regular methods of validating didn't 
			# work, so this is to make sure message has something 
			# written in it. If it doesn't, return to the help.html 
			# template with a "Please explain your problem" message.
			if message == '':
				form = HelpEmailForm(initial=
					{
						'problem': subject,
					})
				messages.add_message(request, messages.INFO, 
					'Por favor, explique su problema.')
				context = {
					'form': form.as_ul,
					'page': 'help',
				}
				return render(request, 'tracker/help.html', context)

			# finish creating variables
			user = request.user
			subject = saved_email['problem']
			message = saved_email['explanation']
			from_email = user.email
			to_email = ['info@hbint.org']

			# Send email, populated with variables created above.
			send_mail(subject, message, from_email, to_email)
			form = HelpEmailForm()

			# render the help.html template with a success message
			messages.add_message(request, messages.SUCCESS, 
				'Tu correo ha sido enviado. Nos pondremos en contacto con '
				'usted tan pronto como sea posible.')
			return HttpResponseRedirect(reverse('tracker:help'))

	# If the user doesn't have an email, prompt them to add an email 
	# to their profile before sending (otherwise there's no way to 
	# contact them.) Return to the profile template to add the email.
	if (request.user.email == ""):
		messages.add_message(request, messages.INFO, 'Por favor, añadir un '
			'correo electrónico a su cuenta.')
		return HttpResponseRedirect(reverse('tracker:profile', 
			kwargs={'profile_id': request.user.id}))
	
	# Create new form
	form = HelpEmailForm()
	
	# Render the help.html template
	context = {
		'form': form.as_ul,
		'page': 'help',
	}
	return render(request, 'tracker/help.html', context)


