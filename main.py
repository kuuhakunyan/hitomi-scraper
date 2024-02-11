from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import logging
from utils import write_urls_to_txt, get_tags_str, get_doujinshi_id_set_from_dir, get_doujinshi_id_from_url

logging.basicConfig(level=logging.INFO)

class HitomiScraper:
    def get_driver(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        return driver
    
    def get_page_key(self, page_url):
        page_key = "?page="
        if page_url.find("search.html") != -1:
            page_key = "#"
        return page_key
    
    def clean_page_url(self, page_url):
        page_key_start_index = page_url.find(self.get_page_key(page_url))
        if page_key_start_index == -1:
            return page_url
        return page_url[:page_key_start_index]
    
    def is_page_loaded(self, driver, page_url, timeout=20):
        driver.get(page_url)
        try:
            element = WebDriverWait(driver, timeout=timeout).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div[class=page-container]>ul>li"))
            )
        except:
            return False
        return True

    def count_pages(self, driver, page_url):
        if not self.is_page_loaded(driver, page_url):
            return 0
        bs = BeautifulSoup(driver.page_source, "lxml")
        page_containers = bs.find_all("div", class_="page-container")
        if len(page_containers) == 0:
            return
        unordered_list = page_containers[-1].find("ul")
        if not unordered_list:
            return 0
        list_items = unordered_list.find_all("li")
        if len(list_items) == 0:
            return 0
        if len(list_items) == 1:
            return 1
        return int(list_items[-1].find("a").text)
        
    def scrape_page(self, driver, page_url, doujinshi_urls):
        if not self.is_page_loaded(driver, page_url):
            return
        bs = BeautifulSoup(driver.page_source, "lxml")
        lillies = bs.find_all("a", class_="lillie")
        if len(lillies) == 0:
            return
        for lillie in lillies:
            doujinshi_urls.append(f"https://hitomi.la{lillie["href"]}")
    
    def scrape_all(self, page_url):
        doujinshi_urls = []
        cleaned_page_url = self.clean_page_url(page_url)
        driver = self.get_driver()
        page_count = self.count_pages(driver, cleaned_page_url)
        logging.info(f"found {page_count} pages from {cleaned_page_url}")
        driver.quit()
        for i in range(1, page_count + 1):
            page_url = f"{cleaned_page_url}{self.get_page_key(cleaned_page_url)}{i}"
            driver = self.get_driver()
            self.scrape_page(driver, page_url, doujinshi_urls)
            logging.info(f"finished scraping page {i}")
            driver.quit()
        logging.info(f"found {len(doujinshi_urls)} urls")
        return doujinshi_urls

def main():
    # print(get_tags_str([
    #     "female:milf",
    #     "language:english",
    #     "neighbor",
        
    #     "-female:futanari",
    #     "-male:feminization",
    #     "-female:shemale",
        
    #     "-female:bestiality",
    #     "-male:bestiality",
    #     "-female:humiliation",
    #     "-male:humiliation",
    #     "-female:transformation",
    #     "-male:transformation",
    # ]))
    
    scraper = HitomiScraper()
    doujinshi_urls = []
    for url in [
        "https://hitomi.la/artist/gin%20eiji-english.html",
        "https://hitomi.la/artist/kawaisaw-english.html",
    ]:
        doujinshi_urls += scraper.scrape_all(url)
    new_doujinshi_urls = []
    for doujinshi_url in set(doujinshi_urls):
        if not get_doujinshi_id_from_url(doujinshi_url) in get_doujinshi_id_set_from_dir("Z:/hitomi"):
            new_doujinshi_urls.append(doujinshi_url)
    logging.info(f"found {len(new_doujinshi_urls)} new urls")
    write_urls_to_txt(f"{time.time()}.txt", new_doujinshi_urls)

main()