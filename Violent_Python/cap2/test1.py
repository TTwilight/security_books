#简单的TCP连接扫描器

import optparse
from socket import *
from threading import *

screenLock=Semaphore(value=1)
def connScan(tgtHost,tgtPort):
    try:
        connSkt=socket(AF_INET,SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send(b'a')
        results=connSkt.recv(4096)
        screenLock.acquire()
        print(str(results))
        print('%d/tcp is open.' % tgtPort)
        connSkt.close()
    except:
        screenLock.acquire()
        print('%d/tcp is closed.' % tgtPort)
    finally:
        screenLock.release()

def portScan(tgtHost,tgtPorts):
    try:
        tgtIP=gethostbyname(tgtHost)
    except:
        print('cannot resolve "%s ": unknown hostname '% tgtHost)
    try:
        tgtName=gethostbyaddr(tgtIP)
        print('scan results for :' +tgtName[0])
    except:
        print('scan results for :' + tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t=Thread(target=connScan,args=(tgtHost,int(tgtPort)))
        t.start()


def main():
    parser=optparse.OptionParser('usage%prog '+'-H <target host> -p <target port>' )
    parser.add_option('-H',dest='tgtHost' ,type='string' ,help='specify target host')
    parser.add_option('-p',dest='tgtPort' ,type='string' ,help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost=options.tgtHost
    tgtPorts=str(options.tgtPort).split(',')
    print(tgtPorts)
    if (tgtHost==None) | (tgtPorts[0]==None):
        print('you must specify a target host and port[s].')
        exit(0)
    portScan(tgtHost,tgtPorts)
if __name__=='__main__':
    main()