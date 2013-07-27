from django.contrib import admin
from shorts.models import Short

class ShortAdmin(admin.ModelAdmin):
	fields = ['short_url', 'target_url', 'hit_count']

admin.site.register(Short, ShortAdmin)