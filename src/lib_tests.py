from MAGIST.UnsupervisedModels.img_cluster import RoughCluster
from MAGIST.WebScraper.google import GoogleScraper
from MAGIST.WebScraper.wikipedia import WikipediaScraper

clusterer = RoughCluster("config.json")

clusterer.unsupervised_clusters(3, "test.jpg", (128, 128), "Masks")

ggl = GoogleScraper("config.json", 'AIzaSyD8imJeBtrVtSJdpFuUgdMQ_oRsbFigc1k', 'd768e8d28e79fb322')

name = ggl.reverse_image_search("Masks/masked1.jpg")

wiki = WikipediaScraper("config.json")

summary = wiki.get_summary(name)

print(summary)