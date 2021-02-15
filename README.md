<p align="center"><img src="https://ae01.alicdn.com/kf/U150c6f229b47468781c941fdd80545eak.png" width="200"></p>
<h3 align="center">- Anime API -</h3>

<p align="center">

<img src="https://img.shields.io/github/v/release/zaxtyson/Anime-API.svg?logo=bilibili" />
<img src='https://readthedocs.org/projects/anime-api/badge/?version=latest' alt='Documentation Status' />

</p>


## 简介

Anime-API 是一个异步的资源解析框架, 用于组织各类爬虫抓取互联网上的资源, 为前端提供格式统一的接口服务

因为前期以动漫、弹幕抓取为主, 所以叫 Anime-API, 但是后面会加入漫画、小说、音乐等抓取功能~


## API 文档

[点我点我](https://anime-api.readthedocs.io/zh_CN/latest/#)

## 更新日志

### `v1.3.1`

- 过滤了 k1080 部分无效视
- 使用续命大法修复部分源播放途中直链失效的问题

### `v1.3.0`

- API 完全改用异步框架重构, 效率大幅提升, 支持服务器端部署
- 修复了几个番剧模块出现的问题, 与源网站同步更新
- 修复了弹幕库的一些问题, 结果更多更准, 过滤了弹幕中无关的内容
- 修复了直链有效期太短导致视频播到一半失败的问题

### `v1.1.8`

- 新增引擎 k1080p
- 修复 youku 某些弹幕解析失败的问题
- 修复 bilibili 用户上传视频弹幕解析失败的问题
- 修复 bahamut 网站更新导致弹幕抓取失败的问题
- 搜索结果异步加载
- 历史记录功能增强, 自动解析上次访问页面

### `v0.7.1`

- 修复 agefans 视频解析异常的问题
- 修复 bimibimi 部分视频解析失败的问题

### `v0.7.0`

- 修复 bimibimi 部分视频解析失败的问题和弹幕 undefined 的问题
- 补充 bilibili 影视区弹幕
- 新增引擎 meijuxia
- 新增弹幕源 youku
- 新增弹幕源 tencent
- 增加新番更新表接口