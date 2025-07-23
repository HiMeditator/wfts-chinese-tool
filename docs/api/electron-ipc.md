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

### `server.stop`

**介绍：** 停止 Python 后端服务

**数据类型：** 无数据

## 后端 ==> 前端
