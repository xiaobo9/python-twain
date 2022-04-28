def geometry(window, width=500, height=300):
    # 得到屏幕宽度
    sw = window.winfo_screenwidth()
    # 得到屏幕高度
    sh = window.winfo_screenheight()
    # 窗口宽高为100
    ww = width
    wh = height
    window.geometry("%dx%d+%d+%d" % (ww, wh, (sw - ww) / 2, (sh - wh) / 2))
