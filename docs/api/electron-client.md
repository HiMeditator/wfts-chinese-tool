# electron client

## 说明

本项目的 Electron 主进程通过 WebSocket 向 Python 进程发送数据。

发送的数据内容一定为单行字符串。且每行字符串均可以解释为一个 JSON 对象。

对象参数如下：

```js
{
  command: string,
  content: string
}
```

## `command` 参数约定

当 JSON 对象的 `command` 参数为下列值时，表示的对应的含义。

### `stop`

`content`: 空

停止 Python 端服务。

### `print`

`content`: string

让 Python 端打印对应内容。
