import tkinter as tk
from tkinter import messagebox
from backend.cp import ContentProvider


class QueryController(tk.Frame):
	"""
	用户输入天气并点击按钮进行查询的组件
	"""

	def __init__(self, master, displayer, row=0):
		tk.Frame.__init__(self)
		self._entry = tk.Entry(self)
		self._query = tk.Button(
			self, text="查询",
			command=QueryController.gen_btn_action(
				self._entry, displayer
			)
		)

		self._entry.grid(row=row, column=0)
		self._query.grid(row=row, column=1)

	@staticmethod
	def gen_btn_action(entry, displayer):
		cp = ContentProvider()

		def inner_func():
			city_name = entry.get() if entry.get() else "达州"
			cp.get_weather_info(city_name)
			if not cp.err:
				displayer.set_tip(cp.tip)
				displayer.set_img(cp.wea_img)
				displayer.set_info(cp.ret_info)
			else:
				messagebox.showerror('错误', cp.err)

		return inner_func


class InfoDisplayer(tk.Frame):
	"""
	显示天气相关信息的组件
	"""

	def __init__(self, master, row=1):
		tk.Frame.__init__(self)
		self._img_label = tk.Label(self)
		self._info_label = tk.Label(self)
		self._tip_label = tk.Label(self)

		self._img_label.grid(row=row)
		self._info_label.grid(row=row + 1)
		self._tip_label.grid(row=row + 2)

	def set_img(self, fn):
		img = tk.PhotoImage(file=f"img/{fn}")
		self._img_label.configure(image=img)
		self._img_label.image = img  # 迷之问题

	def set_info(self, info):
		self._info_label['text'] = info

	def set_tip(self, tip):
		self._tip_label['text'] = "小提示：" + tip
