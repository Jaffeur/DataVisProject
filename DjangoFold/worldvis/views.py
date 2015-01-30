from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def world_map(request):
	template = "datavis.html"

	return render(request, template)

