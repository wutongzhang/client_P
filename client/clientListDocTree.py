import socket, sys, time
import struct


from client.clientCommonFunction import mylog


def ClientDownloadTrFromServer(typeName,mysock,f,paramfilename,clientfilepath):
    # parser the parameter file
    print("  ClientDownloadTrFromServer START...")
    BUFSIZE = 1024

    fp = open(paramfilename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        print(filedata)
        if not filedata: break
        mysock.sendall(filedata)
    fp.close()

    buf = mysock.recv(BUFSIZE)
    print("  ClientDownload1FileFromServer semantics:3.recv buf=", buf)
    fp = open("C:\\Users\\wutong\\Desktop\\untitled2\\untitled2\\req_ALEX_20170708142032_list_all_shapes.json", 'wb')
    fp.write(buf)
    pass


if __name__ == '__main__':
    pass
