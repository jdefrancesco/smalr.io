from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.views.decorators.http import require_GET, require_POST

from shorts.models import Short

def index(request):
	"""
	View for homepage
	"""
	return HttpResponse("hello this is the home page for short urls")