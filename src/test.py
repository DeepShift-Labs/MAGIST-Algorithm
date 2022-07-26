from MAGIST.NeuralDB.MongoUtils import AdminUtils
from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB

a = AdminUtils("config.json")
client = a.initialize_neuraldb()

neural_db = NeuralDB("config.json", client)
neural_db.recreate_db()

a = neural_db.search_entire_db("blah")

print(a)

//testing123
