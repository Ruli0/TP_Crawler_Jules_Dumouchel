
from Crawler_web import CrawlerWeb

crawlerweb1 = CrawlerWeb(start_url = "https://ensai.fr/")

crawlerweb1.crawl()


with open("crawled_webpages.txt", "w") as file:
    for url in crawlerweb1.get_visited_urls():
        file.write(url + "\n")



crawlerweb1.crawl_site_map("https://ensai.fr/sitemap.xml")




with open("crawled_webpages_site_map.txt", "w") as file:
    for url in crawlerweb1.get_visited_urls():
        file.write(url + "\n")
