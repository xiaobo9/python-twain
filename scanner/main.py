import logging
import sys
import threading
import webbrowser
from http.server import HTTPServer

import win_sys_tray as tray
from my_server import MyRequest
from main_gui import MyTwain

"""
启动 监听客户端js请求的服务，以便响应扫描请求；
通过 gui 测试扫描功能的行为。
"""
if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s [%(name)s] %(levelname)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger('main')

    app = MyTwain()
    MyRequest.set_app(app)

    PORT = 8000
    server = HTTPServer(("127.0.0.1", PORT), MyRequest)

    def run_server():
        print(f"Serving at port {PORT}")
        server.serve_forever()

    # 线程启动 http server
    thread = threading.Thread(target=run_server)
    thread.start()

    def scan(sys_tray):
        # 启动窗口，改成启动系统托盘
        app.show()

    def bye(sys_tray):
        MyRequest.set_app(None)
        logger.info('web server shutdowning')
        server.shutdown()
        server.server_close()
        logger.info('app closing')
        app.close()
        logger.info('sys exit 0')
        sys.exit(0)

    def open_browser(sys_tray):
        webbrowser.open('http://127.0.0.1:8000')

    favicon = 'scanner/resources/favicon.ico'
    options = (('扫描', 'scan.ico', scan),
               ('打开页面', 'browser.ico', open_browser),
               )

    tray.SysTray(favicon, '扫描工具，双击显示窗口，右键显示菜单', options, on_quit=bye)
