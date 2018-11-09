# 概述

爬取the hacker news的所有文章内容，进行分词预处理，并且存入mongodb中

# 网址分析

网站首页：https://thehackernews.com/ 

## 翻页操作

网页页面中不显示页码数，其网址也不是以页码来命名：

>![翻页部分](https://github.com/leslie-lss/the-hacker-news/blob/master/image.png)

>https://thehackernews.com/search?updated-max=2018-10-29T21:18:00-11:00&max-results=10

>https://thehackernews.com/search?updated-max=2018-10-19T02:12:00-11:00&max-results=10&start=10&by-date=false

>https://thehackernews.com/search?updated-max=2018-10-12T01:11:00-11:00&max-results=10&start=20&by-date=false

是以页面中文章的时间来命名，只能一页页翻，不确定有多少

页面源码中，next page的元素处存在下一页的href，所以只需定位到该页面元素，即可提取到下一页的地址

## 文章网址

>https://thehackernews.com/2018/11/woocommerce-wordpress-hacking.html

网址中包含年份月份以及文章标题，不存在id号之类的唯一标识符，但是可以从文章列表的源码中直接提取到文章的href

# 数据存储结构

>key | 意义
>-------- | --------
>url | 文章的地址
>article | 文章正文内容
>article_no_url | 过滤掉正文中的链接
>article_chi | 文章中的中文字符
>article_chi_final | 文章中的中文字符的分词结果
>article_eng | 文章中的英文字符
>article_eng_final | 文章中的英文字符的分词结果
