import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test_database"]

users = mydb["users"]

# sample_data = {"name" : "John", "age" : 30}
#
# users.insert_one(sample_data)
#
# sample_data = {"name" : "Billy", "age" : 46}
#
# users.insert_one(sample_data)

users.update_many({"age": {"$gt": 100}}, {"$set": {"age": 49}})