from django.shortcuts import render
from django.http import HttpResponse

## Create your views here.
def homepage(request):
    return HttpResponse('Welcome to our homepage! <strong>#samoKAFICH</strong>')
    # primjetiti korištenje HTML-a