import pyPdf
from pyPdf import PdfFileReader,PdfFileWriter

def printMeta(fileName):
    f=open(fileName,'rb')
    pdfFile=PdfFileReader(f)
    docInfo=pdfFile.getDocumentInfo()
    print("[*] PDF META "+str(fileName))
    for metaItem in docInfo:
        print('[+] '+metaItem+':'+docInfo[metaItem])
    f.close()

if __name__ == '__main__':
    fileName=input()
    printMeta(fileName)
