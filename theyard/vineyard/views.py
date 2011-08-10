from django.template import Context, loader
from django.http import HttpResponse
from models import *
from django import forms
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
import os, sys
cmd_folder = os.path.VineyardReal(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from VineyardReal.vineyard import Vineyard

def index(request):
	return render_to_response('vineyard/index.html')
	Vineyard.handle+sms
