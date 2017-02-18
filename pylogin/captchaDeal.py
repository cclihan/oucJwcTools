'''
Created on 2017年2月16日

@author: 栩夕

在外面通过使用getCaptcha(captcha_img)函数来获取验证码的值


'''

from PIL import Image
from pylogin.svmtraining import train_new,svm_model_test


#************************************图片灰度二值化********************************************#
def get_bin_table():
    threshold = 80
    table = []
    for ii in range(256):
        if ii < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def set_table(a):
    table=[]
    for i in range(256):
        if i<a:
            table.append(0)
        else:
            table.append(1)
    return table

def toGrey(im):
    imgry = im.convert('L')  # 转化为灰度图

    table = get_bin_table()
    out = imgry.point(set_table(140), '1')   #这里可以设置阈值
    return out



#************************************降噪处理********************************************#
def deal_img(img):
    img = img.convert('RGBA')  
    pix = img.load()  # 读取为像素
    for x in range(img.size[0]):  
        pix[x, 0] = pix[x, img.size[1] - 1] = (255, 255, 255, 255)
    for y in range(img.size[1]): 
        pix[0, y] = pix[img.size[0] - 1, y] = (255, 255, 255, 255)


    for x in range(1,img.size[0]-1):
        for y in range(1,img.size[1]-1):
            sumb = (img.getpixel((x-1,y))==(255,255,255,255))\
                   +(img.getpixel((x+1,y))==(255,255,255,255))\
                   +(img.getpixel((x,y-1))==(255,255,255,255))\
                   +(img.getpixel((x,y+1))==(255,255,255,255))
            
            if sumb == 3 or sumb ==4 :
                pix[x, y] = (255, 255, 255, 255)
    return img            
    
#************************************分割图片********************************************#
def spiltimg(img):
    
    child_img_list = []
    y1 = 6
    y2 = 29
    child_img_1 = img.crop((8,y1,22,y2))#child_img = img.crop((x, y, x + 9, img.height - 2))
    child_img_2 = img.crop((23,y1,37,y2))
    child_img_3 = img.crop((38,y1,52,y2))
    child_img_4 = img.crop((53,y1,67,y2))
        
    child_img_list.append(child_img_1)
    child_img_list.append(child_img_2)
    child_img_list.append(child_img_3)
    child_img_list.append(child_img_4)
    return child_img_list

#************************************获取验证码********************************************#
def getCaptcha(captcha_img):
    #for f in os.listdir(pic_path):
    #    if os.path.isfile(pic_path + f):
    #        if f.endswith(".jpg"):
    pic = Image.open(captcha_img)
    pic = toGrey(pic)
    pic = deal_img(pic)
    pic.save("1-%d.jpg")
    pic = Image.open("1-%d.jpg")
            
    childs = spiltimg(pic)
    count = 0
    for c in childs:
        each = '2-%d.tiff'%count
        c.save(each)
        #image = Image.open(each)        
        count += 1

    train_new('teex.txt','C:/Users/栩夕/workspace/123/pylogin/')

    result = svm_model_test('teex.txt')
    return result[0]


