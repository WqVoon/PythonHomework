from backend.cp import ContentProvider as CP
from utils import Loger, SUPPORTED_KEYS
from frontend.drawers import Drawers

Loger.is_debug_mode = True

cls_idx = int(input(
	"请输入新闻类别:\n " +
	" ".join([
		f"{idx}: {SUPPORTED_KEYS[idx]}"
		for idx in range(len(SUPPORTED_KEYS))
	]) +
	"\n> "
))
form_idx = int(input(
    "展示形式:\n"+
    " 0: 直方图 1: 饼图\n"+
    "> "
))


CP.get_info(SUPPORTED_KEYS[cls_idx])
Drawers[form_idx](CP.get_topn(10)).draw()
