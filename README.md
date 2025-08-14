<div align="center" >
    <img src="./build/icon.png" width="100px" height="100px"/>
    <h1 align="center">wfts-ai-chat</h1>
    <p>wfts-ai-chat 是一个尝试使用云端模型来游玩 AI 游戏《Whispers from the Star》的项目。</p>
    <p>
        | <b>简体中文</b>
        | <a href="./README_en.md">English</a> |
    </p>
    <p><i>项目已经初步开发完成，发行版将在之后推出...</i></p>
</div>

![](./assets/main.png)

## 📖 基本使用

该项目仅支持 Windows 系统。本项目目前没有推出发行版，用户需要克隆仓库并自行搭建开发环境来运行项目。或者等待后续推出的发行版。

本项目使用了多个阿里云的云端模型（语音识别模型、大语言模型、语言合成模型）。要使用这些模型首先需要获取阿里云百炼平台的 API KEY，然后将 API KEY 添加到软件设置中或者配置到环境变量中。相关教程：

> 国际版的阿里云服务没有全部提供本项目使用的模型，因此目前非中国用户无法直接使用该项目。如果你是开发者，可以考虑修改项目中使用的模型（音频转文字模型、聊天模型、语言合成模型）

- [获取 API KEY](https://help.aliyun.com/zh/model-studio/get-api-key)
- [将 API Key 配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)

没有 API KEY 该项目将无法运行。

除此之外，运行该项目之前还需安装 [VB Cable](https://vb-audio.com/Cable/) 虚拟音频设备软件，用于将合成的回答音频注入到游戏的虚拟麦克风中。

每次启动游戏时，打开系统的“音量合成器”选项，首先设置游戏的输入设备为默认，待游戏启动后再改为 CABLE Output。

<img src="./assets/mixer.png" style="zoom:40%;" />

## 🚀 运行环境搭建

克隆仓库：

```bash
# HTTPS
git clone https://github.com/HiMeditator/wfts-ai-chat.git
# SSH
git clone git@github.com:HiMeditator/wfts-ai-chat.git
```

安装依赖：

```bash
npm install
```

构建 python 运行环境：

```bash
cd chat
# in ./chat folder
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

运行项目：

```bash
npm run dev
```

暂不支持构建项目。
