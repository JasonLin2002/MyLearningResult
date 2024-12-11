import requests
from bs4 import BeautifulSoup as bs

def get_webSource(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh;" 
        "Intel Mac OS X 10_14_5) AppleWebKit/605.1.15"
        "(KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}
    return requests.get(url, headers=headers)

def generate_urls(url, start, end):
    urls = []
    for i in range(start,end):
        urls.append(url.format(i))
    return urls

def parse_html(r):
    if r.status_code == requests.codes.OK:
        r.encoding = "utf8"
        soup = bs(r.text,"html.parser")
    else:
        print("Parse_html Error")
        soup = None
    return soup

def getWords(soup):
    wordList = {}
    for wordList_table in soup.find_all(class_="wordlist"):
        for word_entry in wordList_table.find_all("tr"):
            wordList[word_entry.th.text] = word_entry.td.text
    return wordList
def main(url):
    urlList = generate_urls(url, 1, 1)
    for link in urlList:
        r = get_webSource(link)
        soup = parse_html(r)
        wordListResult = getWords(soup)
        for word in wordListResult:
            print(f'{word}:{wordListResult[word]}')

if __name__ == "__main__":
    url = "https://www.majortests.com/word-lists/word-list-{:02d}.html"
    main(url)