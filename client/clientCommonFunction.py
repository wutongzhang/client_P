import time

def mylog(level,f,str):
    f.write("[%s]....%s\n" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), str))
    f.flush()



if __name__ == '__main__':
    pass
