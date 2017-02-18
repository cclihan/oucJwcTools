'''
Created on 2017年2月16日

@author: 栩夕
本模块拥有模型训练及模型测试
模型训练: 将每一行的黑点数和每一列的黑点数做为 样本的特征值然后通过svm训练
模型测试: 将传入的文件进行测试,返回结果
'''

from PIL import Image
from pylogin.svmutil import svm_read_problem,svm_train,svm_save_model,svm_load_model,\
svm_predict
import os

#************************************获取特征值********************************************#
def get_feature(img):
    
    img = img.convert('RGBA')
    #pix = img.load()
    width = img.size[0]              
    height = img.size[1]
    pixel_cnt_list = []
    
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == (0,0,0,255):  # 黑色点

                pix_cnt_x += 1
        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == (0,0,0,255):  # 黑色点

                pix_cnt_y += 1
        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

#************************************训练样本********************************************#
def train_new(filename, path_new,tag='0'):
    if os.path.exists(filename):
        os.remove(filename)
    result_new = open(filename, 'a')
    
    for f in os.listdir(path_new):
        
        if f.endswith(".tiff"):
           
            pic = Image.open(path_new + f)
            pixel_cnt_list = get_feature(pic)

            if ord(tag) >= 65:
                line = str(ord(tag)+32) + " "
            else:
                line = tag + ' '
 
            for i in range(1, len(pixel_cnt_list) + 1):
                line += "%d:%d " % (i, pixel_cnt_list[i - 1])
            result_new.write(line + "\n")
    result_new.close()


#************************************模型训练********************************************#
def train_svm_model(filename):
    y, x = svm_read_problem(filename)
    model = svm_train(y, x)
    svm_save_model("svm_model_file", model)
    print('2')


#************************************模型测试********************************************#
def svm_model_test(filename):
    yt, xt = svm_read_problem(filename)
    model = svm_load_model("svm_model_file")
    p_label, p_acc, p_val = svm_predict(yt, xt, model)  # p_label即为识别的结果

    cnt = 0
    results = []
    result = ''
    for item in p_label:  # item:float

        if int(item) >= 97:
            result += chr(int(item))
        else:
            result += str(int(item))
        cnt += 1
        if cnt % 4 == 0:
            results.append(result)
            result = ''
    return results
'''
list1 = ['2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K'\
        ,'M','N','P','Q','R','S','T','U','V','W','X','Y','Z']

for tag in list1:
    
    print(tag)
    base_path = 'C:/Users/栩夕/workspace/123/pylogin/hejisvm/%s/'%tag
    t = train_new(tag,'oucChaTrain.txt', base_path)
print('1')

train_svm_model('oucChaTrain.txt')
'''


