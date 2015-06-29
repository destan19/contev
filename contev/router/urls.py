from django.conf.urls import *
from router.views import *
urlpatterns = patterns('',
                      #url(r'^$',archive),
					  url(r'^echo',echo),
					  url(r'^reportData',reportData),
					  url(r'^showDeviceList',showDeviceList),
					  url(r'^index',index),
					  url(r'^addDevice',addDevice),
					  url(r'^onlineStatus',onlineStatus),
					  url(r'^ajax_test',ajax_test),
					  
                      )