import tkinter as tk
from utils import SUPPORTED_KEYS
from frontend.drawers import Drawers


class RadioButtonGroup(tk.Frame):
	"""
	一组单选框的组件
	"""

	def __init__(self, master, label, row, init_value, values):
		tk.Frame.__init__(self, master)
		var = self.__var = tk.StringVar(
			self, init_value
		)

		tk.Label(self, text=label).grid(row=row)

		idx = 1
		for cls in values:
			tk.Radiobutton(
				self,
				variable=var,
				value=cls, text=cls
			).grid(row=row, column=idx)
			idx += 1

	def get_value(self):
		return self.__var.get()


class ClsChooser(RadioButtonGroup):
	"""
	选择新闻类别的组件
	"""

	def __init__(self, master, row=0):
		RadioButtonGroup.__init__(
			self, master,
			"新闻类别:", row,
			SUPPORTED_KEYS[0], SUPPORTED_KEYS
		)


class FormChooser(RadioButtonGroup):
	"""
	选择展示方式的组件
	"""

	def __init__(self, master, row=1):
		keys = list(Drawers.keys())
		RadioButtonGroup.__init__(
			self, master,
			"展示方式:", row,
			keys[0], keys
		)
