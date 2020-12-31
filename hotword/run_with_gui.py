from backend.cp import ContentProvider as CP
from frontend.ui import ClsChooser, FormChooser
from frontend.drawers import Drawers
from utils import Loger, SUPPORTED_KEYS
import tkinter as tk

Loger.is_debug_mode = True


def gen_btn_action(c, f):
	"""
	利用闭包生成一个绑定了 ClsChooser 和 FormChooser 的动作函数
	"""
	def inner_func():
		cls = c.get_value()
		form = f.get_value()
		try:
			CP.get_info(cls)
			Drawers[form](CP.get_topn(10)).draw()
		except Exception as err:
			pass

	return inner_func


top = tk.Tk()
clss = ClsChooser(top)
forms = FormChooser(top)
btn = tk.Button(top, text="查询", command=gen_btn_action(clss, forms))

clss.grid(sticky='w')
forms.grid(sticky='w')
btn.grid()

top.title("新闻热词分析")
top.resizable(False, False)
top.protocol('WM_DELETE_WINDOW', lambda: top.destroy())
top.mainloop()
