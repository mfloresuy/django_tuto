from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    """docstring for IndexView"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailsView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    """Voting resultts from a question"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:result', args=(question.id,))
        )
