from urllib.request import urlopen,Request,urlretrieve
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import os

def findImage(url):
    print('find images in '+url)
    headers={
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
    req=Request(url,headers=headers)
    html=urlopen(req)
    soup=BeautifulSoup(html,'lxml')
    images=soup.findAll('img')
    return images
def downloadImage(images):
    i=0
    for image in images:
        url=image['src']
        urlretrieve(url,'/home/ttwilight/images/'+str(i)+'.jpg')
        print(i)
        i=i+1
    print('finish')

def getGpsExif():
    # i=0
    # while i<len([os.listdir('/home/ttwilight/images/')]):
    #     path='/home/ttwilight/images/'+str(i)+'.jpg'
    #     imageFile=Image.open(path,'r')
    #     info=imageFile._getexif()
    #     i=i+1
    #     print(info)
    IAM=Image.open('/home/ttwilight/Wallpapers/HongKongEye_ZH-CN12285832688_1920x1080.jpg')
    info=IAM.info
    print(info)


url='https://www.zhihu.com/'
images=findImage(url)
downloadImage(images)
getGpsExif()

