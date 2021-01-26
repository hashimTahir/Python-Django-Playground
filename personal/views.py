from django.shortcuts import render
from personal.models import Question

# Create your views here.


def home_screen_view(request):
    context = {}
    # Oneway
    # context['data_string'] = "String that is to be passed to the view."
    # context['data_number'] = 125663

    # Other way

    # context = {
    #     'data_string': "String that is to be passed to the view.",
    #     'data_number': 125663
    # }

    # Passs list of data

    list_of_views = []
    list_of_views.append("a")
    list_of_views.append("b")
    list_of_views.append("c")
    list_of_views.append("ds")

    questions = Question.objects.all
    context['questions'] =  questions

    context['list_name_dosent_matter_here'] = list_of_views

    return render(request, "personal/home.html", context)
