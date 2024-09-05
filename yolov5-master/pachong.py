# 第一版
# -*-coding:utf-8-*-
import os
import re
import shutil
import time
from contextlib import nullcontext

import requests
import bs4
from bs4 import BeautifulSoup
import os.path
import shutil

# 手动写入目标套图的首页地址
download_url = "https://cn.bing.com/images/search?q=t%E6%81%A4%E5%9B%BE%E7%89%87%E5%A4%A7%E5%85%A8&qs=MM&form=QBIR&sp=4&lq=0&pq=t%E6%81%A4%E5%9B%BE%E7%89%87&sk=MM3&sc=10-4&cvid=29EE62C869114849B4BC11412D585301&first=1"

# 手动写入目标套图的页数
page_num = 1

# 创建一个文件夹用来保存图片
file_name = "D:\\own\\2024\\提案\\images\\测试图库3"

# 目标图片下载地址的前半部分(固定不变那部分，后半段是变化的，需要解析网页得到)
imgae_down_url_1 = "https://cn.bing.com"


# 创建文件夹
def CreateFolder(file):
    """创建存储数据文件夹"""
    flag = 1
    while flag == 1:  # 若文件已存在，则不继续往下走以免覆盖了原文件
        if not os.path.exists(file):
            os.mkdir(file)
            flag = 0
        else:
            print('该文件已存在，请重新输入')
            flag = 1
            time.sleep(1)
        # 返回文件夹的路径，这里直接放这工程的根目录下
        path = os.path.abspath(file) + "\\"
    return path


# 下载图片
def DownloadPicture(download_url, path):
    # 访问目标网址
    r = requests.get(url=download_url, timeout=30)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")

    # 解析网址，提取目标图片相关信息，注：这里的解析方法是不固定的，可以根据实际的情况灵活使用
    a = soup.find_all('div',{'class':'img_cont hoff'})
    # a = soup.find_all('div')

    # 下载图片
    j = 0
    aLen=len(a)
    for i in range(len(a)):
        if(i==21):
            continue
        tag = a[i].find_all("img")
        print('---------------')
        print(i)
        print(tag)
        print('---------------')
        if (tag!=None and (tag[0].get('src') != None or tag[0].get('data-src') != None)):
            img_name = str(i) + ".jpg"  # 以数字命名图片，图片格式为jpg
            # 获取目标图片下载地址的后半部分
            if(tag[0].get('src') != None):
                imgae_down_url_2 = tag[0].attrs['src']
            elif (tag[0].get('data-src') != None):
                imgae_down_url_2 = tag[0].attrs['data-src']
            # 把目标图片地址的前后两部分拼接起来，得到完整的下载地址
            imgae_down_url = imgae_down_url_2
            print("imgae_down_url: ", imgae_down_url)

            # 下载图片
            try:
                img_data = requests.get(imgae_down_url)
            except:
                continue
            # 保存图片
            img_path = path + img_name
            with open(img_path, 'wb') as fp:
                fp.write(img_data.content)
            print(img_name, "   ******下载完成！")

num = 0
def rename(img_folder):
    for img_name in os.listdir(img_folder):  # os.listdir()： 列出路径下所有的文件
        #os.path.join() 拼接文件路径
        global num
        src = os.path.join(img_folder, img_name)   #src：要修改的目录名
        dst = os.path.join(img_folder, str(num) + '.jpg') #dst： 修改后的目录名      注意此处str(num)将num转化为字符串,继而拼接
        num= num+1
        os.rename(src, dst) #用dst替代src

def moveFiles(path, disdir):  # path为原始路径，disdir是移动的目标目录
    dirlist = os.listdir(path)
    for i in dirlist:
        child = os.path.join('%s/%s' % (path, i))
        if os.path.isfile(child):
            imagename, jpg = os.path.splitext(i)  # 分开文件名和后缀
            shutil.copy(child, os.path.join(disdir, imagename + ".jpg"))#保存格式自己设置
            # 复制后改为原来图片名称
            # 也可以用shutil.move()
            continue
        moveFiles(child, disdir)

# 将多个文件夹图片合到一起
def renameTestImagesToOne():
    img_folder0='D:/own/2024/提案/yolov5-base/yolov5-master/yolov5-master/own_datas/images/train'
    disdir = 'D:\\own\\2024\\提案\\images\\1'  # 移动到目标文件夹

    rename(img_folder0)

    # moveFiles(img_folder0, disdir)



# 主函数
if __name__ == "__main__":
    # # 创建保存数据的文件夹
    # path = CreateFolder(file_name)
    # print("创建文件夹成功: ", path)
    #
    # # 按页下载图片
    # for i in range(0, page_num):
    #     print('第'+str(i)+'页')
    #     if i == 0:
    #         page_url = download_url  # 首页网址，注：因为这个网站首页和后面那些页面网址的规则不一样，所以这里要区分开来
    #     else:
    #         page_url = download_url[:-5] + "_" + str(i) + ".html"  # 第2页往后的网址，都是用数字来排布页面
    #     # 下载图片
    #     print("page_url: ", page_url)
    #     DownloadPicture(page_url, path)  # 注:这个网站每一页最多是3张图片，每张图片我都用数字命名
    #
    # print("全部下载完成！", "共" + str(len(os.listdir(path))) + "张图片")

    renameTestImagesToOne()
