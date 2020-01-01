# Build20141007
# coding=utf-8

import winreg
import sys
import subprocess
import json
import os
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


def read_setting():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        "Software\Microsoft\Windows\CurrentVersion\Internet Settings") as handle:
        server_and_port = winreg.QueryValueEx(handle, "ProxyServer")[0]
        current_proxy_server = server_and_port[:server_and_port.find(':')]
        current_proxy_port = server_and_port[server_and_port.find(':') + 1:]
        proxy_server_status = winreg.QueryValueEx(handle, "ProxyEnable")
    return (current_proxy_server, current_proxy_port, proxy_server_status[0])


def set_proxy(addr, port, bit):
    with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                          reserved=0, access=winreg.KEY_SET_VALUE) as handle:
        if len(addr):
            winreg.SetValueEx(handle, 'ProxyServer', 0, 1, addr + ':' + port)
        winreg.SetValueEx(handle, 'ProxyEnable', 0, 4, bit)
    proxy_addr.set(read_setting()[0] + ':' + read_setting()[1])
    proxy_bit.set(proxy_enable_status[read_setting()[2]])


def read_file(target):
    if not (cfg_file_name in os.listdir()):
        messagebox.showinfo(message='找不到配置文件，使用默认配置', icon="warning")
        set_proxy('172.16.217.240', '3128', 1)
        with open(cfg_file_name, 'w') as file_handle:
            default_proxy = {"1": ["Proxy 1", "172.16.217.240", "3128", 1], "2": ["No proxy", "", "", 0]}
            json.dump(default_proxy, file_handle)
        return default_proxy
    else:
        with open(target, 'r') as file_handle:
            file_handle.seek(0)
            config_str = json.load(file_handle)
        return config_str


def show_menu():
    config_str = read_file(cfg_file_name)
    menu_entry = sorted(config_str.keys())
    for i in menu_entry:
        ttk.Button(lframe2, text=config_str[i][0],
                   command=lambda i1=i: (set_proxy(config_str[i1][1], config_str[i1][2], config_str[i1][3])),
                   style="TButton").grid(row=int(i))
    return


def center(win):
    print('called')
    print(win.geometry())
    win.update_idletasks()
    width = win.winfo_width()
    print(width)
    frm_width = win.winfo_rootx() - win.winfo_x()
    print('frm_width:' + str(frm_width))
    win_width = width + 2 * frm_width
    height = win.winfo_height() + 20
    print('height:' + str(height))
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    print('win_height:' + str(win_height))
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    if win.attributes('-alpha') == 0:
        win.attributes('-alpha', 1.0)
    print('geo', win.geometry())
    win.deiconify()


def ie_exit():
    subprocess.Popen(r'c:\\Program Files\\Internet Explorer\\iexplore.exe')
    sys.exit()


cfg_file_name = 'config.txt'
proxy_enable_status = ('禁用', '启用')

root = Tk()
# root.resizable(0,0)
root.title("代理服务器设置助手 3.4")

ttk.Style().configure("TButton", padding=3, relief="flat", font=12)
appHighlightFont = font.Font(size=14, weight='bold')
appFont = font.Font(size=12)

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(E, W))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

str_warning = "请先关闭Internet Explorer！"
str_addr_port = "状态  IP地址:端口"
str_status = "启用状态："

ttk.Label(mainframe, text=str_warning, foreground='red', font=appHighlightFont).grid(column=0, row=0, columnspan=2)

frame1 = ttk.Frame(mainframe, padding="3 3 3 3")
frame1.grid(column=0, row=1, sticky=(E, W))
frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)

frame2 = ttk.Frame(mainframe, padding="3 3 3 3")
frame2.grid(column=1, row=3)
frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)

lframe1_id = ttk.Label(text='当前设置', font=appFont)
lframe1 = ttk.Labelframe(mainframe, labelwidget=lframe1_id, padding="3 3 3 3", labelanchor='n')
lframe1.grid(column=0, row=2, columnspan=2, sticky=E + W)

lframe2_id = ttk.Label(text='可用设置', font=appFont)
lframe2 = ttk.Labelframe(mainframe, labelwidget=lframe2_id, padding="3 3 3 3", labelanchor='n')
lframe2.grid(row=3, columnspan=2)

# button_ck=ttk.Checkbutton(lframe1, text="启用")
# button_ck.grid(column=1, row=4)

proxy_addr = StringVar()
proxy_bit = StringVar()
ttk.Label(lframe1, text=str_addr_port, font=appFont).grid(column=0, row=2, columnspan=2, sticky=(W))

proxy_bit_entry = ttk.Label(lframe1, width=5, textvariable=proxy_bit, font=appFont)
proxy_bit_entry.grid(column=0, row=3, sticky=(E))
proxy_bit.set(proxy_enable_status[read_setting()[2]])

proxy_addr_entry = ttk.Entry(lframe1, width=22, textvariable=proxy_addr, font=appFont)
proxy_addr_entry.grid(column=1, row=3, sticky=(W))
proxy_addr.set(read_setting()[0] + ':' + read_setting()[1])

# button_read_file=ttk.Button(frame1, text="读配置文件", style="TButton", command = lambda:show_menu())
# button_read_file.grid(column=0, row=1, sticky=(W))

button_exit = ttk.Button(mainframe, text="退出", style="TButton", command=lambda: sys.exit())
button_exit.grid(column=0, row=4, sticky=(W))

button_ie = ttk.Button(mainframe, text="启动IE_退出", style="TButton", command=lambda: ie_exit())
button_ie.grid(column=1, row=4)

for child in mainframe.winfo_children(): child.grid_configure(padx=2, pady=1)
# for child in lframe1.winfo_children(): child.grid_configure(padx = 2, pady = 1)
# for child in lframe2.winfo_children(): child.grid_configure(padx = 2, pady = 1)

# center(root)
show_menu()
root.mainloop()
