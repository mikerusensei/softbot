import requests

from bs4 import BeautifulSoup
from command import Date_Parser

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

class Scraper_Url(Scraper):
    def scrape_url(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            section = soup.find('section', id='inq_section')
            infos = section.find_all('div', id='ncg-info')
            links_dict = {} # title: url
            for info in infos:
                h1_tag = info.find('h1')
                a_tag = h1_tag.find('a')
                # links_dict["title"] = a_tag.get_text()
                # links_dict["url"] = a_tag['href']
                links_dict[a_tag.get_text()] = a_tag['href']
            return links_dict
        else:
            print(f"Failed to retrieve URL: {response.status_code}")
            return None

class Scraper_Article(Scraper):
    def scrape_article(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find('section', id='inq_section')
            # author = article.find('div', id='art_author')
            # print(f"Author: {author.get_text()}")
            date = article.find('div', id='art_plat')
            # print(f"Date: {date.get_text()}")
            parsed_date = Date_Parser(date.get_text()).execute()
            content = article.find('div', id='article_content')
            paragraphs = content.find_all('p')

            fetch_paragraphs = []
            for paragraph in paragraphs:
                divs = paragraph.find_all('div')
                strong = paragraph.find_all('strong')

                if divs:
                    continue
                if strong:
                    continue
                if 'wp-caption-text' in paragraph.get('class', []):
                    continue
                if 'headertext' in paragraph.get('class', []):
                    break
                if paragraph.get_text(strip=True):
                    fetch_paragraphs.append(paragraph)
                
            converted_article = self.convert_paragraph(fetch_paragraphs)
            return converted_article, parsed_date
        else:
            print(f"Failed to retrieve article: {response.status_code}")
            return None
    
    def convert_paragraph(self, paragraphs):
        converted_paragraph = ""
        for paragraph in paragraphs:
            converted_paragraph += paragraph.get_text(strip=True) + " "
        return converted_paragraph.strip()
