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

## `v1.4.3`

- 新增视频引擎 `4K鸭奈菲(4Kya)`
- 新增视频引擎 `Lib在线(libvio)`  
- 新增视频引擎 `阿房影视(afang)`  
- 修复视频引擎 `AgeFans` 域名映射异常的问题
- 修复视频引擎 `ZzzFun` 部分视频无法播放的问题
- 修复视频引擎 `bimibimi` 无法搜索和播放的问题
- 修复视频引擎 `K1080` 部分视频无法播放的问题
- 弃用视频引擎 `Meijuxia`, 质量太差
- 弃用视频引擎 `bde4`

### `v1.4.2`

- 修复视频引擎 `K1080` 失效的问题

### `v1.4.1`

- 修复视频引擎 `ZzzFun` 资源迁移导致无法使用的问题
- 修复视频引擎 `K1080` 部分视频无法播放的问题
- 修复视频引擎 `樱花动漫(yhdm)` 域名变更的问题
- 视频视频引擎 `哔嘀影视(bde4)` 切换备用域名
- 过滤视频引擎 `AgeFans` 部分无效视频源
- 过滤弹幕引擎 `爱奇艺(iqiyi)` 和 `腾讯视频(tencent)` 无关搜索结果   
- 修复弹幕引擎  `哔哩哔哩(bilibili)` 部分番剧弹幕抓取失败的问题[#12](https://github.com/zaxtyson/AnimeSearcher/issues/12)
- 移除失效视频源 `eyunzhu` 和弹幕源 `哔咪哔咪(bimibimi)`

### `v1.4.0`

- 支持 HLS 格式视频流量代理, 支持混淆流量解码
- 对经常被墙的网站做了 A 记录, 防止域名失效, 加快 DNS 解析速度
- 新增视频搜索引擎 `哔嘀影视(bde4)`
- 新增弹幕搜索引擎 `爱奇艺(iqiyi)`
- 修复引擎 `k1080`, `meijuxia`, 与官方保存同步
- 修复 `优酷(youku)` 弹幕搜索无结果的问题
- 修复 `哔哩哔哩(bilibili)` 120分钟之后无弹幕的问题[#9](https://github.com/zaxtyson/AnimeSearcher/issues/9)
- 修复 `ZZZFun` 播放路线1

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