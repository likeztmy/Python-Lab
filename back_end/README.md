# 安装依赖
`pip install -r requirements`

# 运行
`python service.py`

# 目录

`danmaku.py---弹幕爬取相关函数`

`my_pb2.py---存放与弹幕数据相关的rpc通信协议`

`search.py---视频信息搜索相关函数`

`service.py---后端接口函数文件`

`sql.py---数据库操作文件`

`user.py---用户信息相关函数`

`video.py---视频信息相关函数`

#  功能说明

### 弹幕解析

目前弹幕解析功能仅支持解析b站填充到视频中的弹幕，也就是说一些未填充到视频里的弹幕还没有办法爬取并解析。并且解析填充到视频里的弹幕也存在着不稳定的情况。

### 弹幕爬取

同上，目前可爬取的弹幕内容仅限于b站填充到视频里的弹幕数据。比如说有的视频可能存在着几万甚至十几万的弹幕数据，但最终填充到视频里的弹幕数据最多可能只有两三万那么多，甚至可能只有六七千那么多。所以目前项目还存在着一定的局限性。等期末周结束之后可能会进行一个优化。

### 词云图绘制

由于还未购买服务器及数据库，所以目前该项目的构建运行仍然是在本地环境。而这里的词云图绘制功能用到的数据库其实是我的本地数据库，故该功能还不能正式投入使用，只能在本地运行使用。
