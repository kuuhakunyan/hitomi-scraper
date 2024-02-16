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
    scraper = HitomiScraper()
    doujinshi_urls = []
    for url in [
        "https://hitomi.la/search.html?-female%3Acheating%20language%3Aenglish%20female%3Asole_female%20male%3Asole_male%20girlfriend%20-female%3Afutanari%20-male%3Afeminization%20-female%3Ashemale%20-female%3Abestiality%20-male%3Abestiality%20-female%3Ahumiliation%20-male%3Ahumiliation%20-female%3Atransformation%20-male%3Atransformation%20-type%3Aanime%20-female%3Ascat_insertion%20-female%3Agiantess%20-female%3Afemales_only%20-tag%3Awestern_cg%20-tag%3Awestern_imageset%20-tag%3Awestern_non-h%20-female%3Aminigirl%20-male%3Aminiguy%20-female%3Ainsect_girl%20-male%3Ainsect_boy%20-female%3Ascat%20-male%3Ascat%20-female%3Afarting%20-male%3Afarting%20-female%3Ainsect%20-male%3Ainsect%20-female%3Aguro%20-male%3Aguro%20-female%3Aamputee%20-male%3Aamputee%20-female%3Aomorashi%20-male%3Aomorashi%20-female%3Ainfantilism%20-male%3Ainfantilism%20-female%3Avore%20-male%3Avore%20-female%3Ashrinking%20-male%3Ashrinking%20-female%3Aunbirth%20-male%3Aunbirth%20-female%3Asmell%20-male%3Asmell%20-female%3Acbt%20-male%3Acbt%20-female%3Abdsm%20-male%3Abdsm%20-female%3Abondage%20-male%3Abondage%20-female%3Afurry%20-male%3Afurry%20-female%3Ahuman_on_furry%20-male%3Ahuman_on_furry%20-female%3Aurination%20-male%3Aurination%20-female%3Aprolapse%20-male%3Aprolapse%20-female%3Amidget%20-male%3Amidget%20-female%3Aabortion%20-male%3Aabortion%20-female%3Aanalphagia%20-male%3Aanalphagia%20-female%3Asnuff%20-male%3Asnuff%20-female%3Aasphyxiation%20-male%3Aasphyxiation",
        "https://hitomi.la/search.html?-female%3Acheating%20language%3Aenglish%20female%3Asole_female%20male%3Asole_male%20kanojo%20-female%3Afutanari%20-male%3Afeminization%20-female%3Ashemale%20-female%3Abestiality%20-male%3Abestiality%20-female%3Ahumiliation%20-male%3Ahumiliation%20-female%3Atransformation%20-male%3Atransformation%20-type%3Aanime%20-female%3Ascat_insertion%20-female%3Agiantess%20-female%3Afemales_only%20-tag%3Awestern_cg%20-tag%3Awestern_imageset%20-tag%3Awestern_non-h%20-female%3Aminigirl%20-male%3Aminiguy%20-female%3Ainsect_girl%20-male%3Ainsect_boy%20-female%3Ascat%20-male%3Ascat%20-female%3Afarting%20-male%3Afarting%20-female%3Ainsect%20-male%3Ainsect%20-female%3Aguro%20-male%3Aguro%20-female%3Aamputee%20-male%3Aamputee%20-female%3Aomorashi%20-male%3Aomorashi%20-female%3Ainfantilism%20-male%3Ainfantilism%20-female%3Avore%20-male%3Avore%20-female%3Ashrinking%20-male%3Ashrinking%20-female%3Aunbirth%20-male%3Aunbirth%20-female%3Asmell%20-male%3Asmell%20-female%3Acbt%20-male%3Acbt%20-female%3Abdsm%20-male%3Abdsm%20-female%3Abondage%20-male%3Abondage%20-female%3Afurry%20-male%3Afurry%20-female%3Ahuman_on_furry%20-male%3Ahuman_on_furry%20-female%3Aurination%20-male%3Aurination%20-female%3Aprolapse%20-male%3Aprolapse%20-female%3Amidget%20-male%3Amidget%20-female%3Aabortion%20-male%3Aabortion%20-female%3Aanalphagia%20-male%3Aanalphagia%20-female%3Asnuff%20-male%3Asnuff%20-female%3Aasphyxiation%20-male%3Aasphyxiation"
    ]:
        doujinshi_urls += scraper.scrape_all(url)
    if len(doujinshi_urls) == 0:
        return
    new_doujinshi_urls = []
    for doujinshi_url in set(doujinshi_urls):
        if not get_doujinshi_id_from_url(doujinshi_url) in get_doujinshi_id_set_from_dir("Z:/hitomi"):
            new_doujinshi_urls.append(doujinshi_url)
    logging.info(f"found {len(new_doujinshi_urls)} new urls")
    write_urls_to_txt(f"{time.time()}.txt", new_doujinshi_urls)

# print(get_tags_str([
#     # "female:milf",
#     # "language:english",
#     # "neighbor",
    
#     # "female:emotionless_sex",
    
#     "-female:cheating language:english female:sole_female male:sole_male kanojo"
    
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

main()