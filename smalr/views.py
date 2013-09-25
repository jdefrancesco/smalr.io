##############################################################################################
# Author: in70x, Madhax
# Date:   9/21/2013
# 
# Description: smalr.io views file
# Major TODO: add url dispatcher for custom length URLs
#
#
#
# Last Updated: 9/23/2013
# Copyright (c) smalr.io
################################################################################################

import datetime
import json
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
from django.core import serializers

from smalr.models import *
from shorts.short import *

def shorten(request):
    p = request.POST
    if p["url"] and p["url"] != "":
        url = p["url"]
        #@TODO fix custom URL collission
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
        tmp = urls.objects.create(key=url_key, status=0, hit_count=0, safety_rating=0.0, url=url)

        plaintext_url = value_encode62(url_key)  
        now = datetime.datetime.now()
        request.session['last'] = now
        if 'urls' in request.session:
            request.session['urls'].append(tmp.id)
        else:
            request.session['urls'] = []
            request.session['urls'].append(tmp.id)
        
        #@TODO get a list of all recent URLs created by this user (via acct_id or session)
    output = []
    if 'urls' in request.session:
        my_urls = urls.objects.in_bulk(request.session['urls'])
        for pk in request.session['urls']:
            output.append([my_urls[pk].pk, value_encode62(my_urls[pk].key), str(my_urls[pk].last_accessed), my_urls[pk].hit_count, long(my_urls[pk].safety_rating), my_urls[pk].url])
        
    #reverse output
    output = output[::-1]
    data = json.dumps(output)
    return HttpResponse(data, mimetype='application/json')

def custom_shorten(request):
    #@TODO Finish custom URLS
    p = request.POST
    if p["url"]:
        pass
    return("")


#check if custom URL is available, will return  true/false via ajax on keyboard input
def is_valid_custom(request):
    #@TODO Finish is valid
    p = request.POST
    if p["url"]:
        pass
    return("")
    
    
def status():
    #@TODO Finish status pages
    return("")
    

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

def index(request):
    #@TODO find better placement for template
    c = {}
    c.update(csrf(request))
    return render_to_response("index.djt", c)

def register(request):
    return HttpResponseRedirect("")

def login(request):
    return HttpResponseRedirect("")

