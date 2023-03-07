from MAGIST.Vision.UnsupervisedModels.img_cluster import RoughCluster
from MAGIST.Utils.WebScraper.google import GoogleScraper
from MAGIST.TaskManagment.ThreadedQueue import MainPriorityQueue
from MAGIST.Utils.WebScraper.wikipedia import WikipediaScraper

use_esdb = True

if use_esdb:
    from MAGIST.NeuralDB.ElasticSearch import ESDB
elif not use_esdb:
    from MAGIST.NeuralDB.MongoUtils import AdminUtils
    from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB

import numpy as np
from os import walk
from tqdm import tqdm

filenames = next(walk("inputs"), (None, None, []))[2]  # [] if no file

cluster = RoughCluster("config/config.json")
scraper = GoogleScraper("config/config.json")
queue = MainPriorityQueue("config/config.json")

if use_esdb:
    elastic = ESDB("config/config.json", "http://localhost:9200", "config/queries.json", "config/schema.json")
    elastic.delete_all_indices()
    elastic.create_index("object_db", "object_db_schema")
    elastic.create_index("word_db", "word_db_schema")
elif not use_esdb:
    mongo_admin = AdminUtils("config/config.json")
    client = mongo_admin.initialize_neuraldb()
    neural_db = NeuralDB("config/config.json", client)

    neural_db.recreate_db()

wiki = WikipediaScraper("config/config.json")

for f in tqdm(filenames):
    try:
        imgs = cluster.unsupervised_clusters(
            3, f"inputs/{f}", (200, 200), "Clusters")

        labels = []

        for i in imgs:
            label = scraper.reverse_image_search(i)
            labels.append(label)

        labels = np.unique(np.array(labels))

        queue.detach_thread()

        priority = 1

        # for l in labels:
        # 	scraper.download_raw_img_dataset(l, 10, "Data/")

        # from MAGIST.Vision.DetectionDataManager.image_slicer import ImageSlicer
        #
        # slicer = ImageSlicer("config/config.json")
        #
        # counter = 0
        # for l in labels:
        # 	path = os.path.join("Data", l)
        # 	file = os.listdir(path)
        #
        # 	for f in file:
        # 		full_path = os.path.join(path, f)
        # 		os.system(f"mv '{full_path}' '{os.path.join(path, f'Frame{str(counter).zfill(2)}.jpg')}'")
        # 		counter += 1
        #
        # counter = 0
        # for l in labels:
        # 	path = os.path.join("Data", l)
        # 	os.listdir(path)
        #
        #
        # for l in labels:
        # 	path = os.path.join("Data", l)
        #
        # 	slicer.image_integrity_verification(path, delete_invalid=True)
        # 	slicer.resizer((500, 500), path)
        # 	coordinates = slicer.coordinate_compute((500, 500), (100, 100))
        # 	slicer.crop_segments(coordinates, path, "Sliced", l)
        #
        #
        #
        #
        # from MAGIST.Vision.FullySupervisedModels.MAGIST_Lite_Detector import MAGIST_CNN
        #
        # cnn = MAGIST_CNN("config/config.json")
        #
        # queue.put_queue(cnn, name="MAGIST_CNN_Trainer", priority=10)

        all_obj_data = []

        for l in labels:
            description = wiki.get_summary(l)
            if use_esdb:
                all_obj_data.append([l, description])
            elif not use_esdb:
                neural_db.insert_obj_desc(l, description)

        if use_esdb:
            for d in all_obj_data:
                temp_data = elastic.format_object_data(str(d[0]), str(d[1]))
                elastic.add_doc("object_db", "object_db_schema", temp_data)
        if not use_esdb:
            neural_db.remove_duplicates()
        queue.join_thread()

    except Exception as e:
        print("=============================BIG ERROR: SKIP IMAGE=============================")
        print(e)
        pass
