# python stdout

本文档主要记录本项目 Python 进程标准输出内容的约定。

## 说明

本项目的 Python 进程通过标准输出向 Electron 主进程发送数据。

Python 进程标准输出 (`sys.stdout`) 的内容一定为一行一行的字符串。且每行字符串均可以解释为一个 JSON 对象。

对象参数如下：

```js
{
  command: string,
  content: string
}
```

## `command` 参数约定

当 JSON 对象的 `command` 参数为下列值时，表示的对应的含义。

### `ready`

`conetnt`: 空

表示 Python 端已就绪，node.js 端可以开始建立 WebSocket 连接了。

### `print`

`content`: string

输出 Python 端打印的内容。
