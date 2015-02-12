################################################################################################
# Author: in70x, Madhax
# Date:   8/20/2013
# 
# Description: smalr.io models file
#
#
#
#
# Last Updated: 9/26/2013
# Copyright (c) smalr.io
################################################################################################


import datetime
import hashlib
import urlparse

from django.db import models
from django.utils import timezone

from tagging.fields import TagField
from shorts.short import *

class State(models.Model):
    """
    singleton table keeping dynamic state information
    """
    urls_head = models.PositiveIntegerField(default=0) #ptr to next short url, used to minimize lookup time on next 'random' short URL

class DestinationUrls(models.Model):
    """
    Table for the destination URLs, kept separately and immutable 
    """
    url = models.CharField(max_length=2000)
    
    
class ShortUrls(models.Model):
    """
    Table for our short urls
    """
    key            = models.BigIntegerField(default=0, unique=True, db_index=True)
    status         = models.PositiveIntegerField(default=0) #TBD status codes (deleted/blocked/disabled, etc)
    date_submitted = models.DateTimeField(auto_now_add=True) # Date link was created
    last_accessed  = models.DateTimeField(auto_now=True)     # Update automatically each access of link
    hit_count      = models.BigIntegerField(default=0)  # Hit count of link
    safety_rating  = models.DecimalField(max_digits=5, decimal_places=2) #safety score, probably will change
    safety_time    = models.DateTimeField(auto_now=True) #date when safety rating was determined. 
    destination_url = models.ForeignKey(DestinationUrls)
    
    def __unicode__(self):
        pass

    # Tell us is link was recently created..self.
    def was_created_recently(self):
        return  self.date_submitted >= timezone.now() - datetime.timedelta(days=1)
    
    def dict_output(self):
        new_dict = dict()
        new_dict['pk'] = self.pk
        new_dict['key'] = value_encode62(self.key)
        new_dict['hit_count'] = self.hit_count
        new_dict['last_accessed'] = str(self.last_accessed)
        new_dict['safety_rating'] = long(self.safety_rating)
        new_dict['destination_url'] = self.get_external_destination_url()
        return new_dict

    def is_secure(self):
        return self.safety_rating > 80
    
    def create_thumbnail(self):
        #@TODO
        #generate thumbnail for URL
        return False 
    
    def calculate_security(self):
        #@TODO
        #recalculate security
        return False

    def get_external_destination_url(self):
        #add http or https to url if it is not there
        pr = urlparse.urlparse(self.destination_url.url)
        if pr.scheme == '':
            pr = pr._replace(scheme='http')
            return urlparse.urlunparse(pr)
        return self.destination_url.url
    
class Users(models.Model):
    login_name    = models.CharField(max_length=32, unique=True, db_index=True)
    password_hash = models.CharField(max_length=40)
    email         = models.CharField(max_length=255, unique=True)
    
    def is_password(self, input_password):
        h = hashlib.sha1()
        h.update(input_password)
        return h.hexdigest() == self.password_hash
    
    
    
class owner_to_url(models.Model):
    user_id = models.PositiveIntegerField(default=0,  db_index=True)
    url_id  = models.PositiveIntegerField(default=0)
    
class url_to_owner(models.Model):
    url_id  = models.PositiveIntegerField(default=0,  db_index=True)
    user_id = models.PositiveIntegerField(default=0)

    
    