import asyncio
import logging
import os
import re
import threading
from venv import logger
import zipfile
import httpx
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from retrying import retry
import configparser
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

session = requests.Session()
adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50)
session.mount('http://', adapter)
session.mount('https://', adapter)
 
def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def ensure_config_file_exists(config_path):
    if not os.path.exists(config_path):
        create_config_file(config_path)

def create_config_file(config_path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'url': '',
                         'output_folder': '',  # 使用配置文件目录的 'output' 作为默认值
                         'Whether_to_compress_files': 'True'}  # 设置默认布尔值为 'True'
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    logger.info(f"已创建配置文件模板：{config_path}")


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def write_config(section, option, value, config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set(section, option, value)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# 获取当前脚本的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}


#分析漫画
def fetch_comics(url, tag, page=1):
    base_url = url + '/search/'
    headers = {
        # Add your headers here if needed
    }
    params = {
        "q": tag,
        "f": "_all",
        "s": "create_time_DESC",
        "syn": "yes",
        "p": page
    }

    # 发起请求并解析响应内容
    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 收集所有漫画信息
    comics = soup.find_all("li", class_="gallary_item")
    comics_details = []
    for comic in comics:
        title = comic.find("div", class_="title").a.text.strip()
        link = urljoin(base_url, comic.find("div", class_="title").a['href'])
        comics_details.append({
            "title": title,
            "link": link
        })

    # 返回总页数和漫画详情
    return  comics_details

def sanitize_filename(filename):
    """
    Remove illegal characters from the filename
    """
    # Windows文件名中不允许的字符
    invalid_chars = r'[\\/*?:"<>|]'
    sanitized = re.sub(invalid_chars, '', filename)
    return sanitized

def download_comic1(comic_url, output_folder, headers):
    # 构建下载页面的URL
    download_url = comic_url.replace("/photos-index-", "/download-index-")
    
    # 打印下载URL，以便查看它是否正确
    logger.info(f"下载URL: {download_url}")

    try:
        # 发送请求并设置请求头
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()  # 检查是否有请求错误

        # 解析下载页面的HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        download_div = soup.find('div', class_='download_btn')

        # 提取文件名
        file_name = soup.find('p', class_='download_filename').text.strip()
        # 编码和解码文件名以忽略无法解码的字符
        file_name_safe = file_name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        file_name_safe = sanitize_filename(file_name_safe)
        if download_div:
            download_links = download_div.find_all('a', class_='down_btn', href=True)

            # 确保输出文件夹存在
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for download_link in download_links:
                download_href = download_link['href']
                download_url = f"https:{download_href}"
                
                # 构建完整的文件路径
                file_path = os.path.join(output_folder, file_name_safe)

                # 检查文件是否已存在
                if not os.path.exists(file_path):
                    # 发送请求并获取文件总大小
                    file_response = requests.get(download_url, stream=True)
                    total_size_in_bytes = int(file_response.headers.get('content-length', 0))
                    
                    # 添加文件大小检查，如果小于100KB则不下载
                    if total_size_in_bytes < 100 * 1024:  # 100KB
                        logger.info(f"请求失败.")
                        return False
                    else:
                        block_size = 1024  # 1 Kilobyte

                        # 显示进度条并写入文件
                        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                        with open(file_path, 'wb') as file:
                            for data in file_response.iter_content(block_size):
                                progress_bar.update(len(data))
                                file.write(data)
                        progress_bar.close()

                        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                            logger.info("ERROR, something went wrong")

        return True

    except requests.exceptions.RequestException:
        return False


# 设置基本的日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化下载的图片集合和线程锁
downloaded_images = set()
lock = threading.Lock()


def download_comic2(url, comic_url, output_folder, zip_output=False):
    def get_option_values(page_url, session):
        response = session.get(page_url)
        if response.status_code != 200:
            logger.error("Failed to fetch page: %s", page_url)
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        select_element = soup.find('select', class_='pageselect')
        if not select_element:
            return []

        return [option.get('value') for option in select_element.find_all('option')]

    def extract_img_url(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tag = soup.find('img', id='picarea')
        if img_tag and 'src' in img_tag.attrs:
            return 'https:' + img_tag['src']
        return None

    @retry(stop_max_attempt_number=5, wait_fixed=500)
    def download_image(img_url, download_folder, zip_file=None):
        with lock:
            if img_url in downloaded_images:
                logger.info(f"Image already downloaded: {img_url}")
                return

        response = requests.get(img_url)
        if response.status_code == 200:
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(download_folder, img_name)

            if zip_file:
                zip_file.writestr(img_name, response.content)
                logger.info(f"Downloaded image to ZIP: {img_url}")
            else:
                with open(img_path, 'wb') as img_file:
                    img_file.write(response.content)
                logger.info(f"Downloaded image: {img_url}")

            with lock:
                downloaded_images.add(img_url)
        else:
            logger.error(f"Failed to download image from URL: {img_url}")
            raise Exception(f"Failed to download image from URL: {img_url}")

    def download_page(value, session, download_folder, zip_file=None):
        page_url = f"{url}/photos-view-id-{value}.html"
        response = session.get(page_url)
        if response.status_code == 200:
            img_url = extract_img_url(response.text)
            if img_url:
                logger.info(f"Downloading image: {img_url}")
                download_image(img_url, download_folder, zip_file)
            else:
                logger.warning(f"No image URL found for page: {page_url}")
        else:
            logger.error(f"Failed to fetch URL: {page_url}")

    session = requests.Session()
    response = session.get(comic_url)
    if response.status_code != 200:
        logger.error("Failed to fetch comic URL: %s", comic_url)
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    file_name = soup.find('h2').get_text(strip=True)
    # 编码和解码文件名以忽略无法解码的字符
    file_name_safe = file_name.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    logger.info("File Name: %s", file_name_safe)
    comic_id = soup.find('div', class_='pic_box tb').find('a')['href'].split('-')[-1].split('.')[0]
    logger.info("Comic ID: %s", comic_id)
    total_page_url = f"{url}/photos-view-id-{comic_id}.html"
    values = get_option_values(total_page_url, session)

    max_threads = 50  # 设置线程池大小

    if zip_output:
        zip_file_path = os.path.join(output_folder, file_name_safe + '.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                for value in values:
                    executor.submit(download_page, value, session, output_folder, zip_file)
            logger.info(f"Comic downloaded and zipped: {zip_file_path}")
    else:
        download_folder = os.path.join(output_folder, file_name_safe)
        os.makedirs(download_folder, exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for value in values:
                executor.submit(download_page, value, session, download_folder)

        logger.info(f"Comic downloaded to folder: {download_folder}")


def download_file(url, comic_url, output_folder):
    download_directory = output_folder

    # 读取配置文件中是否开启压缩文件下载
    config = load_config(config_path)
    Whether_to_compress_files = config.getboolean('DEFAULT', 'Whether_to_compress_files', fallback=True)

    logger.info(f"开始下载: {comic_url}")

    response = requests.get(comic_url, stream=True)
    logger.info(f"请求状态码：{response.status_code}")

    if response.status_code == 200:
        # 调用 download_comic1 尝试下载
        if download_comic1(comic_url, download_directory, headers):
            return True
        else:
            logger.info("download_comic1 下载失败，尝试使用 download_comic2")
            return download_comic2(url, comic_url, download_directory, Whether_to_compress_files)
    else:
        logger.info(f"下载失败，状态码：{response.status_code}")
        logger.info("尝试使用备用下载方法 download_comic2。")
        return download_comic2(url, comic_url, download_directory, Whether_to_compress_files)


#从发布页获取可用域名
async def webtest(start_url):
    def get_urls_from_page(url):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            all_div = soup.find('div', id='all')
            ul_tag = all_div.find('ul')
            li_tags = ul_tag.find_all('li')

            urls = []
            for li in li_tags:
                a_tags = li.find_all('a')
                for a in a_tags:
                    href = a.get('href')
                    # 移除结尾的斜杠（如果存在）
                    if href.endswith('/'):
                        href = href[:-1]
                    # 检查 URL 是否以 .org 或 .cn 结尾，或者包含 'google.cn'
                    if not (href.endswith('.org') or href.endswith('.cn') or 'google.cn' in href or 'wnacg.date' in href):
                        urls.append(href)

            return urls[1:] 
        except Exception as e:
            return []


    async def fetch_url(client, url):
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return url, response.status_code
            else:
                return url, None
        except httpx.RequestError:
            return url, None

    async def test_url_status(client, urls):
        tasks = [fetch_url(client, url) for url in urls]
        valid_urls = []
        for task in asyncio.as_completed(tasks):
            url, status = await task
            if status == 200:
                valid_urls.append(url)  # 确保添加的是完整的URL
        return valid_urls


    urls = get_urls_from_page(start_url)
    if not urls:
        logger.info("获取URLs时出现错误。")
        return None
    filtered_urls = [url for url in urls if not (url.endswith('.org') or url.endswith('.cn'))]

    # 创建和使用 httpx.AsyncClient 客户端
    async with httpx.AsyncClient() as client:
        valid_urls = await test_url_status(client, filtered_urls)
        return valid_urls[0] if valid_urls else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.ini')

    if not os.path.exists(config_path):
        create_config_file(config_path)

    config = load_config(config_path)
    default_url = "https://wnacg01.org"
    url = config.get('DEFAULT', 'url', fallback=default_url)
    output_folder = config.get('DEFAULT', 'output_folder', fallback="")
    Whether_to_compress_files = config.getboolean('DEFAULT', 'Whether_to_compress_files', fallback=True)

    config_complete = all([config.has_option('DEFAULT', option) for option in ['url', 'output_folder', 'Whether_to_compress_files']])

    if not config_complete or not output_folder:
        # 检查url配置
        if not config.has_option('DEFAULT', 'url') or not url:
            user_url = input(f"请输入发布页URL (回车使用默认:{default_url}): ")
            if not user_url:  # 如果用户直接回车，使用默认值
                url = default_url
            elif validate_url(user_url):  # 如果用户输入了新的URL且是有效的
                url = user_url
            write_config('DEFAULT', 'url', url, config_path)

        if not output_folder:
            user_output_folder = input(f"请输入下载目录 (回车使用当前目录的output文件夹): ")
            if user_output_folder:
                if os.path.isdir(user_output_folder):
                    output_folder = user_output_folder
                else:
                    logger.info("无效的目录输入，使用默认配置。")
            if not output_folder:
                output_folder = os.path.join(script_dir, "output")
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                logger.info(f"已创建输出目录：{output_folder}")
            write_config('DEFAULT', 'output_folder', output_folder, config_path)

        if not config.has_option('DEFAULT', 'Whether_to_compress_files'):
            user_compress_input = input(f"是否开启压缩包下载？(1: 是, 0: 否, 回车默认为是): ")
            if user_compress_input in ["1", "0"]:
                Whether_to_compress_files = user_compress_input == "1"
            else:
                logger.info("无效的输入，使用默认配置。")
            write_config('DEFAULT', 'Whether_to_compress_files', str(Whether_to_compress_files), config_path)


    current_base_url = asyncio.run(webtest(url))
    logger.info(f"目前使用域名:{current_base_url}")
            
    exit_program = False  # 设置退出标志

    while not exit_program:
        user_input = input("请输入关键词或漫画链接: ")
        if user_input == 'q':
            break

        if user_input.startswith('https://'):
            logger.info("检测到漫画链接，准备下载...")
            download_file(current_base_url, user_input, output_folder)
            continue

        tag = user_input
        current_page = 1
        comics = fetch_comics(current_base_url, tag, current_page)

        base_search_url_pattern = f"{current_base_url}/search?q={tag}&f=_all&s=create_time_DESC&syn=yes&p={current_page}"
        search_url = base_search_url_pattern.format(tag=tag, page=current_page)
        logger.info(f"搜索的tag链接: {search_url}")

        for index, comic in enumerate(comics, start=1):
            logger.info(f"C{index}: {comic['title']}")

        logger.info(f"\nPage:{current_page}")
        while True:
            user_input = input("\n输入'C序号'下载对应序号的漫画，输入罗马数字切换到对应页码，'P页码'下载对应页码的所有漫画，'q'退出程序:").upper()
            if user_input == 'Q':
                exit_program = True  # 设置退出标志
                break

            if user_input.startswith('C'):
                try:
                    comic_index = int(user_input[1:]) - 1
                    if 0 <= comic_index < len(comics):
                        selected_comic = comics[comic_index]
                        logger.info(f"下载: {selected_comic['title']}")
                        download_file(current_base_url, comics[comic_index]['link'], output_folder)
                    else:
                        logger.info("序号错误，请重新输入")
                except ValueError:
                    logger.info("格式错误，请输入'C'后跟数字序号")

            elif user_input.startswith('P'):
                try:
                    page_number = int(user_input[1:])
                    logger.info(f"下载第 {page_number} 页的所有漫画")
                    # 因为不再需要总页数，直接调用 fetch_comics 函数即可
                    page_comics = fetch_comics(current_base_url, tag, page_number)
                    for comic in page_comics:
                        logger.info(f"下载: {comic['title']}")
                        download_file(current_base_url, comic['link'], output_folder)
                except ValueError:
                    logger.info("格式错误，请输入'P'后跟页码数字")

            elif user_input.isdigit():
                page_number = int(user_input)
                logger.info(f"切换到第 {page_number} 页")
                current_page = page_number
                comics = fetch_comics(current_base_url, tag, current_page)
                if not comics:
                    logger.info("页面不存在")
                else:
                    for index, comic in enumerate(comics, start=1):
                        logger.info(f"C{index}: {comic['title']}")
                    logger.info(f"\nPage:{current_page}")                    
            else:
                try:
                    roman_page_number = roman_to_int(user_input)
                    logger.info(f"切换到罗马数字页码 {roman_page_number}")
                    current_page = roman_page_number
                    comics = fetch_comics(current_base_url, tag, current_page)
                    if not comics:
                        logger.info("页面不存在")
                    else:
                        for index, comic in enumerate(comics, start=1):
                            logger.info(f"C{index}: {comic['title']}")
                        # 不再需要打印当前页码信息
                except (ValueError, KeyError):
                    logger.info("输入无效，请输入'C序号'下载漫画，'P页码'下载该页所有漫画，或罗马数字切换页码")


def roman_to_int(s):
    """
    Convert a Roman numeral to an integer.
    """
    s = s.upper() 
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    num = 0
    prev_value = 0

    for i in range(len(s) - 1, -1, -1):
        int_val = roman_dict.get(s[i], 0) 
        if int_val < prev_value:
            num -= int_val
        else:
            num += int_val
        prev_value = int_val

    return num

def find_roman_page_number(user_input):
    """
    Find and return the Roman page number in user input.
    """
    user_input = user_input.lower()
    for word in user_input.split():
        if word.isalpha() and all(char in 'ivxlcdm' for char in word):
            return roman_to_int(word)
    return None


if __name__ == "__main__":
    main()
