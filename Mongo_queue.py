from pymongo import MongoClient,errors
class mongo_queue():
	OUTSTANDING = 0#还未爬取
	PROCESSING = 1#正在爬取
	COMPLETE =2#爬取完成
	def __init__(self,db,collection):
		self.client = MongoClient()
		self.Client = self.client[db]
		self.db = self.Client[collection]
	def push_title(self,url,title):
		try:
			result = self.db.insert({'_id':url,'title':title,'statues':self.OUTSTANDING})
			print('插入数据成功')
		except errors.DuplicateKeyError as e:
			print('重复数据')
	def push_img(self,img_url):
		try:
			result = self.db.insert({'_id':img_url,'statues':self.OUTSTANDING})
			print('插入数据成功')
		except errors.DuplicateKeyError as e:
			print('重复数据')
	def complete(self,url):
		try:
			self.db.update({'_id':url},{'$set':{'statues':self.COMPLETE}})
		except Exception as e:
			raise e
	def get_url(self):
		record = self.db.find_and_modify(
            query={'statues': self.OUTSTANDING},
            update={'$set': {'statues': self.PROCESSING}}
        )
		if record:
			return record['_id']
		else:
			
			raise KeyError


