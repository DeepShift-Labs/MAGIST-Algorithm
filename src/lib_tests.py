# from MAGIST.UnsupervisedModels.img_cluster import RoughCluster
# from MAGIST.WebScraper.google import GoogleScraper
# from MAGIST.WebScraper.wikipedia import WikipediaScraper
#
# clusterer = RoughCluster("config.json")
#
# clusterer.unsupervised_clusters(2, "test.jpg", (600, 600), "Masks")
#
# ggl = GoogleScraper("config.json", 'AIzaSyD8imJeBtrVtSJdpFuUgdMQ_oRsbFigc1k', 'd768e8d28e79fb322')
#
# name = ggl.reverse_image_search("Masks/masked1.jpg")
#
# wiki = WikipediaScraper("config.json")
#
# summary = wiki.get_summary(name)
#
# print(summary)


from MAGIST.DetectionDataManager.image_slicer import ImageSlicer

slicer = ImageSlicer("config.json")

coordinates = slicer.coordinate_compute((300, 300), (50, 50))

slicer.crop_segments(coordinates, "Pics", "Sliced", "ostrich")