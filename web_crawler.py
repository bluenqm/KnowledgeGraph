import requests
from bs4 import BeautifulSoup
import requests
class WebCrawler:
    def __init__(self, url):
        self.url = url

    def download_html(self, url, download_file_name):
        response = requests.get(url)
        with open(download_file_name, "wb") as file:
            file.write(response.content)

    def url_exists(self, any_url):
        try:
            response = requests.head(any_url)
            return response.status_code < 400
        except requests.ConnectionError:
            return False