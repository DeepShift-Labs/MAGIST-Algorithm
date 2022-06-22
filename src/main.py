from MAGIST.Vision.UnsupervisedModels.img_cluster import RoughCluster
import time, os

cluster = RoughCluster("config.json")

imgs = cluster.unsupervised_clusters(3, "Input.jpg", (200, 200), "Clusters")


from MAGIST.Utils.WebScraper.google import GoogleScraper

scraper = GoogleScraper("config.json")

labels = []

for i in imgs:
	label = scraper.reverse_image_search(i)
	labels.append(label)

print(labels)

from MAGIST.TaskManagment.ThreadedQueue import MainPriorityQueue

queue = MainPriorityQueue("config.json")
queue.detach_thread()

priority = 1

def dummy(a, b, c):
	time.sleep(30)

for l in labels:
	queue.put_queue(dummy, l, 200, "Data/", name=f"Downloading {l}", priority=priority)
	priority += 1


from MAGIST.Vision.DetectionDataManager.image_slicer import ImageSlicer

slicer = ImageSlicer("config.json")



for l in labels:
	path = os.path.join("Data", l)
	slicer.image_integrity_verification(path, delete_invalid=True)
	slicer.resizer((500, 500), path)
	coordinates = slicer.coordinate_compute((500, 500), (100, 100))
	slicer.crop_segments(coordinates, path, "Sliced", l)




from MAGIST.Vision.FullySupervisedModels.MAGIST_Lite_Detector import MAGIST_CNN

cnn = MAGIST_CNN("config.json")

queue.put_queue(cnn, name="MAGIST_CNN_Trainer", priority=10)

from MAGIST.Utils.WebScraper.wikipedia import WikipediaScraper
from MAGIST.NeuralDB.MongoUtils import AdminUtils

mongo_admin = AdminUtils("config.json")
client = mongo_admin.initialize_neuraldb()

from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB

neural_db = NeuralDB("config.json", client)
neural_db.recreate_db()

wiki = WikipediaScraper("config.json")

for l in labels:
	description = wiki.get_summary(l)
	neural_db.insert_obj_desc(l, description)

queue.join_thread()
