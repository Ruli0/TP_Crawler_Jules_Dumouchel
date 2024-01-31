import urllib.request
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import xml.etree.ElementTree as ET
import sqlite3
from urllib.robotparser import RobotFileParser
import urllib.request as urllib
from urllib.parse import urljoin
import urllib.error




class CrawlerWeb:
    def __init__(self, start_url, max_urls=50, max_links_page = 5, verbose=False):
        self.start_url = start_url
        self.visited_urls = set()
        self.urls_to_visit = [start_url]
        self.crawled_urls = []
        self.max_urls = max_urls
        self.max_links_per_page = max_links_page
        self.last_download_time = time.time()
        self.verbose = verbose


        """
        Attributs :

    start_url (chaîne de caractères) : L'URL à partir de laquelle le crawl commence.
    visited_urls (ensemble) : Les URLs qui ont déjà été visitées.
    urls_to_crawl (liste) : Les URLs trouvées et qui doivent être parcourues.
    crawled_urls (liste) : Les URLs qui ont été parcourues.
    max_urls (entier) : Le nombre maximal d'URLs à parcourir.
    max_links_per_page (entier) : Le nombre maximal de liens à suivre sur une page.
    last_download_time (flottant) : L'heure du dernier téléchargement.
    verbose (booléen) : Indique si des informations supplémentaires doivent être affichées pendant le processus de crawl.

        """

    def crawl(self):

        self.visited_urls = set()
        while self.urls_to_visit and len(self.visited_urls) < self.max_urls:
            current_url = self.urls_to_visit.pop(0)
            print(f"Crawling: {current_url}")
            
            try:
                response = requests.get(current_url)
                self.visited_urls.add(current_url)

                soup = BeautifulSoup(response.text, 'html.parser')
                links_found = 0

                for link in soup.find_all('a', href=True):
                    link_url = urljoin(current_url, link['href'])
                    if not link_url.startswith('http'):
                        continue  # Ignorer les URLs non valides ou relatives
                    if self.can_crawl(link_url):
                         # Ignorer les URLs non autorisées
                        if links_found >= self.max_links_per_page:
                            break

                    new_url = urljoin(current_url, link['href'])
                    if new_url not in self.visited_urls and new_url not in self.urls_to_visit:
                        self.urls_to_visit.append(new_url)
                        self.store_page_with_new_connection(new_url) #Permet de stocker les pages dans la base de données
                        print(f"Found link: {new_url}")
                        links_found += 1

                time.sleep(3) # Respect de la politeness en attedant 3 secondes entre chaque appel

            except requests.RequestException:
                pass

            if len(self.visited_urls) >= self.max_urls:
                break

        return self.visited_urls
    


    
    def can_crawl(self, url):
        rp = RobotFileParser()
        robots_txt_url = urljoin(url, "/robots.txt")
        try:
            rp.set_url(robots_txt_url)
            rp.read()
        except urllib.error.URLError as e:
            print(f"Erreur lors de l'accès à {robots_txt_url}: {e}")
            return False
        except Exception as e:
            print(f"Erreur inattendue lors de l'accès à {robots_txt_url}: {e}")
            return False

        if self.verbose:
            print(f"Permission de crawler {url} : {rp.can_fetch('*', url)}")
        return rp.can_fetch("*", url)







    def get_visited_urls(self):
        return self.visited_urls

    def get_sitemaps_from_index(self, sitemap_index_url):
        response = requests.get(sitemap_index_url)
        if response.status_code != 200:
            return []

        sitemap_index = ET.fromstring(response.content)
        sitemap_urls = [sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for sitemap in sitemap_index.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')]
        return sitemap_urls


    def get_urls_from_sitemap(self, sitemap_url):
        response = requests.get(sitemap_url)
        if response.status_code != 200:
            return []

        sitemap = ET.fromstring(response.content)
        page_urls = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for url in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')]
        return page_urls
    

    def crawl_site_map(self, sitemap_index_url, max_urls=100): # On augmente le threshold à 100.
        
        self.visited_urls = set()
        self.visited_urls = set()
        sitemap_urls = self.get_sitemaps_from_index(sitemap_index_url)

        for sitemap_url in sitemap_urls:
            if len(self.visited_urls) >= self.max_urls:
                break
            if self.can_crawl(sitemap_url):


                page_urls = self.get_urls_from_sitemap(sitemap_url)
                for page_url in page_urls:
                    if len(self.visited_urls) >= max_urls:
                        break

                    if page_url not in self.visited_urls:
                        print(f"Crawling: {page_url}")
                        self.visited_urls.add(page_url)
                        self.store_page_with_new_connection(page_url) #Permet de stocker les pages dans la base de données
                        time.sleep(5)  # Respect de la politesse

        return self.visited_urls
    

    def store_page_with_new_connection(self, url):
        try:
            conn = sqlite3.connect("webpage.db")
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS webpage
                (url text, age real)"""
            )
            cursor.execute("INSERT INTO webpage VALUES (?, ?)", (url, time.time()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
