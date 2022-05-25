from MAGIST.WebScraper.wikipedia import WikipediaScraper

scraper = WikipediaScraper("config.json")

print(scraper.get_summary("doors"))
