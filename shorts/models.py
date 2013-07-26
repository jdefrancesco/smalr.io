from django.db import models

class Short(models.Model):
	"""
	Model for our short urls
	"""
	target_url     = models.URLField(max_length=2000) # Averaging support from browsers
	short_url      = models.CharField(max_length=200) # max_length is this high for a "short link" because of custom created links
	date_submitted = models.DateTimeField(auto_add_now=True)
	last_accessed  = models.DateTimeField(auto_now=True)	
	hit_count      = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		pass




