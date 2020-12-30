from requests import get as old_get

# 访问 jsonp 时的模版，下面的模版用来配合 get_from_file 使用本地文件进行测试
URL_TEMPLATE = "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/{}_{}.jsonp"
# URL_TEMPLATE = "./test_data/{}_{}.jsonp"

# 爬取数据的延时
FETCH_DELAY = 2

# 支持的新闻类别
SUPPORTED_CLASS = {
	'主页': 'news',
	'国内': 'china',
	'国际': 'world',
	'社会': 'society',
	'法制': 'law',
	'文娱': 'ent',
	'科技': 'tech',
	'生活': 'life'
}
SUPPORTED_KEYS = list(SUPPORTED_CLASS.keys())


class Loger:
	"""
	仅在调试模式下输出调试信息
	"""
	is_debug_mode = True

	@staticmethod
	def log(msg):
		if Loger.is_debug_mode:
			print(f"[DEBUG] {msg}")


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


# 这一坨用来测试, TestObj 模拟 requests.Response 对象
# get_from_file 模拟 requests.get 方法
class TestObj:
	def __init__(self, data):
		self.text = data


def get_from_file(url):
	with open(url) as f:
		return TestObj(f.read())
