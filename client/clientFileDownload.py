# -*- coding:utf-8 -*-
import socket, sys, time
import struct,os,json,tarfile


from clientCommonFunction import mylog


def ClientDownloadFileFromServer(mysock,f,paramfilename):
    # parser the parameter file
    print("  ClientDownload1FileFromServer START...")

    SBUFSIZE = 1024
    BUFSIZE = 1024

    fp = open(paramfilename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        print(filedata)
        if not filedata: break
        mysock.sendall(filedata)
    fp.close()

    fp = open(paramfilename, 'r')
    str = fp.read()
    fp.close()
    j_str = json.loads(str)
    clientfilepath = j_str['clientfilepath']
    clientfilename = j_str['clientfilename']

    # buf = mysock.recv(BUFSIZE)
    # buf = buf.decode('utf-8')
    # print("  ClientDownload1FileFromServer semantics:3.recv buf=", buf)
    # if (buf.find('OK') >= 0):#.encode('utf-8')
    FILEINFO_SIZE = struct.calcsize('<128s32sI8s')
    fhead = mysock.recv(FILEINFO_SIZE)

    revfilename, temp1, filesize, temp2 = struct.unpack('<128s32sI8s', fhead)
    revfilename = revfilename.decode('utf-8')
    revfilename = revfilename.strip("\00")
    fullfilename = clientfilepath + revfilename
    print("revfilename:"+revfilename)

    print("  ClientDownload1FileFromServer semantics:4.recv fullclientfilename=", fullfilename)
    fp = open(fullfilename, 'wb')
    restsize = filesize
    mylog(3, f, "ClientDownload1FileFromServer;FU1FLE,filesize=%d" % filesize)
    while 1:
        if restsize > SBUFSIZE:
            filedata = mysock.recv(SBUFSIZE)
        else:
            filedata = mysock.recv(restsize)
        if not filedata: break

        fp.write(filedata)
        restsize = restsize - len(filedata)
        if restsize == 0: break
    fp.flush()
    fp.close()
    time.sleep(0.1)
    print("  ClientDownload1FileFromServer semantics:5.recv OVER")
    t = tarfile.open(fullfilename)
    t.extractall(clientfilepath)
    t.close()
    #os.remove(fullfilename)
    # else:
    #     mylog(3, f, "ClientDownload1FileFromServer;File does not exist!")
    #     pass
    print("  ClientDownload1FileFromServer END.")
    pass

if __name__ == '__main__':
    pass

