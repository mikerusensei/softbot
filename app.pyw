import re
import time
import socket

from tkinter import messagebox
from summarizer import summarize
from datetime import datetime, timedelta

from scraper import Scraper_Url, Scraper_Article
from command import Load_JSON, Save_JSON


class App:
    def __init__(self):
        self.file_path = "data.json"
        self.cache = Load_JSON(self.file_path).execute()
        self.current_time = datetime.now()
        self.end_day = self.current_time.replace(hour=23, minute=59, second=0, microsecond=0)
        self.start_day = self.current_time.replace(hour=00, minute=00, second=0, microsecond=0)

        self.base_url = "https://newsinfo.inquirer.net/"

        self.wheather_related_keywords = ["storm", "rain", "tsunami",  "tornado", "heatwave",  "cyclone"]
        self.land_related_keywords = ["earthquakes", "earthquake", "landslide", "landslides", "drought", "volcano", "eruption"]
        self.emergency_situation_keywords = ["outbreak", "pandemic", "fire", "accident", "explosion"]
        self.health_related_keywords = ["disease", "virus", "infection", "vaccine"]
        self.general_keywords = ["warning", "danger", "hazard", "security", "suspend", "suspension"]
        self.keywords = self.wheather_related_keywords + self.land_related_keywords + self.emergency_situation_keywords + self.health_related_keywords + self.general_keywords

    def check_connection(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            return False

    def send_alert(self, message):
        messagebox.showinfo("Alert", message)

    def check_keyword(self, title, date, article, keywords):
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', article):
                summary = summarize(title, article)
                converted = ' '.join(summary)

                if keyword in self.wheather_related_keywords:
                    tips = "Maghanda sa paparating na pagbabago ng panahon"
                elif keyword in self.land_related_keywords:
                    tips = "Maging alerto sa iyong palagid"
                elif keyword in self.emergency_situation_keywords:
                    tips = "Lumapit sa pinakamalit na tanggapan ng gobyerno"
                elif keyword in self.health_related_keywords:
                    tips = "Palaging maghugas ng kamay at magbaon ng alcohol"
                elif keyword in self.general_keywords:
                    tips = "Maging alerto palagi at maging mapagmatyag!"
                
                message = f"Keyword: {keyword}\n{date}\n\n\"{title}\"\n-->{converted}\n\nTIPS:\n{tips}"

                self.send_alert(message)
                break
    
    def remove_old_titles(self):
        days_ago = self.current_time - timedelta(days=3)

        list_titles = []
        for title, data in self.cache.items():
            convert_date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")

            if convert_date < days_ago:
                list_titles.append(title)
        
        for title in list_titles:
            del self.cache[title]

    def scrape(self):
        if self.check_connection():
            scraper = Scraper_Url(self.base_url)
            links = scraper.scrape_url()

            for title, url in links.items():
                if title in self.cache:
                    print("Title scraped already!")
                    continue
                else:
                    self.remove_old_titles()
                    scraper_article = Scraper_Article(url)
                    article, date = scraper_article.scrape_article()
                    if date > self.start_day and date < self.end_day:
                        self.check_keyword(title, date, article, self.keywords)
                    else:
                        print(f"{date} News is not news today")

                    self.cache[title] = {
                        "url": url,
                        "date": date.strftime("%Y-%m-%d %H:%M:%S")
                    }
            Save_JSON(self.cache, self.file_path).execute()
            return True
        else:
            messagebox.showerror("Error", "Please connect to the internet!\nThen rerun the program.")
            return False
        
if __name__ =='__main__':
    app = App()
    running = True
    # result = app.scrape()
    while running:
        result = app.scrape()
        if result:
            time.sleep(900)
        else:
            running = False