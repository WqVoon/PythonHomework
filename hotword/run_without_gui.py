# 用 shell 进行交互的客户端

from backend.cp import ContentProvider as CP
from backend.data_getter import WordCounter as WC
from utils import Loger, SUPPORTED_KEYS

Loger.is_debug_mode = True

idx = int(input(
	"请输入新闻类别:\n " +
	" ".join([
		f"{idx}: {SUPPORTED_KEYS[idx]}"
		for idx in range(len(SUPPORTED_KEYS))
	]) +
	"\n> "
))
cnt = int(input("请输入热词数量:\n> "))

CP.get_info(SUPPORTED_KEYS[idx])

print(WC.get_topn(cnt))
