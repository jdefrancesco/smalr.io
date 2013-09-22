##############################################################################################
# Author: in70x, Madhax
# Date:   8/21/2013
# 
# Description: smalr.io views file
#
#
#
#
#
# Copyright (c) smalr.io
################################################################################################

import datetime
from string import join

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist



from smalr.models import *
from shorts.short import *

def shorten(request):
    #@TODO Finish Shorten URL
    p = request.POST
    if p["url"]:
        url = p["url"]
        try: #get next 'dynamic' url
            url_key = state.objects.get(pk=1)
            url_key.urls_head += 1
            url_key.save()
            url_key = url_key.urls_head
        except ObjectDoesNotExist:
            #create row and set URL key to default
            url_key = 1
            state.objects.create(urls_head=1)
        #insert short URL
        urls.objects.create(key=url_key, status=0, hit_count=0, safety_rating=0.0, url=url)
        plaintext_url = base10_to_base62(url_key)      
        #@TODO get a list of all recent URLs created by this user (via acct_id or session)
    #return HttpResponseRedirect("http://smalr.io/")
    return render_to_response("fake-landing.html")
    
    

def redirect(request, key):
    key = base62_to_base10(key.encode('ascii'))
    try:
        url = urls.objects.get(key=key)
        url.hit_count += 1
        now = datetime.datetime.now()
        url.last_accessed = now.strftime("%Y-%m-%d %H:%M")
        url.save()
        return HttpResponseRedirect(url.url)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("http://smalr.io/")
    return HttpResponseRedirect("")

def main(request):
    return render_to_response("fake-index.html")

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("fake-index.html", c)

def register(request):
    return HttpResponseRedirect("")

def login(request):
    return HttpResponseRedirect("")

