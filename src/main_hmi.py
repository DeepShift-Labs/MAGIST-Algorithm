from MAGIST.NLP.WordScraper import FullDictionarySearch
from MAGIST.NLP.SelfAttention import TextPreprocessing
from MAGIST.NLP.AudioTranscriber import GoogleAudioTranscriber
from MAGIST.Vision.UnsupervisedModels.img_cluster import RoughCluster
import numpy as np
import os
from os import walk
from tqdm import tqdm

filenames = next(walk("inputs"), (None, None, []))[2]  # [] if no file

cluster = RoughCluster("config/config.json")

for f in tqdm(filenames):
    try:
        imgs = cluster.unsupervised_clusters(
            3, f"inputs/{f}", (200, 200), "Clusters")

        from MAGIST.Utils.WebScraper.google import GoogleScraper

        scraper = GoogleScraper("config/config.json")

        labels = []

        for i in imgs:
            label = scraper.reverse_image_search(i)
            labels.append(label)

        labels = np.unique(np.array(labels))

        from MAGIST.TaskManagment.ThreadedQueue import MainPriorityQueue

        queue = MainPriorityQueue("config/config.json")
        queue.detach_thread()

        priority = 1

        for l in labels:
            scraper.download_raw_img_dataset(l, 10, "Data/")

        from MAGIST.Vision.DetectionDataManager.image_slicer import ImageSlicer

        slicer = ImageSlicer("config/config.json")

        counter = 0
        for l in labels:
            path = os.path.join("Data", l)
            file = os.listdir(path)

            for f in file:
                full_path = os.path.join(path, f)
                os.system(
                    f"mv '{full_path}' '{os.path.join(path, f'Frame{str(counter).zfill(2)}.jpg')}'")
                counter += 1

        counter = 0
        for l in labels:
            path = os.path.join("Data", l)
            os.listdir(path)

        for l in labels:
            path = os.path.join("Data", l)

            slicer.image_integrity_verification(path, delete_invalid=True)
            slicer.resizer((500, 500), path)
            coordinates = slicer.coordinate_compute((500, 500), (100, 100))
            slicer.crop_segments(coordinates, path, "Sliced", l)

        from MAGIST.Vision.FullySupervisedModels.MAGIST_Lite_Detector import MAGIST_CNN

        cnn = MAGIST_CNN("config/config.json")

        queue.put_queue(cnn, name="MAGIST_CNN_Trainer", priority=10)

        from MAGIST.Utils.WebScraper.wikipedia import WikipediaScraper
        from MAGIST.NeuralDB.MongoUtils import AdminUtils

        mongo_admin = AdminUtils("config/config.json")
        client = mongo_admin.initialize_neuraldb()

        from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB

        neural_db = NeuralDB("config/config.json", client)
        neural_db.recreate_db()

        wiki = WikipediaScraper("config/config.json")

        for l in labels:
            description = wiki.get_summary(l)
            neural_db.insert_obj_desc(l, description)

        neural_db.remove_duplicates()
        queue.join_thread()
    except BaseException:
        print("=============================BIG ERROR: SKIP IMAGE=============================")
        pass


transcriber = GoogleAudioTranscriber("config/config.json")

text = transcriber.microphone_listener()


selfattention = TextPreprocessing("config/config.json")

selected = []
for i in selfattention.__call__(text):
    if i[2] == "Good":
        selected.append(i[1])


search_res = []
unused_terms = []
for i in selected:
    res = neural_db.search_entire_db(i)
    if res != []:
        search_res.append(res)
    else:
        unused_terms.append(i)

search_res = np.array(search_res)
search_res = np.squeeze(search_res)

try:
    print("=====================================================================================================")
    print(search_res)
    print("=====================================================================================================")
    print(unused_terms)
except IndexError:
    print("No results found")


dict = FullDictionarySearch("config/config.json")

for i in unused_terms:
    definition = dict.define(i)
    neural_db.insert_word_desc(i, definition)

neural_db.remove_duplicates()
