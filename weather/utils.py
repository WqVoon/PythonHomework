from json import load
from requests import get as old_get


class Loger:
	"""
	仅在调试模式下输出调试信息
	"""
	is_debug_mode = True

	@staticmethod
	def log(msg):
		if Loger.is_debug_mode:
			print(f"[DEBUG] {msg}")


class URLBuilder:
	"""
	根据 url_info.json 中的内容来拼接请求的 url
	该对象在模块被 import 后会生成对象作用域的 url 前缀
	参数则通过 get_url 方法来拼接
	"""

	url = None

	@staticmethod
	def init():
		with open("url_info.json") as f:
			info = load(f)

			URLBuilder.url = info['url'] + '&'.join([
				f"{key}={value}"
				for key, value in info['args'].items()
			]) + '&'

	@staticmethod
	def get_url(**args):
		"""
		根据 args 中的内容来与 url 前缀进行拼接
		返回拼接后的完整 url
		"""
		return URLBuilder.url + '&'.join([
			f"{key}={value}"
			for key, value in args.items()
		])


UserAgent = " ".join([
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6)",
	"AppleWebKit/537.36 (KHTML, like Gecko)",
	"Chrome/87.0.4280.88 Safari/537.36"
])


def get(url):
	"""
	requests.get 的包装函数，修改了 UA
	并在内部调用 raise_for_status 函数
	"""
	res = old_get(url, headers={'User-Agent': UserAgent})
	res.raise_for_status()
	return res


# 初始化 URLBuilder 的状态
URLBuilder.init()
