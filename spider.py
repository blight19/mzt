from Download import request
from bs4 import BeautifulSoup
from Mongo_queue import mongo_queue
from multiprocessing import Process,cpu_count
import os
img_queue = mongo_queue('meinvxiezhenji','old')
def crawl(url):
	urls = []
	res = request.get(url)
	soup = BeautifulSoup(res.text,'lxml')
	page_num = soup.find('div',class_='pagenavi').find_all('a')[-2].find('span').text
	title = soup.find('head').find('title').text
	for page in range(1,int(page_num)+1):
		page_url = url+'/'+str(page)
		response = request.get(page_url)
		img_soup = BeautifulSoup(response.text,'lxml')
		img_url = img_soup.find('div',class_='main-image').find('p').find('img')['src']
		print(img_url)
		save_img(img_url,title)
		
def save_img(url,title):
	img = request.get(url).content
	name = url[-9:-4].replace('/','')
	mkdir(title)
	f = open(name+'.jpg','ab')
	f.write(img)
	f.close()
def mkdir(title):
	title.strip()
	try:
		os.makedirs('E://mzt//'+title)
		os.chdir('E://mzt//'+title)
	except Exception as e:
		os.chdir('E://mzt//'+title)
def main():
	while True:
		url = img_queue.get_url()
		print('爬取中。。。'+url)
		crawl(url)
		print('爬取完毕：'+url)
		img_queue.complete(url)
if __name__ == '__main__':
    process = []
    num_cpus = cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus*10):
        p = Process(target=main) ##创建进程
        p.daemon = True
        p.start() ##启动进程
        
        process.append(p) ##添加进进程队列
    for p in process:
        p.join() ##等待进程队列里面的进程结束
		
