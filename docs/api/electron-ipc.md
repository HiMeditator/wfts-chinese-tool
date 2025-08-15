# electron ipc

本文档主要记录 Electron 主进程和渲染进程的通信约定。

## 前端 <=> 后端

## 前端 ==> 后端

### `server.start`

**介绍：** 启动 Python 后端服务

**数据类型：** 无数据

### `server.listen`

**介绍：** 让 Python 后端服务监听系统音频输出

**数据类型：** 无数据

### `server.record`

**介绍：** 让 Python 后端服务监听麦克风输入

**数据类型：** 无数据

### `server.break`

**介绍：** 让 Python 后端服务停止音频监听

**数据类型：** 无数据

### `server.translate`

**介绍：** 让 Python 后端服务将中文内容翻译成英语

**数据类型：**

```ts
{
  type: "remote" | "ollama",
  name: string,
  text: string
}
```

### `server.synthesis`

**介绍：** 让 Python 后端服务将文本合成为音频

**数据类型：** `string`

### `server.play`

**介绍：** 让 Python 后端服务播放和注入合成的音频

**数据类型：** 无数据

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

### `message.send`

**介绍：** 向前端发送信息，其中必定有 `command` 参数

**数据类型：** `any`
