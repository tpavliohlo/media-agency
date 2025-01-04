from django.shortcuts import render
from django.views import generic

from catalog.models import Redactor, Topic, Newspaper


# Create your views here.
def index(request):
    """View function for home page."""

    num_redactors = Redactor.objects.all().count()
    num_topics = Topic.objects.all().count()
    num_newspapers = Newspaper.objects.all().count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        'num_redactors': num_redactors,
        'num_topics': num_topics,
        'num_newspapers': num_newspapers,
        'num_visits': num_visits,
    }
    return render(request, "catalog/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    queryset = Topic.objects.all().order_by('name')
    paginate_by = 5


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    # resolving N+1 problem
    queryset = Newspaper.objects.select_related('topic')

class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related('newspaper_set__topic')
