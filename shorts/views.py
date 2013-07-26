from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect
from django.views.decorators.http import require_GET, require_POST

from shorts.models import Short

def index(request):
	"""
	View for homepage
	"""
	pass