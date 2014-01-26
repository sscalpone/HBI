from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from polls.models import Choice, Question

def index(request):
    latest_poll_list = Question.objects.order_by('-pub_date')[:5]
    context = RequestContext(request, {
	'latest_poll_list': latest_poll_list,
    })
    return render(request, 'polls/index.html', context)

# def index(request):
#     latest_poll_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = RequestContext(request, {
# 	'latest_poll_list': latest_poll_list,
#     })
#     return HttpResponse(template.render(context))

def detail(request, poll_id):
	poll = get_object_or_404(Question, pk=poll_id)
	return render(request, 'polls/detail.html', {'poll' : poll} )

# def detail(request, poll_id):
#     try:
#         poll = Question.objects.get(pk=poll_id)
#     except Question.DoesNotExist:
#         raise Http404
#     return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
	poll = get_object_or_404(Question, pk=poll_id)
	return render(request, 'polls/results.html', {'poll' : poll} )

def vote(request, poll_id):
	p = get_object_or_404(Question, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the poll voting form.
		return render(request, 'polls/detail.html', {
			'poll' : p,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedriect after successfully dealing
		# with POST data.  This prefents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

