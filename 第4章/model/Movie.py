from streamlit.elements import empty


class Movie:
    def __init__(self,
                 url,
                 name="",
                 date="",
                 tags=None,
                 time="",
                 score="",
                 language="",
                 director="",
                 author="",
                 slogan="",
                 desc=""):
        """
        电影实体
        :param url:  链接
        :param name: 名称
        :param date: 上映时间
        :param tags:  类型
        :param time: 时长
        :param score: 评分
        :param language: 语言
        :param director: 导演
        :param author: 作者
        :param slogan: 宣传语
        :param desc: 简介
        """
        if tags is None:
            tags = []
        self.url = url
        self.name = name
        self.date = date
        self.tags = tags
        self.time = time
        self.score = score
        self.language = language
        self.director = director
        self.author = author
        self.slogan = slogan
        self.desc = desc

    def __str__(self):
        return f"电影名：{self.name}, 链接：{self.url}, 上映时间：{self.date},类型：{self.tags},时长：{self.time},评分：{self.score},语言：{self.language},作者：{self.author},slogan:{self.slogan},简介：{self.desc}"
