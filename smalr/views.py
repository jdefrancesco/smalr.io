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




def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def main(request):
    """Main listing."""
    forums = Forum.objects.all()
    return render_to_response("forum/list.html", dict(forums=forums, user=request.user))

def forum(request, pk):
    """Listing of threads in a forum."""
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = mk_paginator(request, threads, 20)
    return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk))

def thread(request, pk):
    """Listing of posts in a thread."""
    posts = Post.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    t = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title,
                                                           forum_pk=t.forum.pk, media_url=MEDIA_URL))

@login_required
def profile(request, pk):
    """Edit user profile."""
    profile = UserProfile.objects.get(user=pk)
    img = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            # resize and save image under same filename
            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((160,160), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
    else:
        pf = ProfileForm(instance=profile)

    if profile.avatar:
        img = "/media/" + profile.avatar.name
    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))

@login_required
def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("dbe.forum.views.%s" % ptype, args=[pk])
    if ptype == "new_thread":
        title = "Start New Topic"
        subject = ''
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title

    return render_to_response("forum/post.html", add_csrf(request, subject=subject, action=action,
                                                          title=title))

def increment_post_counter(request):
    profile = request.user.userprofile_set.all()[0]
    profile.posts += 1
    profile.save()

@login_required
def new_thread(request, pk):
    """Start a new thread."""
    p = request.POST
    if p["subject"] and p["body"]:
        forum = Forum.objects.get(pk=pk)
        thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
        Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("dbe.forum.views.forum", args=[pk]))

@login_required
def reply(request, pk):
    """Reply to a thread."""
    p = request.POST
    if p["body"]:
        thread = Thread.objects.get(pk=pk)
        post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("dbe.forum.views.thread", args=[pk]) + "?page=last")



