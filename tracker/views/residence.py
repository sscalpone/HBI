from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Residence
from tracker.models import ResidenceForm

def index(request):
    list_of_residences = Residence.objects.all()
    context = {'residences': list_of_residences }
    return render(request, 'tracker/main.html', context)

def new(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST, request.FILES)
        if form.is_valid():
            saved_residence = form.save()
            if saved_residence:
                return HttpResponseRedirect(reverse('tracker:residences'))
    else:
        form = ResidenceForm()
    context = {
        'form': form.as_ul,
    }
    return render(request, 'tracker/add_residence.html', context)

def view(request, residence_id):
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