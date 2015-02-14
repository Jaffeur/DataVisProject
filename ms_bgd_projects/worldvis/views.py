from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_protect
import models


# Create your views here.
@requires_csrf_token
def world_map(request):
	countries = models.get_countries()
	features = models.get_features()
	template = "datavis.html"
	return render(request, template, {'countries' : countries, 'features' : features})

