#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import sys

from clientListShapes import *
from clientListDocTree import *
from clientFileDownload import *


import json

if __name__ != "__main__":
    sys.exit(2)

host =''
textport=''
srvroot=''
clientdir=''

#############################################################################
f = open("../pyclient.log", "w")

if len(sys.argv) == 2:
	paramfilename = sys.argv[1]
	print("~~~~~~~~~~~~~~~~~~~~~~~"+sys.argv[0])
	print("~~~~~~~~~~~~~~~~~~~~~~~" + sys.argv[1])
	mylog(3, f, paramfilename)
else:
    #print("usage: %s paramfilename(including path)" % sys.argv[0])
    mylog(3, f,"exit111 %s" % sys.argv[0])
    f.close()
    sys.exit(2)



#paramfilename = "D://tmp//download.json"
print(paramfilename);
fp = open(paramfilename,'r')
str=fp.read()
fp.close()
json = json.loads(str)

print('origion: ' + str)
host = json['srvip']
textport = json['srvport']
typeName = json['type']
print(host, textport, typeName)


mylog(3,f,"type="+typeName)

#######################################################################
#建立socket
try:
	mylog(3,f,'Creating socket object')
	mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
	print("Strange error creating socket: %s" % e)
	mylog(3,f,"Strange error creating socket: %s" % e)
	sys.exit(99)

# Try parsing it as a numeric port number.

try:
	port = int(textport)
except ValueError:
	# That didn't work.  Look it up instread.
	try:
		port = socket.getservbyname(textport, 'tcp')
	except socket.error as e:
		print("Couldn't find your port: %s" % e)
		mylog(3,f,"Couldn't find your port: %s" % e)
		sys.exit(99)

mylog(3,f,'Connecting to %s:%d' % (host, port))
time.sleep(1)

#######################################################################
#socket进行连接
try:
	mysocket.connect((host, port))
except socket.gaierror as e:
	print("Address-related error connecting to server: %s" % e)
	mylog(3,f,"Address-related error connecting to server: %s" % e)
	sys.exit(99)
except socket.error as e:
	print("Connection error: %s" % e)
	mylog(3,f,"Connection error: %s" % e)
	sys.exit(99)


mylog(3,f,'Sending query')
time.sleep(1)
timeout = 200
socket.setdefaulttimeout(timeout)

##############################################################################################
#开始socket通讯的语义
try:
	#mysocket.sendall("ASKING")
	#########################################################################################
	#buf=mysocket.recv(6)
	#mylog(3,f,"\nreceiving.....%s"%buf)
	#############################################################################
	#发送文件
	#############################################################################

	if typeName == "list_all_shapes":
		ClientDownloadShFromServer(mysocket, f, paramfilename)
	if typeName == "list_doc_tree":
	 	ClientDownloadTrFromServer(mysocket, f, paramfilename)
	# if typeName == "download_file":
	# 	ClientDownloadFileFromServer(typeName, mysocket, f, paramfilename, clientfilepath,clientfilename)

except socket.error as e:
	print("Error sending data: %s" % e)
	mylog(3,f,"Error sending data: %s" % e)
	sys.exit(90)

###########################################################################################
#关闭socket
############################################################################################
print("  Shutting down socket....")
mylog(3,f,'Shutting down socket')
time.sleep(1)
try:
	timeout = 20
	#mysocket.setdefaulttimeout(timeout)
	mysocket.settimeout(0.0)
	mysocket.shutdown(1)

except socket.error as e:
	print("Error sending data (detected by shutdown): %s" % e)
	mylog(3,f,"Error sending data (detected by shutdown): %s" % e)
	#sys.exit(1)

##############################################################################################
sys.exit(0)