# from MAGIST.NeuralDB.MongoUtils import AdminUtils
# from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB
#
#
# mongo_admin = AdminUtils("config/config.json")
# client = mongo_admin.initialize_neuraldb()
# neural_db = NeuralDB("config/config.json", client)
#
# neural_db.recreate_db()
#
#
# neural_db.search_entire_db("an")

# from MAGIST.Utils.WebScraper.google import GoogleScraper
#
# google_scraper = GoogleScraper("config/config.json")
# google_scraper.download_raw_img_dataset("robot", 100, "Data")

from PIL import Image
import os


def image_checker(path):
    os.chdir(path)
    for items in os.listdir(path):
        if items.endswith(".webp" or ".jpg" or ".jpeg"):
            file_name, file_end = os.path.splitext(items)
            try:
                image = Image.open(items)
                image.save(file_name+".png")
                print(f"{file_name+file_end} conversion to PNG success!")
            except OSError:
                print(f"\n{file_name+file_end} conversion to PNG unsuccessful :(")
                print(f"Error: Could not be decoded - {file_name+file_end} could be malicious!")
        elif items.endswith(".png"):
            print("It is already in the PNG format!")
    for i in os.listdir(path):
        print(i)


dir_path = "/home/krishna/Documents/Github/MAGIST-Algorithm/src/Data/robot"
image_checker(dir_path)