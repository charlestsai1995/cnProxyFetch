#!/usr/bin/python
import requests
import xml.dom.minidom
import sys
import time
import linecache
import ConfigParser
import os

path = os.path.abspath(os.path.dirname(sys.argv[0]))
conf = ConfigParser.ConfigParser()
conf.read(path+"/config.ini")
f = open(path+'/ip.xml','w')
r = requests.get('http://www.getproxy.jp/proxyapi?ApiKey='+conf.get('api','apikey')+'&area=CN&sort=requesttime&orderby=asc&page='+conf.get('api','page'))
r=str(r.text)
f.writelines(r)
f.close()
dom = xml.dom.minidom.parse(path+'/ip.xml')
ip=dom.getElementsByTagName('ip')
pingt=dom.getElementsByTagName('requesttime')
test=pingt[len(pingt)-1]
test.firstChild.data=int(test.firstChild.data)
if test.firstChild.data<2:
	exit()
bl=open(path+'/blacklist.txt','r')
blist=bl.read()
fit = 0
i=0
for index, element in enumerate(ip):
	pingt[index] = int(pingt[index].firstChild.data)
	if pingt[index] < 1 or pingt[index] > 2000:
		print 'ping not pass ' + element.firstChild.data
	else:
		print 'ping pass ' + element.firstChild.data
		if element.firstChild.data in blist:
			print 'excluded'
		else:
			fit = 1
			i = index
			break
if fit == 1:
	print 'result ' + ip[i].firstChild.data
	currentip_file=open(path+'/current.txt','w+')
	currentip_file.write(ip[i].firstChild.data)
	pac=open(conf.get('path','web')+'netease.pac','r+')
	flist=pac.readlines()
	flist[1]='   if (host == \'music.163.com\') return \'PROXY '+ip[i].firstChild.data+'\';\n'
	flist[2]='   if (shExpMatch(url,\"*.xiami.com/*\")) return \'PROXY ' +ip[i].firstChild.data+'\';\n'
	flist[3]='   if (shExpMatch(url,\"*.xiami.net/*\")) return \'PROXY ' +ip[i].firstChild.data+'\';\n'
	flist[4]='   if (shExpMatch(url,\"*.cnzz.com/*\")) return \'PROXY ' +ip[i].firstChild.data+'\';\n'
	flist[5]='   if (shExpMatch(url,\"*.tudou.com/*\")) return \'PROXY ' +ip[i].firstChild.data+'\';\n'
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	flist[8]='//'+localtime+'\n'
	pac=open(conf.get('path','web')+'netease.pac','w+')
	pac.writelines(flist)
	pac.close()
	webpage=open(conf.get('path','web')+'index.htm','r+')
	pagecon=webpage.readlines()
	pagecon[6]='<center>Current server: ' + ip[i].firstChild.data +'</center>\n'
	pagecon[7]='<center>Update time: ' + localtime +'(EST)</center>\n'
	webpage=open(conf.get('path','web')+'index.htm','w+')
	webpage.writelines(pagecon)
	webpage.close()
else:
	print 'no fit'
