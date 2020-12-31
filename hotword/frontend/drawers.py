from matplotlib.pyplot import rcParams, title
from .bar import BarDrawer
from .pie import PieDrawer

rcParams['font.sans-serif']= ['Heiti TC']#防止中文乱码
rcParams['axes.unicode_minus']=False #解决负号问题
title(f"新闻热词 Top{10}")

Drawers = {
    0: BarDrawer,
    1: PieDrawer
}