
# CrawlerWeb : Un outil de Web Crawling en Python

## Créé par Jules Dumouchel

## À propos

`CrawlerWeb` est une classe Python conçue pour faciliter le web crawling. Elle offre une approche simple mais puissante pour parcourir des sites web, récupérer des liens et les stocker dans une base de données tout en respectant les règles du fichier `robots.txt` des sites.

### Fonctionnalités Clés

- **Crawl Simple**: Parcourt les pages web à partir d'une URL de départ, en collectant les liens.
- **Respect de la Politesse**: Pause de 3 secondes entre chaque requête pour ne pas surcharger les serveurs.
- **Traitement des Sitemaps**: Permet de récupérer les URLs depuis des fichiers sitemap et sitemap index.
- **Stockage des Données**: Stocke les URLs visitées dans une base de données SQLite.
- **Respect des Règles de robots.txt**: Vérifie le fichier `robots.txt` de chaque site pour s'assurer que le crawl est autorisé.
- **Configuration Flexible**: Paramètres personnalisables pour le nombre maximal de pages et de liens par page.
- **Mode Verbose**: Option pour des logs détaillés pendant le processus de crawl.

## Utilisation

### Initialisation

```python
crawler = CrawlerWeb("https://example.com", max_urls=50, max_links_page=5, verbose=True)
```

### Démarrer le Crawl

```python
visited_urls = crawler.crawl()
```

### Récupérer les URLs depuis un Sitemap

```python
sitemap_urls = crawler.get_sitemaps_from_index("https://example.com/sitemap_index.xml")
page_urls = crawler.get_urls_from_sitemap("https://example.com/sitemap.xml")
```

### Exécuter un Crawl Complet à partir d'un Sitemap Index

```python
all_urls = crawler.crawl_site_map("https://example.com/sitemap_index.xml", max_urls=150)
```

### Stocker les Pages dans la Base de Données

Les pages visitées sont automatiquement stockées dans une base de données SQLite.

## Dépendances

- Python 3.x
- `requests`
- `beautifulsoup4`
- `sqlite3`

### Installation des Dépendances

```bash
pip install requests beautifulsoup4
```

