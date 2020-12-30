from utils import get, Loger, FETCH_DELAY, SUPPORTED_CLASS, URL_TEMPLATE
from queue import Queue
from re import compile
from time import sleep

log = Loger.log


class URLBuilder:
	"""
	根据类别和索引来拼接请求的 url
	"""
	__map = SUPPORTED_CLASS
	__url_template = URL_TEMPLATE

	@staticmethod
	def get_url(cls, idx):
		return URLBuilder.__url_template.format(
			URLBuilder.__map[cls],
			idx
		)


class URLGetter:
	"""
	根据用户选择的类别来获取其新闻列表
	列表中记录着每篇文章的实际 url，并放在 task_queue 中等待
	"""

	task_queue = Queue()
	__total_task_count = 0
	__finished_task_count = 0

	@staticmethod
	def get_urls(cls, limit=-1):
		"""
		根据类别来获取对应类别的所有文章的 url，放到 task_queue 中
		"""
		log("准备根据类别获取 URL 并加入到任务队列")
		if not URLGetter.task_queue.empty():
			URLGetter.task_queue = Queue()

		queue = URLGetter.task_queue
		idx = 1
		content = get(URLBuilder.get_url(cls, 1)).text
		total = URLGetter.__get_item_count(content) if limit < 0 else limit

		while queue.qsize() < total:
			content = get(URLBuilder.get_url(cls, idx)).text if queue.qsize() else content
			for url in URLGetter.__get_item_urls(content):
				log(f"加入 {url} 到任务队列")
				URLGetter.task_queue.put(url)

				if queue.qsize() == total:
					break

			idx += 1
			sleep(FETCH_DELAY)

		size = queue.qsize()
		log(f"任务队列装填完毕, 共 {size} 条 URL")

	# 用于获取实际的词条总数量的正则模式
	__total_pattern = compile(r'"total":(\d+)')

	@staticmethod
	def __get_item_count(item):
		"""
		用于获取实际的词条总数量
		"""
		return int(URLGetter.__total_pattern.findall(item)[0])

	# 用于提取出词条的 url 的正则模式
	__real_url_pattern = compile(r'https://news.cctv.com/.*?.shtml')

	@staticmethod
	def __get_item_urls(item):
		"""
		用于提取出词条的 url, 该 url 可用于获取实际的新闻内容
		"""
		return URLGetter.__real_url_pattern.findall(item)
