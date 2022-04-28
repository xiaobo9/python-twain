import logging
import time
import tkinter as tk

import tk_geometry
import twain


class MyTwain():
    """
    通过 gui 测试扫描功能的行为。
    """

    def __init__(self):
        self.root = None
        self.logger = logging.getLogger('MyTwain')

    def show(self):
        root = self.root
        if not root:
            self.logger.info('show gui')
            root = tk.Tk()
            self.root = root
            root.title('扫描工具')
            root.iconbitmap('scanner/resources/favicon.ico')
            # 窗口的关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self.close)

            tk_geometry.geometry(self.root)
            scan_btn = tk.Button(self.root, text="scan",
                                 bg="lightblue", width=10, command=self.scan)
            scan_btn.pack()
            self.root.mainloop()
            return

        self.logger.info('窗口已经打开了, 显示到最前')
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        return

    def close(self):
        if self.root:
            _root = self.root
            self.logger.info('close gui')
            self.root = None
            _root.destroy()

    def start_scan(self):
        self.show()

    def scan(self):
        # 绑定到父窗口 64位的dll
        dsm_name = 'extras/TWAINDSM_64.dll'
        # dsm_name = None
        sm = twain.SourceManager(
            self.root.winfo_id(),
            Language=twain.TWLG_CHINESE_SIMPLIFIED,
            Country=twain.TWCY_CHINA,
            MajorNum=2,
            MinorNum=1,
            ProductName="twain scanner",
            dsm_name=dsm_name,
            # SupportedGroups=twain.DG_IMAGE | twain.DG_CONTROL | twain.DG_AUDIO,
            SupportedGroups=twain.DG_IMAGE | twain.DG_CONTROL,
        )

        # 可以指定 source name 直接打开
        self.logger.info('before open_source')
        ss = sm.open_source(product_name=None)
        self.logger.info('after open_source')
        if not ss:
            self.logger('没有选择扫描仪')
            return

        self.logger.info('before request_acquire')
        # ss.request_acquire(0, 0)
        ss.request_acquire(1, 1)
        self.logger.info('after request_acquire')
        # 连续扫描
        ss.set_capability(twain.CAP_XFERCOUNT, twain.TWTY_INT32, -1)
        # 等待扫描仪设置完成
        try:
            ss.modal_loop()

            self.do_scan(ss)
        except Exception:
            self.logger.warning('发生了什么', exc_info=True)

    def do_scan(self, ss):
        scan_count = 0
        rv_count = 1
        self.logger('count: %s', rv_count)
        while rv_count > 0:
            self.logger('while count: %s', {rv_count})
            try:
                rv = ss.xfer_image_natively()
                if rv:
                    scan_count = scan_count + 1
                    (handle, rv_count) = rv
                    self.logger('rv count: %s',{rv_count})
                    now = time.strftime(
                        '%Y%m%d%H%M%S', time.localtime(time.time()))
                    twain.dib_to_bm_file(handle, "temp/image" + now + ".bmp")
                else:
                    self.logger("报错了")
            except Exception:
                self.logger.warning('可能是取消了操作吧', exc_info=True)
                break

        self.logger.info('扫描了 “%d” 张图片', scan_count)

        # 扫描完了。关掉窗口
        self.close()
