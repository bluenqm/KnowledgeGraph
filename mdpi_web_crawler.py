import requests
from bs4 import BeautifulSoup
from web_crawler import WebCrawler


class MDPIWebCrawler(WebCrawler):
    def __init__(self):
        super().__init__("https://www.mdpi.com/journal/aerospace")
        self.save_directory = "MDPI"

    def crawl(self):
        prefix = "https://www.mdpi.com/2226-4310/"
        for i in range(1, 10):
            volume_url = prefix + str(i)
            issue_index = 0
            while True:
                issue_index += 1
                issue_url = volume_url + "/" + str(issue_index)
                if not self.url_exists(issue_url):
                    break
                article_urls =  self.get_article_urls(issue_url)
                for article_url in article_urls:
                    full_url = "https://www.mdpi.com/" + article_url
                    self.download_url(full_url)
    def get_article_urls(self, issue_url):
        url_pattern = issue_url[20:]
        print("Getting articles from " + url_pattern)
        response = requests.get(issue_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all("a", class_="title-link")
        filtered_links = [link.get("href") for link in links if link.get("href").startswith(url_pattern)]
        return filtered_links

    def download_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("h1", class_="title hypothesis_container").text
        ascii_title = "".join(c for c in title if c.isalnum())
        filename = ascii_title.strip().replace(" ", "_") + ".html"
        file_path = f"{self.save_directory}/{filename}"
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(response.text)

