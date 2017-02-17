# 运用pexpect模块模拟简单的人机交互的ssh登录
import pexpect

PROMPT=['# ','>>> ','> ','\$ ']
def send_command(child,cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user,host,password):
    ssh_newkey='Are you sure you want to continue connecting'
    connStr='ssh '+ user + '@'+host
    child=pexpect.spawn(connStr)
    ret=child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword:'])
    if ret==0:
        print('Error connecting')
        return
    if ret==1:
        child.sendline('yes')
        ret=child.expect([pexpect.TIMEOUT,'[p|P]assword:'])
    if ret==0:
        print('Error connecting')
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child
def main():
    host='123.207.28.159'
    user='ubuntu'
    password='LPL2016val!'
    child=connect(user,host,password)
    send_command(child,'ll /var')
    print(child.before)
if __name__ == '__main__':
    main()
#  pxssh模块是pexpect的SSH简化用法,可以直接用pxssh进行SSH的连接
# ,使用这个模块,会比pexpect简化一些代码,他能用预先写好的login(),logout(),prompt()
# 等函数直接与ssh进行交互
# from pexpect import pxssh
# def send_command(s,cmd):
#     s.sendline(cmd)
#     s.prompt()
#     print(s.before)
#
# def connect(host,user,password):
#     try:
#         s=pxssh.pxssh()
#         s.login(host,user,password)
#         return s
#     except:
#         print('Error Connecting')
#         return
#
# s=connect('127.0.0.1','root','root')
# send_command(s,'ls /var')
