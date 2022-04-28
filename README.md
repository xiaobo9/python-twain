# python-twain

python-twain,python,twain

桌面应用启动后，额外启动 web 服务监听一个端口，响应扫描请求事件，把扫描结果按照 ajax 请求上传到后台服务器

最初的实现灵感来自于 qq 的浏览器页面快速登陆功能

qq 客户端程序本地监听某端口，腾讯将子域名 `localhost.ptlogin2.qq.com` 绑定到 `127.0.0.1` 进而解决跨域访问的问题。

浏览器上 qq 快速登陆页面通过 ajax 访问上述监听服务，获取当前桌面登录的 qq 用户认证信息进行快速登陆。

## 本程序功能流程

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

## 开发环境配置，打包

```bash
# 配置虚拟环境 venv
python -m venv venv
source venv/Scripts/activate

# 安装依赖
pip install -r requirements.txt

# requirements
pip freeze >requirements.txt

# 打包
#python setup.py install
python package.py
```
