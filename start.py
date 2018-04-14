from Mongo_queue import mongo_queue
from Download import request
from bs4 import BeautifulSoup
index_queue = mongo_queue('meinvxiezhenji','old')
def main():
	res = request.get('http://www.mzitu.com/old/')
	soup = BeautifulSoup(res.text,'lxml')
	
	all_a = soup.find('div', class_='all').find_all('a')
	for a in all_a:
		title = a.get_text()
		url = a['href']
		index_queue.push_title(url,title)	

if __name__ == '__main__':
	main()