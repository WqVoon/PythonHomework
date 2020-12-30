from .url_handler import URLGetter as UG
from threading import RLock, Thread
from utils import get, FETCH_DELAY, Loger
from bs4 import BeautifulSoup as bs
from jieba import cut
from time import sleep

log = Loger.log


class WordCounter:
	"""
	线程安全的单词计数器
	"""
	__map = dict()  # 键为单词，值为数量
	__lock = RLock()  # 为实现线程安全而做的锁
	__result = None  # 保存排序后的 map

	@staticmethod
	def reset():
		"""
		重置计数器状态，方便下次使用
		"""
		WordCounter.__map.clear()
		WordCounter.__result = None
		log("计数器状态已重置")

	@staticmethod
	def add_word(w):
		"""
		将单词线程安全地加入到 __map 中
		"""
		map_ref = WordCounter.__map
		with WordCounter.__lock:
			log(f"添加 {w} 到 WordCounter 中")
			map_ref[w] = map_ref.get(w, 0) + 1

	@staticmethod
	def get_topn(n):
		"""
		若未排序过则先排序
		返回占比最大的 n 个词
		"""
		if WordCounter.__result is None:
			WordCounter.sort_data()

		return WordCounter.__result[:n]

	@staticmethod
	def get_all_data():
		"""
		若未排序过则先排序
		返回 __result 的浅拷贝
		"""
		if WordCounter.__result is None:
			WordCounter.sort_data()

		return WordCounter.__result

	@staticmethod
	def sort_data():
		"""
		更新 __result 属性为排序后的列表
		"""
		WordCounter.__result = list(sorted(
			WordCounter.__map.items(),
			key=lambda item: item[1],
			reverse=True
		))

	@staticmethod
	def update_result(new_result):
		"""
		更新 __result 属性，为缓存功能提供服务
		"""
		WordCounter.__result = new_result


class CrawlerController:
	"""
	爬虫对象的控制对象
	"""
	THREAD_COUNT = 5

	@staticmethod
	def get_data():
		"""
		创建 THREAD_COUNT 个线程来爬取 UG.task_queue 中的数据
		同时阻塞主线程直到所有数据被消耗干净
		"""
		WordCounter.reset()
		for i in range(CrawlerController.THREAD_COUNT):
			Crawler().start()

		UG.task_queue.join()


class Crawler(Thread):
	"""
	爬虫对象，完成如下任务：
	- 从 URLGetter.task_queue 中获取 url
	- 发出请求
	- 提取请求中的正文
	- 使用 jieba 进行切词
	- 将单词统计到 WordCounter 中
	"""

	def __init__(self):
		Thread.__init__(self)

	def run(self):
		"""
		线程对象的 target，不断地重复上述任务直到 task_queue 为空
		"""
		while not UG.task_queue.empty():
			Crawler.do_task()

	@staticmethod
	def do_task():
		try:
			url = UG.task_queue.get()
			res = get(url).content.decode('utf8')
			root = bs(res, 'html.parser')

			for text in Crawler.get_main_body(root):
				for token in cut(text):
					log(f"解析出 {token}")
					if len(token) > 1:
						WordCounter.add_word(token)
		except Exception as err:
			log(f'解析失败，原因:{err}')

		UG.task_queue.task_done()
		sleep(FETCH_DELAY)

	@staticmethod
	def get_main_body(doc):
		"""
		从 html 文档中返回正文部分
		只按照下述方式提取，提取失败则认为正文为空
		"""
		try:
			ps = doc.find(
				'div', class_='content_area'
			).find_all('p')
		except Exception:
			ps = []

		return [p.text[2:] for p in ps]
