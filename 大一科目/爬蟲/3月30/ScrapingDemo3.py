import requests

def get_webSource(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh;" 
        "Intel Mac OS X 10_14_5) AppleWebKit/605.1.15"
        "(KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}
    return requests.get(url, headers=headers)

def main(url):
    r=get_webSource(url)
    if r.status_code == requests.codes.OK:
        r.encoding = "utf8"
        print(r.text)
    else:
        print("http Error..."+url)

if __name__=="__main__":
    keyword = input()
    url = "https://search.books.com.tw/search/query/key/+keyword+/cat/all"
    main(url)

