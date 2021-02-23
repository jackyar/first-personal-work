# first-personal-work
Process video comment information to generate word cloud map

**部署环境：** tomcat 8.5(列表中所有文件均在同一个web工程文件目录下)

* 爬取腾讯视频《在一起》的评论信息 ----- 数据采集
* 使用python的第三方库jieba分词处理评论信息，并保存到comments.js文件 ----- 数据处理
* 生成词云图展示数据 ----- 数据可视化

