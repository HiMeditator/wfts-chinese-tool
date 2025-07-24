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

### `prompt`

内容为系统提示词。

设置系统提示词（System Prompt）。

### `listen`

内容为空。

监听系统音频输出。

### `answer`

内容为空。

让 Python 端基于监听到的音频进行回答，然后将回答的内容转换为音频备用。

### `output`

内容为空。

将 Python 端转换的音频输出到虚拟麦克风设备：CABLE Input (VB-Audio Virtual Cable)。

### `stop`

内容为空。

停止 Python 端服务。
