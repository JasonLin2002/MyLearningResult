import requests
from bs4 import BeautifulSoup as bs

def get_webSource(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh;" 
        "Intel Mac OS X 10_14_5) AppleWebKit/605.1.15"
        "(KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}
    session = requests.session()
    return session.post(url, data=payload, headers=headers)

def parse_html(r):
    if r.status_code == requests.codes.OK:
        r.encoding = "utf8"
        soup = bs(r.text, "html.parser")
    else:
        print("Parse_html Error")
        soup = None
    return soup

def main(url, payload):
    r=get_webSource(url, payload)
    print(r.text)

if __name__ == "__main__":
    url = "http://140.134.53.58/~D1146188/loginCheck.php"
    payload = {"id": "Jack", "pw": "1245"}
    main(url, payload)