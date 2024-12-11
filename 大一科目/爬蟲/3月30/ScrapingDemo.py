import requests

url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=HTC"
headers1 = {
    "User-Agent":"Mozilla/5.0 (Macintosh;" 
    "Intel Mac OS X 10_14_5) AppleWebKit/605.1.15"
    "(KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
}

r= requests.get(url, headers=headers1)

if r.status_code == requests.codes.OK:
    r.encoding = "utf8"
    print(r.text)
else:
    print("http Error..."+url)
