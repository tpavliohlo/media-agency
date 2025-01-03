from django.shortcuts import render

from catalog.models import Redactor, Topic, Newspaper


# Create your views here.
def index(request):
    """View function for home page."""

    num_redactors = Redactor.objects.all().count()
    num_topics = Topic.objects.all().count()
    num_newspapers = Newspaper.objects.all().count()

    context = {
        'num_redactors': num_redactors,
        'num_topics': num_topics,
        'num_newspapers': num_newspapers,
    }
    return render(request, "index.html", context=context)
