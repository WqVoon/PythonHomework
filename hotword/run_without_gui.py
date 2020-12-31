# 用 shell 进行交互的客户端

from backend.cp import ContentProvider as CP
from utils import Loger, SUPPORTED_KEYS

Loger.is_debug_mode = True

cls_prompt = ("请输入新闻类别:\n " +
	" ".join([
		f"{idx}: {SUPPORTED_KEYS[idx]}"
		for idx in range(len(SUPPORTED_KEYS))
	]) +
	"\n> ")

cnt_prompt = "请输入热词数量:\n> "

while True:
	try:
		idx = int(input(cls_prompt))
		cnt = int(input(cnt_prompt))

		CP.get_info(SUPPORTED_KEYS[idx])
		print(f"新闻热词 Top{cnt}")
		for word, cnt in CP.get_topn(cnt):
			print(f"\t“{word}” 出现了 {cnt} 次")

	except (KeyboardInterrupt, EOFError):
		print("Bye")
		break
