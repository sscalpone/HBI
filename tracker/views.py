from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import Residence

def index(request):
    return render(request, 'tracker/index.html')

def login(request):
    return HttpResponseRedirect(reverse('tracker:main'))

def main(request):
    residence_list = Residence.objects.order_by('residence_name')
    context = RequestContext(request, {
	'residence_list': residence_list,
    })
    return render(request, 'tracker/main.html', context)

def residence(request, residence_id):
	p = get_object_or_404(Residence, pk=residence_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the residence choosing form.
		return render(request, 'tracker/main.html', {
			'poll' : p,
			'error_message': "You didn't select a choice.",
		})
	else:
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

