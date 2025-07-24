# electron ipc

本文档主要记录 Electron 主进程和渲染进程的通信约定。

## 前端 <=> 后端

## 前端 ==> 后端

### `server.start`

**介绍：** 启动 Python 后端服务

**数据类型：** 无数据

### `server.send`

**介绍：** 向 Python 后端服务发送数据

**数据类型：** `string`

### `server.listen`

**介绍：** 让 Python 后端服务监听系统音频输出

**数据类型：** `string`

### `server.convert`

**介绍：** 将 Python 后端服务监听的音频转换成文本

**数据类型：** `string`

### `server.stop`

**介绍：** 停止 Python 后端服务

**数据类型：** 无数据

### `window.pin`

**介绍：** 设置窗口是否顶置

**数据类型：** `boolean`

### `window.close`

**介绍：** 关闭窗口

**数据类型：** 无数据

## 后端 ==> 前端

### `info.send`

**介绍：** 向前端发送正常日志信息

**数据类型：** `string`

### `warn.send`

**介绍：** 向前端发送警告日志信息

**数据类型：** `string`

### `error.send`

**介绍：** 向前端发送错误日志信息

**数据类型：** `string`
