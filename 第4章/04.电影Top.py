import csv
import requests
from lxml import etree

BASE_URL = "https://www.themoviedb.org"
TOP_MOVIE_URL = "https://www.themoviedb.org/movie"


def parse_movie() -> list[dict]:
    """解析电影数据"""
    res = requests.get(TOP_MOVIE_URL, timeout=60,
                       headers={"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"})
    # print(res.text)
    tree = etree.HTML(res.text)
    movie_name_list = tree.xpath("//div[@data-media-type='movie']/@data-name")
    print(movie_name_list)
    movie_url_list = tree.xpath("//div[@id='media-list']/div/div/div/div/div/div/a/@href")
    print(movie_url_list)
    movie_time_list = tree.xpath("//span[@class='release_date w-full font-light']/text()")
    print(movie_time_list)

    print("\n\n\n")
    movie_list = []
    for i in range(0, len(movie_name_list)):
        movie = {"name": movie_name_list[i], "url": f"{BASE_URL}{movie_url_list[i]}", "time": movie_time_list[i]}
        print(movie)
        movie_list.append(movie)
    print(movie_list)
    return movie_list


def save_csv(movie_list):
    """
    将电影数据存储到csv
    :param movie_list: 电影数据
    :return:
    """
    with open("./movies.csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=["名称", "链接", "上映时间"])
        csv_writer.writeheader()
        for movie in movie_list:
            csv_writer.writerow({"名称": movie['name'], "链接": movie['url'], "上映时间": movie['time']})


if __name__ == '__main__':
    movies = parse_movie()
    save_csv(movies)
