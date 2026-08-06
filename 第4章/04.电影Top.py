import csv

import requests
from lxml import etree

from 第4章.model.Movie import Movie

BASE_URL = "https://www.themoviedb.org"
TOP_MOVIE_URL = "https://www.themoviedb.org/discover/movie/items"


def get_movie_url_list(page=1) -> list[str]:
    """
    获取电影详情地址列表
    :param page: 页码
    :return:电影详情地址列表
    """
    res = requests.post(TOP_MOVIE_URL, data={"page": page}, timeout=60,
                        headers={"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"})
    # print(res.text)
    tree = etree.HTML(res.text)
    # movie_name_list = tree.xpath("//div[@data-media-type='movie']/@data-name")
    # print(movie_name_list)
    movie_url_list = tree.xpath("//div[@id='media-list']/div/div/div/div/div/div/a/@href")
    print(movie_url_list)
    # movie_time_list = tree.xpath("//span[@class='release_date w-full font-light']/text()")
    # print(movie_time_list)

    print("\n\n")
    return movie_url_list


def get_movie_info(movie_url) -> Movie:
    """
    根据电影Url获取电影信息实体
    :param movie_url: 电影Url
    :return: 电影信息实体
    """
    movie = Movie(BASE_URL + movie_url)
    res = requests.get(BASE_URL + movie_url, timeout=60,
                       headers={"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"})
    tree = etree.HTML(res.text)
    movie.name = handle_strip_list(tree.xpath("//*[@id='original_header']/div[2]//h2/a/text()"))
    print(movie.name)
    movie.year = handle_strip_list(tree.xpath("//*[@id='original_header']/div[2]//h2/span/text()"))
    print(movie.year)
    movie.date = handle_strip_list(tree.xpath("//*[@id='original_header']//span[@class='release']/text()"))
    print(movie.date)
    movie.tags = handle_strip_list(tree.xpath("//*[@id='original_header']//span[@class='genres']/a/text()"))
    print(movie.tags)
    movie.time = handle_strip_list(tree.xpath("//*[@id='original_header']//span[@class='runtime']/text()"))
    print(movie.time)
    movie.score = handle_strip_list(
        tree.xpath("//*[@id='original_header']//div[@class='user_score_chart']/@data-percent"))
    print(movie.score)
    movie.language = handle_strip_list(
        tree.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()"))
    print(movie.language)
    # 所有的身份列表
    identity_list = tree.xpath("//*[@id='original_header']/div[2]/section/div[3]//li[@class='profile']")
    role_list = parse_identity_list(identity_list)
    movie.director = handle_strip_list(role_list["director"])
    print(movie.director)
    movie.author = handle_strip_list(role_list["writer"])
    print(movie.author)
    movie.slogan = handle_strip_list(tree.xpath("//*[@id='original_header']//h3[@class='tagline']/text()"))
    print(movie.slogan)
    movie.desc = handle_strip_list(tree.xpath("//*[@id='original_header']//div[@class='overview']/p/text()"))
    print(movie.desc)
    print("\n\n")
    return movie


def parse_identity_list(identity_list) -> dict[str, list]:
    """
    根据身份信息解析需要的身份
    :param identity_list: 身份信息
    :return: 导演, 作者
    """
    role_dict = {"director": [], "writer": []}
    for identity in identity_list:
        name = identity.xpath("./p/a/text()")
        role_text = identity.xpath('./p[@class="character"]/text()')

        # 空值保护，没有名字/角色直接跳过
        if not name or not role_text:
            continue

        name = name[0]
        raw_role = role_text[0]
        # 按逗号切割，去除每个角色前后空格
        role_list = [r.strip() for r in raw_role.split(",")]

        # 判断：是 Director 或者 Writer
        if "Director" in role_list:
            role_dict["director"].append(name)
        if "Writer" in role_list:
            role_dict["writer"].append(name)
    print(role_dict)
    return role_dict


def handle_strip_list(parse_list) -> str:
    """
    处理解析后的数据
    :param parse_list: 解析的数据
    :return: 处理后的数据
    """
    if parse_list:
        return ",".join(parse_list).strip()
    else:
        return ""


def save_csv(movie_list):
    """
    将电影数据存储到csv
    :param movie_list: 电影数据
    :return:
    """
    with open("./movies.csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=["电影名", "链接", "上映时间", "类型", "时长", "评分", "语言", "导演",
                                                   "作者",
                                                   "slogan", "简介"])
        csv_writer.writeheader()
        for movie in movie_list:
            csv_writer.writerow({"电影名": movie.name,
                                 "链接": movie.url,
                                 "上映时间": movie.date,
                                 "类型": movie.tags,
                                 "时长": movie.time,
                                 "评分": movie.score,
                                 "语言": movie.language,
                                 "导演": movie.director,
                                 "作者": movie.author,
                                 "slogan": movie.slogan,
                                 "简介": movie.desc})


if __name__ == '__main__':
    movies = []
    for i in range(1, 6):
        movie_urls = get_movie_url_list(i)
        for url in movie_urls:
            movies.append(get_movie_info(url))
    save_csv(movies)
