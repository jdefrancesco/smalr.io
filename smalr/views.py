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
import time
import json
import random
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

    if "url" in p and p["url"] != "":
        url = p["url"]

        #@TODO fix custom URL collission
        try: #get next 'dynamic' url
            url_key = State.objects.get(pk=1)
            url_key.urls_head += 1
            check_row = ShortUrls.objects.filter(key=url_key.urls_head).exists()
            while check_row == True:
                url_key.urls_head += 1
                check_row = ShortUrls.objects.filter(key=url_key.urls_head).exists()
            url_key.save()
            url_key = url_key.urls_head
        except ObjectDoesNotExist:
            #create row and set URL key to default
            url_key = 1
            State.objects.create(urls_head=1)
        #insert short URL
        new_dest_url = DestinationUrls.objects.create(url=url)
        tmp = ShortUrls.objects.create(key=url_key, status=0, hit_count=0, safety_rating=0.0, destination_url=new_dest_url)

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
        my_urls = ShortUrls.objects.in_bulk(request.session['urls'])
        for pk in request.session['urls']:
            output.append(my_urls[pk].dict_output())
        
    #reverse output
    output = output[::-1]
    data = json.dumps(output)
    return HttpResponse(data, mimetype='application/json')


def delete(request, pk):
    output = []
    if 'urls' in request.session:
        request.session['urls'] =  filter(lambda a: a != int(pk), request.session['urls'])
        my_urls = ShortUrls.objects.in_bulk(request.session['urls'])
        for pk in request.session['urls']:
            output.append(my_urls[pk].dict_output())
    
    output = output[::-1]
    data = json.dumps(output)
    return HttpResponse(data, mimetype='application/json')


#check if custom URL is available, will return  true/false via ajax on keyboard input
def check_custom_form(request):
    p = request.POST
    output = False
    if 'custom_url_input' in p and p['custom_url_input'] != "":
        try:
            custom_url = base62_to_base10(p['custom_url_input'].encode('ascii'))
            check_row = ShortUrls.objects.filter(key=custom_url).exists()
            if check_row == False:
                output = True
            if custom_url < 0 or custom_url > 9223372036854775805:
                output = False
        except:
            output = False
            
    data = json.dump(output)
    return HttpResponse(data, mimetype='application/json')
            
    
def create_custom_url(request):
    p = request.POST
    if 'custom_url_input' in p and p['custom_url_input'] != "" and 'url' in p and p['url'] != "":
        try:
            url = p['url']        
            custom_url = base62_to_base10(p['custom_url_input'].encode('ascii'))
            check_row = ShortUrls.objects.filter(key=custom_url).exists()
            if check_row == False and custom_url > 0 and custom_url < 9223372036854775805:
                output = True
            if custom_url < 0 or custom_url > 9223372036854775805:
                output = False
                
            new_dest_url = DestinationUrls.objects.create(url=url)
            tmp = ShortUrls.objects.create(key=custom_url, status=0, hit_count=0, safety_rating=0.0, destination_url=new_dest_url)
            if 'urls' in request.session:
                request.session['urls'].append(tmp.id)
            else:
                request.session['urls'] = []
                request.session['urls'].append(tmp.id)
        except:
            pass
    
        
    output = []
    if 'urls' in request.session:
        my_urls = ShortUrls.objects.in_bulk(request.session['urls'])
        for pk in request.session['urls']:
            output.append(my_urls[pk].dict_output())
        
    #reverse output
    output = output[::-1]
    data = json.dumps(output)
    
    return HttpResponse(data, mimetype='application/json')


def lookup_n_rows(request, n):
    start = time.time()
    for x in range(0, int(n)):
        custom_url = random.randint(0, 9223372036854775805)
        check_row = ShortUrls.objects.filter(key=custom_url).exists()
    return HttpResponse(str(time.time()-start))    

def create_n_rows(request, n):
    start = time.time()
    for x in range(0, int(n)):
        custom_url = random.randint(0, 9223372036854775805)
        check_row = ShortUrls.objects.filter(key=custom_url).exists()
        if check_row == False:
            new_dest_url = DestinationUrls.objects.create(url="http://google.ca/")
            tmp = ShortUrls.objects.create(key=custom_url, status=0, hit_count=0, safety_rating=0.0, destination_url=new_dest_url)
    
    return HttpResponse(str(time.time()-start)) 
    
def status():
    #@TODO Finish status pages
    return("")

def redirect(request, key):
    key = base62_to_base10(key.encode('ascii'))
    try:
        url = ShortUrls.objects.get(key=key)
        url.hit_count += 1
        now = datetime.datetime.now()
        url.last_accessed = now.strftime("%Y-%m-%d %H:%M")
        url.save()
        return HttpResponseRedirect(url.destination_url.url)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("http://smalr.io/")
    return HttpResponseRedirect("")

def index(request):
    #@TODO find better placement for template
    c = {}
    c.update(csrf(request))
    return render_to_response("index.djt", c)

def register(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("register.djt", c)

def login(request):
    return HttpResponseRedirect("")

