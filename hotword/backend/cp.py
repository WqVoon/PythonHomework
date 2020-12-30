from .data_getter import CrawlerController as CC
from .data_getter import WordCounter as WC
from .url_handler import URLGetter as UG
from utils import Loger, SUPPORTED_KEYS
from json import load, dump
from time import time


class ContentProvider:
	"""
	后端的主要对象，用于获取对应类别的新闻中的热词信息
	"""

	cache = None

	@staticmethod
	def init():
		"""
		加载缓存到内存中
		"""
		try:
			with open('cache.json') as f:
				CP.cache = load(f)
		except Exception:
			CP.cache = {}

	@staticmethod
	def get_info(cls, cnt=10):
		"""
		根据当前内容来从缓存或网页获取热词信息
		"""
		cls = CP.regularize_input(cls)
		cached_item = CP.cache.get(cls, {'timestamp': 0, 'cnt': 0})
		timestamp = cached_item['timestamp']
		if CP.is_overtime(timestamp) or cached_item['cnt'] < cnt:
			CP.__get_info_from_server(cls, cnt)
		else:
			CP.__get_info_from_cache(cls)

	@staticmethod
	def __get_info_from_cache(cls):
		log("从缓存获取热词信息")
		items = CP.cache[cls]['data']
		WC.update_result(items)

	@staticmethod
	def __get_info_from_server(cls, cnt):
		log("从网页爬取热词信息")
		try:
			UG.get_urls(cls, cnt)
			CC.get_data()
			CP.save_cache(cls, cnt)
		except Exception as err:
			log(f"查询失败，原因{err}")

	@staticmethod
	def save_cache(cls, cnt):
		"""
		更新内存中的缓存内容，并将其写入文件
		"""
		CP.cache[cls] = {
			'cnt': cnt,
			'timestamp': time(),
			'data': WC.get_all_data()
		}
		try:
			with open('cache.json', 'w') as f:
				dump(CP.cache, f)
		except Exception as err:
			log(f"写入缓存失败，原因:{err}")

	CACHE_TIME = 60 * 60 * 12

	@staticmethod
	def is_overtime(before):
		"""
		查看缓存是否已经失效
		"""
		return time() - before > CP.CACHE_TIME

	__valid_input = SUPPORTED_KEYS

	@staticmethod
	def regularize_input(cls):
		"""
		使输入合法化
		"""
		if cls not in CP.__valid_input:
			raise Exception("不支持的新闻类别")
		return cls.strip()


# 设置两个引用来简化调用过程
log = Loger.log
CP = ContentProvider

# 初始化 CP 的状态
CP.init()
