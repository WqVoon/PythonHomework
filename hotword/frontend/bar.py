import matplotlib.pyplot as plt


class BarDrawer:
	"""
	用来绘制根据热词绘制直方图
	"""
	def __init__(self, results):
		self._results = results
		self._x = []
		self._y = []
		for x, y in results:
			self._x.append(x)
			self._y.append(y)

	def draw(self):
		plt.xlabel("类别信息")
		plt.ylabel("出现次数")
		plt.bar(self._x, self._y, width=0.4, color="#87CEFA")
		for x, y in self._results:
			plt.text(
				x, y+0.05,
				'%.0f' % y,
				ha='center', va='bottom'
			)
		plt.show()
