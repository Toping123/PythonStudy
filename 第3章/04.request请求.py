import requests
from requests import Response

def request(url) -> Response:
    """
    请求
    :param url: 请求地址url
    :return: 请求结果
    """
    res = requests.get(url)
    print(f"请求结果：{res.text}")
    return res


if __name__ == "__main__":
    response = request("https://www.tiobe.com/tiobe-index/")
    print(response.text)
