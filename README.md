# python-twain

python-twain,python,twain

一边学 python, 一边学 twain，完成许久之前想做的一个小工具

桌面应用启动后，额外启动 web 服务监听一个端口，响应扫描请求事件，把扫描结果按照 js ajax 请求上传到后台服务器

<localhost.ptlogin2.qq.com> qq 页面获取当前桌面登录的 qq 用户信息

## 流程

要做状态处理

### 桌面应用

- 线程/进程 启动本地服务 监听端口
- 系统托盘启动

### 页面流程

#### js 只做流程控制

事件驱动？ ajax 发送启动扫描仪的请求。 然后开启获取材料，直到结果数量为0

- init scan 本地扫描服务上传到后台服务 服务地址，认证信息等等，白名单？
    - ajax 请求，应用 twain source manager，选择要使用的 扫描仪器
    - single scan over 一张图片扫描完的事件
    - single upload over 上传后台服务器完成的事件
    - scan task all over 全部上传完成的事件
- do scan 开始扫描

#### js 获取扫描的文件，自己上传

## 环境配置

命令都是在 git bash 环境下执行的

### venv

```bash
# windows  自带的 twain_32.dll 需要 32位的程序调用，用 32 位的 python
python -m venv venv
source venv/Scripts/activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### requirements

``bash
pip freeze >requirements.txt
``

### 打包

```bash
#python setup.py install
python package.py
```

## twain

### twain 文档

windows 自带的 twain dll `C:\Windows\twain_32.dll`

`twain org` <https://twain.org/>

`twain-dsm` <https://github.com/twain/twain-dsm>

`pytwain` <https://pytwain.readthedocs.io/en/latest/>

`tawin.py` <https://pytwain.readthedocs.io/en/latest/_modules/twain.html>

source manager

```json
{
  "Id": 1,
  "Version": {
    "MajorNum": 2,
    "MinorNum": 1,
    "Language": 41,
    "Country": 86,
    "Info": ""
  },
  "ProtocolMajor": 2,
  "ProtocolMinor": 1,
  "SupportedGroups": 805306371,
  "Manufacturer": "Kevin Gill",
  "ProductFamily": "TWAIN Python Interface",
  "ProductName": "twain scanner",
  "MajorNum": 2,
  "MinorNum": 1,
  "Language": 41,
  "Country": 86,
  "Info": ""
}
```

source list

```
['TWAIN2 FreeImage Software Scanner']
```

source

```
ss = sm.open_source()
ss_id = ss.identity
print(ss.name, ss_id.get('Id'), ss.is_twain2())
```

`twain whl` <https://www.lfd.uci.edu/~gohlke/pythonlibs/#twainmodule>

```bash
# windows 自带的是32位的dll  twain_32.dll, 直接用这个就得安装32位的python 进行开发
py -m pip install dll/twain-1.0.4-cp39-cp39-win32.whl
```
