import datetime

from django.db import models
from django.utils import timezone

from tagging.fields import TagField

class Short(models.Model):
	"""
	Table for our short urls
	"""
	target_url     = models.URLField(max_length=2000) # Averaging support from browsers
	short_url      = models.CharField(max_length=200) # max_length is this high for a "short link" because of custom created links
	date_submitted = models.DateTimeField(auto_now_add=True) # Date link was created
	last_accessed  = models.DateTimeField(auto_now=True)	 # Update automatically each access of link
	hit_count      = models.PositiveIntegerField(default=0)  # Hit count of link
	saftey_rating  = models.DecimalField(max_digits=5, decimal_places=2) # holds percentage value 0.00 to 99.99
	tags  		   = TagField()

	def __unicode__(self):
		pass

	# Tell us is link was recently created..self.
	def was_created_recently(self):
		return  self.date_submitted >= timezone.now() - datetime.timedelta(days=1)





