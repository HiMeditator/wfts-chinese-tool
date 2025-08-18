# electron client

## 说明

本项目的 Electron 主进程通过 Socket 向 Python 进程发送数据。

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


### `listen`

内容为空。

监听系统音频输出。

### `record`

内容为空。

监听用户音频输入。

### `break`

内容为空。

停止音频监听。

### `translate`

`content: string` 为前端发送对象的 JSON 字符串

将内容使用对应的模型进行中文翻译。

### `synthesis`

`content: string`

将内容合成为音频。

### `output`

内容为空。

将 Python 端转换的音频同时输出到默认音频输出和虚拟麦克风设备：CABLE Input (VB-Audio Virtual Cable)。

### `stop`

内容为空。

停止 Python 端服务，退出。
