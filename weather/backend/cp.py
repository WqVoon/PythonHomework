from utils import Loger, get, URLBuilder as ub
from json import load, dump
from string import Template
from re import compile
from time import time


class ContentProvider:
	"""
	后端的主要对象，用于从接口中获得天气信息
	类属性 cache 存放缓存的信息
	类属性 __info_template 用于提供 self.ret_info 的模版
	"""

	cache = {}

	@staticmethod
	def init():
		"""
		从文件中加载缓存
		"""
		try:
			with open("../cache.json") as f:
				CP.cache = load(f)
		except Exception:
			CP.cache = {}

	__info_template = Template(
		"城市：$city\n" +
		"天气：$wea\n" +
		"湿度：$humidity\n" +
		"当前温度：$cur_tem\n" +
		"最高气温：$max_tem\n" +
		"最低气温：$min_tem\n" +
		"空气质量：$air_level\n"
	)

	def __init__(self):
		self.err = ""  # 用于提供错误信息
		self.tip = ""  # 接口提供的小提示
		self.wea_img = ""  # 指明使用哪个图片
		self.ret_info = ""  # 整理好的天气信息

	def get_weather_info(self, city_name):
		"""
		根据当前时间来从缓存或api来获取天气信息
		"""
		self.__init__()
		city = CP.regularize_input(city_name)

		cached_item = CP.cache.get(city, {'timestamp': 0})
		timestamp = cached_item['timestamp']
		if CP.is_overtime(timestamp):
			self.__get_weather_info_from_api(city)
		else:
			self.__get_weather_info_from_cache(city)

	def __get_weather_info_from_cache(self, city_name):
		"""
		根据提供的城市名来从 缓存 获取天气信息
		"""
		log("从缓存获取了信息")
		info = CP.cache[city_name]['info']
		self.__update_self_data(info)
		return info

	def __get_weather_info_from_api(self, city_name):
		"""
		根据提供的城市名来从 api 获取天气信息
		"""
		log("从API获取了信息")
		info = {}
		try:
			res = get(ub.get_url(city=city_name))
			info = res.json()

			if info.get('errcode') is not None:
				raise Exception('请求参数有误')
			if info['city'] != city_name:
				raise Exception('无效的城市名')

			self.__update_self_data(info)
			CP.save_cache(city_name, info)
		except Exception as err:
			log(f"查询出错, 原因:{err}")
			self.err = "查询失败"
		finally:
			return info

	def __update_self_data(self, info):
		"""
		利用 info 中的信息来更新本实例中的属性
		"""
		self.tip = info['air_tips']
		self.wea_img = info['wea_img'] + ".gif"
		self.ret_info = CP.__info_template.safe_substitute(
			city=info['city'],
			wea=info['wea'],
			cur_tem=info['tem'],
			max_tem=info['tem1'],
			min_tem=info['tem2'],
			humidity=info['humidity'],
			air_level=info['air_level']
		)

	blacklist = compile("([市区])")

	@staticmethod
	def regularize_input(msg):
		"""
		使用户的输入合法化，去除两端空格以及“市”和“区”等字
		"""
		return CP.blacklist.sub('', msg.strip())

	CACHE_TIME = 60 * 30  # 缓存的秒数，超时则更新缓存

	@staticmethod
	def is_overtime(before):
		"""
		判断缓存的内容是否已经过时
		"""
		return time() - before > CP.CACHE_TIME

	@staticmethod
	def save_cache(city, info):
		"""
		更新内存中的缓存内容，并将其写入文件
		"""
		CP.cache[city] = {
			'timestamp': time(),
			'info': info
		}
		try:
			with open('cache.json', 'w') as f:
				dump(CP.cache, f)
		except Exception as err:
			log(f"写入缓存失败，原因:{err}")

	@staticmethod
	def bind(func):
		"""
		做装饰器用，给动作函数提供 ContentProvider 对象
		"""
		cp = CP()  # 这一步是必须的，否则所有动作函数都会得到同一个 CP 对象
		return lambda *args: func(cp, *args)


# 设置两个引用来简化调用过程
log = Loger.log
CP = ContentProvider

# 初始化 CP 的状态
CP.init()
