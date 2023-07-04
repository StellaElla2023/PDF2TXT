# -*- coding:utf-8 -*-
import os,re,time
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

fileDir = r'Your Folder'  # Folder containing the pdf files
# Output: all the txt files under the `fileDir\txt` folder

def pdfTotxt(filepath,outpath,file):
    try:
        fp = open(filepath, 'rb')
        outfp = open(outpath,'w', encoding='utf-8')
        rsrcmgr = PDFResourceManager(caching = False)
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams,imagewriter=None)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        fp.close()
        device.close()
        outfp.flush()
        outfp.close()
        print("Saved: "+ file)
    except Exception as e:
         print("Exception:%s",file)

def fileTotxt(fileDir):
    files = os.listdir(fileDir)
    tarDir = fileDir + '\\txt'
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    replace = re.compile(r'\.pdf',re.I)    
    for file in files:
        filePath = fileDir+'\\'+file
        outPath = tarDir+'\\'+re.sub(replace,'',file)+'.txt'
        if not os.path.isfile(outPath):
            start = time.time()
            pdfTotxt(filePath,outPath,file)
            end = time.time()
            print('TIme Used: {:.2f}s'.format(end-start))
            print()
    
if __name__ == '__main__':  
    fileTotxt(fileDir)
