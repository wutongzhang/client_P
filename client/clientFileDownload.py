# -*- coding:utf-8 -*-
import socket, sys, time
import struct


from clientCommonFunction import mylog


def ClientDownloadFileFromServer(typeName,mysock,f,paramfilename,clientfilepath,clientfilename):
    # parser the parameter file
    print("  ClientDownload1FileFromServer START...")
    FBUFSIZE = 1024
    SBUFSIZE = 1024
    BUFSIZE = 1024

    fp = open(paramfilename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        print(filedata)
        if not filedata: break
        mysock.sendall(filedata)
    fp.close()

    buf = mysock.recv(BUFSIZE)
    #buf = buf.decode('utf-8')
    print("  ClientDownload1FileFromServer semantics:3.recv buf=", buf)
    if (buf.find('OK') >= 0):#.encode('utf-8')
        FILEINFO_SIZE = struct.calcsize('<128s32sI8s')
        fhead = mysock.recv(FILEINFO_SIZE)

        filename, temp1, filesize, temp2 = struct.unpack('<128s32sI8s', fhead)
        # clientfilename=clientfilepath+string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','L','m','n','o','p','q','r','s','t'], 8)).replace(" ","")+"_"+downloadfilename.strip('\00')
        filename = filename.decode('utf-8')
        filename = filename.strip("\00")
        print(filename)
        print("  ClientDownload1FileFromServer semantics:4.recv clientfilename=", clientfilename)
        fp = open(clientfilename, 'wb')
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
    else:
        mylog(3, f, "ClientDownload1FileFromServer;File does not exist!")
        pass
    print("  ClientDownload1FileFromServer END.")
    pass

if __name__ == '__main__':
    pass

