from email import header
from sqlite3 import connect
from turtle import ht, pen
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

class Light_download:
    def __init__(self):
        self.url='https://www.wenku8.net/novel/2/2255/index.htm'#轻小说网址
        self.url_list='https://www.wenku8.net/novel/2/2255/'
        self.header={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
        }#请求头
        self.list_contect=list()#每话标题
        self.list_name=list()#每话地址
        self.path='C://Users//86181//Desktop//魔女之旅//'#文本本地下载路径
        self.png_url=list()#每章插图网址
        self.png_contect_url=list()#每张图片地址
        self.path_png=''#图片本地下载地址
        self.timeout=10#超时重新请求次数
        
    def get_download_url(self):
        for i in range(self.timeout):
            try:
                req=requests.get(url=self.url,headers=self.header,timeout=5)
                if req.status_code==200:
                    break
            except:
                print("章节网址请求超时")
        html=req.text.encode('ISO-8859-1')
        a_bf=BeautifulSoup(html,'lxml')
        a=a_bf.find_all(class_='ccss')
        a_href_bf=BeautifulSoup(str(a),'lxml')
        a_href=a_href_bf.find_all('a')
        for i in a_href:
            self.list_contect.append(i.string)
            self.list_name.append(self.url_list+i.get('href'))
            #print(i.string)
            #print(self.url+i.get('href'))
    
    def get_png_url(self):
        for i in range(self.timeout):
            try:
                req=requests.get(url=self.url,headers=self.header,timeout=5)
                if req.status_code==200:
                    break
            except:
                print("章节插图请求超时")
        html=req.content.decode('gbk')
        n_bf=BeautifulSoup(html,'xml')
        n=n_bf.find_all(class_='ccss')
        a_href_bf=BeautifulSoup(str(n),'lxml')
        a_href=a_href_bf.find_all('a')
        for i in a_href:
            if i.string=='插图':
                self.png_url.append(self.url_list+i.get('href'))
                
    def get_every_png(self,url):
        for i in range(self.timeout):
            try:
                req=requests.get(url=url,headers=self.header,timeout=5)
                if req.status_code==200:
                    break
            except:
                print("插图请求超时")
        html=req.content.decode('gbk')
        n1_bf=BeautifulSoup(html,'xml')
        n1=n1_bf.find_all(class_='imagecontent')
        for i in n1:
            self.png_contect_url.append(i.get('src'))
            
    def get_contect(self,url):
        for i in range(self.timeout):
            try:
                req=requests.get(url=url,headers=self.header,timeout=5)
                if req.status_code==200:
                    break
            except:
                print("小说内容请求超时")
        html=req.text.encode('ISO-8859-1')
        all_bf=BeautifulSoup(html,'lxml')
        all=all_bf.find_all(id='content')
        contect=str(all[0])
        contect=contect.replace("<br/>","")
        contect=contect.replace('<ul id="contentdp">最新最全的日本动漫轻小说 轻小说文库(http://www.wenku8.com) 为你一网打尽！</ul>','')
        contect=contect.replace("</div>","")
        contect=contect.replace('<div id="content">','')
        contect=contect.replace('<ul id="contentdp">','')
        contect=contect.replace('(http://www.wenku8.com)</ul>','')
        return contect
    
    def wirte(self,path,contect:str,name:str,i:int):
        path=path+name+'.txt'
        print(path)
        txt=open(path,'a',encoding='utf-8')
        txt.write(book.list_contect[i])
        txt.write(contect)
        txt.close()
        
    def png_download(self,url,a):
        for i in range(self.timeout):
            try:
                r = requests.get(url=url,headers=self.header,timeout=5)
                if r.status_code==200:
                    break
            except:
                print("插图下载请求超时")
        with open('C://Users//86181//Desktop//魔女之旅图片/'+a, 'wb') as f:
            f.write(r.content)
        

qaq=list()#储存本地文件名
book=Light_download()
book.get_download_url()
print("文本开始下载")
for i in tqdm(range(0,len(book.list_contect))):
    book.wirte(book.path,book.get_contect(book.list_name[i]),book.list_contect[i],i)
    time.sleep(0.05)
print("下载完成")

book.get_png_url()

print("加载网页地址")
for i in tqdm(book.png_url):
    book.get_every_png(i)
    time.sleep(0.05)
print("加载完成")

print("生成本地地址")
for i in tqdm(range(0,300)):
    qaq.append(str(i)+'.png')
    time.sleep(0.05)
print("生成完成")

print("图片开始下载")
for i in tqdm(range(0,len(book.png_contect_url))):
    book.png_download(book.png_contect_url[i],qaq[i])
    time.sleep(0.05)
print("下载完成")
