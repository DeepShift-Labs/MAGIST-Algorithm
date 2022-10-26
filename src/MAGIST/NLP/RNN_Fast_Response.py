from MAGIST.NeuralDB.MongoUtils import AdminUtils
from MAGIST.NeuralDB.PrimaryNeuralDB import NeuralDB


mongo_admin = AdminUtils("config/config.json")
client = mongo_admin.initialize_neuraldb()
neural_db = NeuralDB("config/config.json", client)

neural_db.recreate_db()


neural_db.search_entire_db("")