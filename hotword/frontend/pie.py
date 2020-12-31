import matplotlib.pyplot as plt


class PieDrawer:
    """
    用来绘制根据热词绘制饼图
    """
    def __init__(self, results):
        self._results = results
        self._x = []
        self._y = []
        for x, y in results:
            self._x.append(x)
            self._y.append(y)

    def draw(self):
        expl = [0.1] + [0 for i in range(len(self._x)-1)]
        plt.pie(
            explode=expl,
            labels=self._x, x=self._y,
            autopct='%1.1f%%', pctdistance=0.8
        )
        plt.show()
