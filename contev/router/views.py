from django.shortcuts import render
from django.shortcuts import render_to_response 
# Create your views here.
from django.template import loader,Context
from router.models import *
from django.http import HttpResponse
from datetime import *
import json;
from datetime import *
import time
def echo(request):
	return HttpResponse("hello django");
#192.168.17.130/router/showPara?a=1&b=2&c=3&data={"id":"111","state":{"code":"20000","msg":"success"}}

"""
{"id":"111","state":{"code":"20000","msg":"success"}}
resp
{"code":"200","data":{"mac":"11:22:33:44:55:66","id":1}}
>>> data={}
>>> data['mac']="11:22:33:44:55:66"
>>> data['id']=2
>>> print data
{'mac': '11:22:33:44:55:66', 'id': 2}
>>> res_json={}
>>> res_json['code']="200"
>>> res_json['data']=data
>>> print res_json
{'code': '200', 'data': {'mac': '11:22:33:44:55:66', 'id': 2}}
"""

"""
192.168.17.130/router/reportData?para={"id":"10001","router":{"mac":"11:22:33:44:55:66","sver":"m001","hver":"001"},"data":{}}

{
	"id":"10001",
	"router":{
		"mac":"11:22:33:44:55:66",
		"sver":"m001",
		"hver":"001",
	}
	"data":
	{
		
	}
}

res
{
	"id":"10001",
	"state":
	{
		"code":"20000",
		"msg":"success"
	}
}
"""
def index(request):
	return render_to_response('index.html')
	
def reportData(request):
	req_para=request.REQUEST.get("device_info")
	req_json=json.loads(req_para)
	res_json={}
	res_state={}
	id=req_json['id']
	router_obj=req_json['router']
	data_obj=req_json['data']
	try:
		router=Device.objects.filter(mac=router_obj['mac'])
	except:
		print 'not exist' 
		
	if (any(router)):
		router=Device.objects.get(mac=router_obj['mac'])
		last_time=router.last_heart_time
		
		last_time=last_time.replace(tzinfo=None)
		now=datetime.now()
		
		seconds=(now-last_time).seconds
		weekday=date.today().weekday()
		status=router.online_status
		if ( len(status) < 13 ):
			status="0;0;0;0;0;0;0"
		
		status_bits_arr=status.split(";")

		cur_status=long(status_bits_arr[weekday])
		
		hour=int(time.strftime("%H"))
		cur_status=1<<hour | cur_status
		print cur_status,hour
		status_bits_arr[weekday]='%d' %cur_status
		status=""
		for i,value in enumerate(status_bits_arr):
			status+=value
			if(i<6):
				status+=";"
		
		router.online_status=status
		print weekday,status
		router.last_heart_time=datetime.now()
		
		res_state['msg']='success'
		res_state['code']='200000'
		router.save()
	else:
		res_state['msg']='device not exist'
		res_state['code']='500001'
	
	res_json['id']=id
	res_json['state']=res_state
	return HttpResponse(json.dumps(res_json))
	
"""
	func:showDeviceList
	desc:display all device list
	input: none
"""
def showDeviceList(request):
	devs=Device.objects.all();
	dev_list=[]
	for dev in devs:
		dev_dict={}
		dev_dict['obj']=dev
		last_time=dev.last_heart_time
		last_time=last_time.replace(tzinfo=None)
		now=datetime.now()
		seconds=(now-last_time).seconds
		print "seconds=",seconds
		#30 minutes
		if (seconds > 1800):
			dev_dict['status']=0
		else:
			dev_dict['status']=1
		dev_list.append(dev_dict)
		
	t=loader.get_template('device_list.html')
	c=Context({
		'device_list':dev_list,
		'name':'hello',
			})
	return HttpResponse(t.render(c))

"""
"""
def onlineStatus(request):
	dev_mac=request.REQUEST.get("mac")		
	try:
		dev=Device.objects.filter(mac=dev_mac)
	except:
		print 'not exist' 
	if (any(dev)):
		dev=Device.objects.get(mac=dev_mac)
		status=dev.online_status	
	
	t=loader.get_template('online_status.html')
	c=Context({
		'status':status,
			})
	return HttpResponse(t.render(c))
	
	
"""
	func:addDevice
	desc:add a new device
	input: mac
"""	

	

def addDevice(request):
	
	dev_mac=request.REQUEST.get("mac")
	res_str="success"
	print dev_mac
	if (len(dev_mac) < 17):
		return	render_to_response("result.html",{"res":"invalid mac"})
	try:
		dev=Device.objects.filter(mac=dev_mac)
	except:
		print 'not exist'
	if (any(dev)):
		res_str="error"
	else:
		new_dev=Device(mac=dev_mac)
		new_dev.last_heart_time=datetime.now()
		new_dev.price=300
		new_dev.h_version="001"
		new_dev.s_version="m0001"
		new_dev.descript="xxxxxxxx"
		new_dev.register_date=datetime.now()
		new_dev.cmd_exe_time=datetime.now()
		new_dev.online_status="0;0;0;0;0;0;0"
		new_dev.save()
	return	render_to_response("result.html",{"res":res_str})

def ajax_test(request):
	return	render_to_response("ajax_test.html")	
	

