from django.shortcuts import render
from django.http import HttpResponse, Http404

from polls.models import Question

# Create your views here.


def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_questions}
    return render(request=request, template_name="polls/index.html", context=context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question is not exist")
    return render(
        request=request,
        template_name="polls/detail.html",
        context={"question": question},
    )


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You are voting on question %s" % question_id)
