from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from web3 import Web3
from .viewmodels.StudentViewModel import StudentBt
import json
import os

# Create your views here.


def index(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(
        BASE_DIR, "aeibt/contractsjson/student_record_compiled_code.json"
    )
    with open(json_file_path) as file:
        student_json = json.load(file)

    # get bytecode
    bytecode = student_json["contracts"]["InfoStorage.sol"]["InfoStorage"]["evm"][
        "bytecode"
    ]["object"]

    # get abi
    abi = student_json["contracts"]["InfoStorage.sol"]["InfoStorage"]["abi"]
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

    chain_id = 1337
    # my_address = os.getenv("MY_ADDRESS")
    # private_key = os.getenv("MY_PRIVATE_KEY")
    student_storage_contract = w3.eth.contract(
        address="0xf528118C6a6bBB61b47Ff92B4431C9b7277E790a", abi=abi, bytecode=bytecode
    )

    results = student_storage_contract.functions.get_all_students().call()
    students = []
    for v in results:
        st = StudentBt(
            v[0],
            v[1],
            v[2],
            v[3],
            v[4],
            v[5],
            v[6],
            v[7],
        )
        students.append(st)

    return render(
        request,
        "aeibt/index.html",
        {"btstudents": students, "error_message": "no student found in the blockchain"},
    )


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "aeibt/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("aeibt:results", args=(question.id,)))
