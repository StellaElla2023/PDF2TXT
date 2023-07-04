import fitz
import os
import time
import re
import requests
import base64
import random
 
fileDir = r'D:\比赛\财务数智化第二节\pdf'
APIKey = 'PeUW1e3Ujx9Wgxc50TG2Vxly'
SecretKey = 'T4ShQfNLQF1orY0pE0s39dLgcTgGKA11'
    
def pdf_to_pic(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        zoom_x = 2 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_{}.png'.format(pg))#将图片写入指定的文件夹内
        #print('pdf to pic: No.{}'.format(pg))
    return pdfDoc.pageCount

def pic_to_txt(imagePath,pdfPath,txtPath):    
    global txt
    txt = ''
    files = os.listdir(imagePath)
    files.sort(key= lambda x:int(re.findall(r'\d+',x)[0]))
    for file in files:
        if int(re.findall(r'\d+',file)[0]) % 10 == 0: print('pic to txt: ' + file) 
        file = imagePath + '\\' + file
        for i in range(10):  
            try:
                page = img_to_str(file, txt)
                time.sleep(random.random())
                break
            except:
                print('Try again')
                continue
        txt += page
        fw = open(txtPath,'w',encoding='utf-8')   # a追加写
        fw.write(txt)
        fw.close()

    
def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()
 
def img_to_str(image_path,txt):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img, 'paragraph':'true'}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    result = response.json()
    page = ''
    for item in result['paragraphs_result']:
        para = ''
        para_idx =  item['words_result_idx']
        for i in para_idx:
            if result['words_result'][i]['words'] not in txt:
                para += result['words_result'][i]['words']
        #print(para)
        page += para + '\n'
    return page[:-1]

def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(APIKey, SecretKey)
    response = requests.get(host)
    return response.json()['access_token']
 
if __name__ == "__main__":
    global access_token
    access_token = get_token()
    files = os.listdir(fileDir)
    if not os.path.exists(fileDir +'\\txt'):
        os.makedirs(fileDir +'\\txt')
    for file in files:
        if 'pdf' in file or 'PDF' in file:
            pdfPath = fileDir + '\\' + file
            txtPath = fileDir +'\\txt\\' + file.replace('pdf','txt').replace('PDF','txt')
            imagePath = fileDir +'\\image\\' + file[:-4]
            if not os.path.exists(imagePath):
                pdf_to_pic(pdfPath, imagePath)
                print('Picture Done')
            if not os.path.exists(txtPath):
                start = time.time()
                print(file)
                pic_to_txt(imagePath,pdfPath,txtPath)
                end = time.time()
                print('Time used: {:.4f}s'.format(end-start))
                print()