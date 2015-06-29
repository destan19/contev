from django.contrib import admin

# Register your models here.

from .models import Device
from .models import Param
class DeviceAdmin(admin.ModelAdmin):
	fieldsets=[
		#(None,               {'fields': ['question_text']}),
		#('Date information', {'fields': ['pub_date']}),
    ]
admin.site.register(Device,DeviceAdmin)

admin.site.register(Param,DeviceAdmin)