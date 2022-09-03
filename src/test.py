# from MAGIST.NeuralDB.ElasticSearch import ESDB
#
# esdb = ESDB("config/config.json", "http://192.168.31.188:9200", "config/queries.json", "config/schema.json")
#
#
# esdb.create_index("test_index22", "word_db_schema")

#
# import cv2
# vidcap = cv2.VideoCapture('vid.mp4')
# success,image = vidcap.read()
# count = 0
# while success:
#   cv2.imwrite("inputs/frame%d.jpg" % count, image)     # save frame as JPEG file
#   success,image = vidcap.read()
#   print('Read a new frame: ', success)
#   count += 1


from os import walk

filenames = next(walk("inputs"), (None, None, []))[2]  # [] if no file
print(filenames)