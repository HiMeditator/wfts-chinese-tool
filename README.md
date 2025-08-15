<div align="center" >
    <img src="./build/icon.png" width="100px" height="100px"/>
    <h1 align="center">wfts-chinese-tool</h1>
    <p>wfts-chinese-tool 为中文玩家准备的一个工具软件。用户可以通过该软件获取对话的中文翻译，用户还可以将中文语音转换为英语并输入到游戏中。</p>
</div>

![](./assets/main.png)

## ✨ 软件特性

获取对话和翻译：软件能捕获系统音频输出，并调用云端语音识别模型生成音频对应文字内容和中文翻译。


英语音频合成：用户可以在该软件中通过中文进行语音输入，软件调用云端模型翻译为英语，并合成英语内容的音频。

英语音频输出：软件可以将合成的音频输出到虚拟音频设备中，游戏可以根据虚拟设备获取该音频。

## 软件下载

[GitHub Releases](https://github.com/HiMeditator/wfts-chinese-tool/releases)

## 📖 基本使用

该项目仅支持 Windows 系统。

本项目使用了阿里云的云端模型（语音识别模型、语音合成模型）。要使用这些模型首先需要获取阿里云百炼平台的 API KEY，然后将 API KEY 添加到软件设置中或者配置到环境变量中。相关教程：

- [获取 API KEY](https://help.aliyun.com/zh/model-studio/get-api-key)
- [将 API Key 配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)

**如果没有将阿里云的 API KEY 配置到环境变量，该项目将无法正常工作！**

除此之外，还需要安装 [VB Cable](https://vb-audio.com/Cable/) 虚拟音频设备软件。软件将使用该音频设备将合成的英语音频注入到游戏的虚拟麦克风中。

完成上述操作后建议重启计算机以使得操作生效。

之后每次启动游戏时，打开系统的“音量合成器”选项，首先设置游戏的输入设备为默认，待游戏启动后再改为 CABLE Output。

<img src="./assets/mixer.png" style="zoom:40%;" />

## 🚀 运行项目

克隆仓库：

```bash
# HTTPS
git clone https://github.com/HiMeditator/wfts-chinese-tool.git
# SSH
git clone git@github.com:HiMeditator/wfts-chinese-tool.git
```

安装依赖：

```bash
npm install
```

构建 python 运行环境：

```bash
cd chat
# 在 /chat 目录
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

打包 Python 程序：

```bash
# 在 /chat 目录，激活 Python 虚拟环境运行
pyinstaller main.spec
```

运行项目：

```bash
npm run dev
```

构建项目：

```bash
npm run build:win
```
