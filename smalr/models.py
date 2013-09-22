################################################################################################
# Author: in70x, Madhax
# Date:   8/20/2013
# 
# Description: smalr.io models file
#
#
#
#
#
# Copyright (c) smalr.io
################################################################################################


import datetime
import hashlib

from django.db import models
from django.utils import timezone

from tagging.fields import TagField

class state(models.Model):
    """
    singleton table keeping dynamic state information
    """
    urls_head = models.PositiveIntegerField(default=0) #ptr to next short url, used to minimize lookup time on next 'random' short URL


class urls(models.Model):
    """
    Table for our short urls
    """
    key            = models.PositiveIntegerField(default=0, unique=True, db_index=True)
    status         = models.PositiveIntegerField(default=0) #TBD status codes (deleted/blocked/disabled, etc)
    date_submitted = models.DateTimeField(auto_now_add=True) # Date link was created
    last_accessed  = models.DateTimeField(auto_now=True)     # Update automatically each access of link
    hit_count      = models.PositiveIntegerField(default=0)  # Hit count of link
    safety_rating  = models.DecimalField(max_digits=5, decimal_places=2) #safety score, probably will change
    safety_time    = models.DateTimeField(auto_now=True) #date when safety rating was determined. 
    url            = models.CharField(max_length=2000) #actual URL
    
    def __unicode__(self):
        pass

    # Tell us is link was recently created..self.
    def was_created_recently(self):
        return  self.date_submitted >= timezone.now() - datetime.timedelta(days=1)

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
    
class users(models.Model):
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

    
    