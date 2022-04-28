import logging
import os.path

import win32api
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

class SysTray(object):
    """
    系统托盘
    """
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self, icon, hover_text, menu_options: tuple, on_quit=None, default_menu_index=None,
                 window_class_name=None):
        self.logger = logging.getLogger('SysTray')
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('退出', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or 'SysTrayIconPy'

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify,
                       }

        wnd_class = win32gui.WNDCLASS()
        wnd_class.hInstance = win32gui.GetModuleHandle(None)
        h_inst = wnd_class.hInstance
        wnd_class.lpszClassName = self.window_class_name
        wnd_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wnd_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wnd_class.hbrBackground = win32con.COLOR_WINDOW
        wnd_class.lpfnWndProc = message_map

        class_atom = win32gui.RegisterClass(wnd_class)

        self.hwnd = win32gui.CreateWindow(class_atom,
                                          self.window_class_name,
                                          win32con.WS_OVERLAPPED | win32con.WS_SYSMENU,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          None,
                                          None,
                                          h_inst,
                                          None
                                          )

        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()
        win32gui.PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            self.logger.debug(menu_option)
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((
                    option_text,
                    option_icon,
                    self._add_ids_to_menu_options(option_action),
                    self._next_action_id
                ))
            else:
                self.logger.warning('Unknown item, text:[%s], icon:[%s], action:[%s]', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags
                                       )
        else:
            self.logger.info("Can't find icon file '%s' using default.", self.icon)
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          hicon,
                          self.hover_text
                          )
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit:
            self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        elif lparam == win32con.WM_MOUSEMOVE:
            pass
        else:
            # self.logger.info('lparam: %s', lparam)
            pass
        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None
                                )
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        icon_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        icon_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        if os.path.isfile(icon):
            hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, icon_x, icon_y, win32con.LR_LOADFROMFILE)
        else:
            self.logger.info("Can't find icon file '%s' using default.", icon)
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        hdc_bitmap = win32gui.CreateCompatibleDC(0)
        hdc_screen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdc_screen, icon_x, icon_y)
        hdm_old = win32gui.SelectObject(hdc_bitmap, hbm)

        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdc_bitmap, (0, 0, 16, 16), brush)

        win32gui.DrawIconEx(hdc_bitmap, 0, 0, hicon, icon_x, icon_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdc_bitmap, hdm_old)
        win32gui.DeleteDC(hdc_bitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        action_id = win32gui.LOWORD(wparam)
        self.execute_menu_option(action_id)

    def execute_menu_option(self, action_id):
        menu_action = self.menu_actions_by_id[action_id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)


def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)


# https://blog.csdn.net/dyx1024/article/details/7430638
# http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html
if __name__ == '__main__':
    def bye(sys_tray_icon):
        print('退出')


    def hello(sys_tray_icon):
        print('hello')


    def world(sys_tray_icon):
        print('退出')


    favicon = 'favicon.ico'
    options = (('hello', favicon, hello),
               ('world', favicon, world)
               )

    SysTray(favicon, 'SysTray', options, on_quit=bye)
