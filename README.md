# pyqbot

基于酷Q HTTP API插件的脚手架项目。可用于使用python快速开发自己需要的QQ机器人插件功能。

## Features

目前仅支持聊天消息的事件响应：

* 支持群/私聊消息
* 支持只处理私聊/群消息，以及处理特定群的聊天消息
* 支持信息匹配处理器，关键词的完整匹配、消息开头匹配、正则匹配
* 支持设置多个默认处理器，用以处理无命令匹配情况的闲聊

支持的功能：

* 可设置命令CD时间
* 可以设置是否at发送人
* 保存运行期间群消息记录，每群最多200条，，可按发言人查询或任意查询
* python-aiocqhttp支持的其它酷Q HTTP API调用

## To Do

* 定时任务的设置
* notice和request的处理（因为我用不到，优先度很低）

## Usage

bot.py, internal.py为框架核心文件，不建议修改。

config.py存储了QQ机器人的配置。
其中bot_commands为匹配处理器，default_proc为无匹配时的处理器。
添加格式参见注释。

## Example

customreply.py实现了两个小功能。

一个使用正则匹配触发，在有人问“有人XXX吗”的时候以一定概率回复“没有，guna”。

一个无匹配触发，以90%的概率跟从复读，或以2%的概率复读上一个人。

## Acknowledgements
[richardchien/python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp)
酷Q HTTP API的Python SDK

[Raka-loah/qqbot-plugin-warframe](https://github.com/Raka-loah/qqbot-plugin-warframe)
借用了大量的基础处理逻辑