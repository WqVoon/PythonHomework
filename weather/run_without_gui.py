# 用 shell 进行交互的客户端

from backend.cp import ContentProvider as CP
from utils import Loger

Loger.is_debug_mode = True


@CP.bind
def action(cp, city_name):
	cp.get_weather_info(city_name)
	if cp.err:
		print(cp.err)
	else:
		print(cp.ret_info)


while True:
	try:
		action(input("请输入城市名:"))
	except (EOFError, KeyboardInterrupt):
		print("\nBye")
		break
