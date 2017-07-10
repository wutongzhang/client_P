# -*- coding:utf-8 -*-
'''
Created on 2012-8-20

@author: test
'''
import socket, sys, time
from threading import *
import struct
import os,json,tarfile

from clientCommonFunction import mylog


def ClientUpload1FileToServer(mysock,f,paramfilename):
    # parser the parameter file
    upfilename = u""
    fullfilename = ''

    print("  ClientUpload1FileToServer START...")
    BUFSIZE = 1024

    fp = open(paramfilename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata: break
        mysock.sendall(filedata)
    fp.close()

    fp = open(paramfilename, 'r')
    str = fp.read()
    fp.close()
    j_str = json.loads(str)
    clientfilepath = j_str['clientfilepath']
    clientfilename = j_str['clientfilename']

    print("  ClientUpload1FileToServer semantics:2.send file full path=")

    # buf = mysock.recv(BUFSIZE)
    # print("  ClientUpload1FileToServer semantics:3.recv buf=", buf)
    # if (buf.find('OK') >= 0):
    fullfilename = clientfilepath
    upfilename = clientfilepath.encode("UTF-8")
    print("  ClientUpload1FileToServer UP FILE NAME=", fullfilename)
    print("  ClientUpload1FileToServer;UP FILE SIZE=", os.stat(fullfilename).st_size)

    FILEINFO_SIZE = struct.calcsize('<128s32sI8s')
    fhead = struct.pack('<128s11I', upfilename, 0, 0, 0, 0, 0, 0, 0, 0, os.stat(fullfilename).st_size, 0, 0)
    mysock.send(fhead)
    # print "  ClientUpload1FileToServer semantics:4.send file fhead=",fhead

    fp = open(fullfilename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata: break
        mysock.sendall(filedata)
    fp.close()
    print("  ClientUpload1FileToServer semantics:4.send file block each %d" % BUFSIZE)

    buf = mysock.recv(BUFSIZE)
    print("  ClientUpload1FileToServer semantics:5.recv return=%s" % buf)
    # else:
    #     mylog(3, f, "ClientUpload1FileToServer;File does not exist!")
    #     print("  ClientUpload1FileToServer semantics error.")
    #     pass
    print("  ClientUpload1FileToServer END.")
    pass


###################################################################################
# �ϴ��ļ�
###################################################################################
def clientFU1FLE(cmdname,mysocket,paramfilename,clientfilepath,flog):
        for i in range(0, 200):
            print("i=", i)
            ClientUpload1FileToServer(cmdname,mysocket,flog,paramfilename,clientfilepath)


if __name__ == '__main__':
    pass