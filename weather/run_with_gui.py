import tkinter as tk
from frontend.ui import QueryController, InfoDisplayer

top = tk.Tk()
top.title('实况天气查询')
top.resizable(False, False)

info_displayer = InfoDisplayer(top)
querycontroller = QueryController(top, info_displayer)

querycontroller.grid()
info_displayer.grid()

top.mainloop()