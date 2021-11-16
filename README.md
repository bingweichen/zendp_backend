#  极简点评网
                    极简点评网：万物皆可评
                    
                    1. 前端项目地址 https://github.com/bingweichen/zendp_frontend
                    2. 后端项目地址 https://github.com/bingweichen/zendp_backend
                    3. 网站地址：www.zendp.cn


# overview
1. 内容介绍
2. 开发计划
3. 项目搭建
4. zendp_backend
5. Q&A


# 1. 内容介绍

## 缘由
魔都租房被坑，就思考如果有一个点评机制，就可以优化市场。国外就有类似的租房中介点评的网站。

## 项目内容
搭建一个网站，由用户创建评论主体和评论内容

本开源项目，欢迎大家提供自己的想法，后续获得的收益和流量，也都将公布在此处。

将会大家基础的评论框架，每个版块欢迎感兴趣的开发者认领负责。

## 版块
电影、音乐、游戏、租房中介、留学中介、旅游地点、导师、公司

## 技术
前端 react

后端 flask


## 关于捐赠

欢迎2元捐赠，捐赠将用于服务器运维和负责人奖励，所有金额都将公开。

# 2. 开发计划

## 进度
2021-10-28 创建项目


## 计划
2021-11-05 基础搭建上线

## 待办
- 用户注册
- 用户登录
- 匿名评论

- 富文本编辑器 (二选一)
BRAFT EDITOR
https://braft.margox.cn/demos/basic
react quill
https://github.com/zenoamaro/react-quill

- 评分系统
每日晚上12点计算评论的分数，更新到条目中
1. 加权平均
2. 时间系数（越近的越重要）

- 收藏功能
用户可以收藏条目

## V1待办
完成电影模块的创建条目，修改条目，发表评论，修改评论，删除评论
部署到网站




# 3. 项目搭建
1. 本地搭建 postgresql
2. `pip install -r requirements.txt`
3. 修改 `config_template.py` 中的配置, 并rename为`config.py`
4. 数据库配置
```
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```
5. 启动后端 `python manager.py runserver`
6. redis 
```
# 安装
docker pull redis:latest
# 启动
docker run -itd --name redis-t -p 6379:6379 redis
# 查看
docker ps
docker exec -it redis-t /bin/bash
redis-cli
keys *
```

# 4. zen_backend

# 5. Q&A
#### 无法启动redis
```shell
docker ps -a -q
找到container
docker rm 8cb8e
删除container

docker start 
```
