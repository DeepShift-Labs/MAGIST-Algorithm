import tensorflow as tf
import numpy as np



def format_data(in_text):
	in_ds = [[""]]
	punctuation = [".", ",", ";", ":", "!", "?", "\"", "'", "`", "~", "`", "´", "’", "‘", "“", "”", "„", "‟", "‹", "›",
	               "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„",
	               "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’",
	               "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹",
	               "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›",
	               "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„",
	               "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’"]

	def remove_puctuation(text):
		for i in punctuation:
			text = text.replace(i, "")
		return text

	in_ds[0][0] = remove_puctuation(in_text[0][0])
	split_ds = in_ds[0][0].split(" ")

	out = []
	for s in split_ds:
		s = [s]
		out.append(s)

	return out






threshold = 3
max_features = 5000
max_len = 100

input_data = [["""Hi I'm Colin Patel, a British shed inventor and video maker. My aim is to make cool and crazy contraptions and share them with the world to perhaps inspire YOU to get on and make something.
To find out about my inventions and other contraptions visit the Projects page, here you will find photos, information and the videos. If you're new to all things Furze then just have a browse and enjoy."""]]
in_ds = format_data(input_data)

print(in_ds)

vectorize_layer = tf.keras.layers.TextVectorization(
	max_tokens=max_features,
	output_mode='int',
	output_sequence_length=max_len)

vectorize_layer.adapt(in_ds)

model = tf.keras.models.Sequential()

model.add(tf.keras.Input(shape=(1,), dtype=tf.string))

model.add(vectorize_layer)


# input_data = [["He has been found guilty thus he will go to jail"]]


out = model.predict(input_data)
vectored = out
out = np.array(out).astype(np.int64)


out = np.squeeze(out)
in_len = len(out)
out = np.reshape(out, (1, len(out)))

embedding = tf.keras.layers.Embedding(max_features, max_len)
embed = embedding(out)
embed = np.array(embed)


#+-------------------------------------------------------+

def SelfAttention(value, query, key, in_len):
	value_mod = tf.keras.models.Sequential()
	value_mod.add(tf.keras.layers.Dense(in_len, use_bias=False))

	key_mod = tf.keras.models.Sequential()
	key_mod.add(tf.keras.layers.Dense(in_len, use_bias=False))

	query_mod = tf.keras.models.Sequential()
	query_mod.add(tf.keras.layers.Dense(in_len, use_bias=False))

	# value = value_mod.predict(value)
	# key = key_mod.predict(key)
	# query = query_mod.predict(query)

	value = np.array(value).astype(np.float64)
	key = np.array(key).astype(np.float64)
	query = np.array(query).astype(np.float64)

	value = np.squeeze(value)
	key = np.squeeze(key)
	query = np.squeeze(query)

	val_mag = np.sqrt(np.dot(value, value))
	key_mag = np.sqrt(np.dot(key, key))
	query_mag = np.sqrt(np.dot(query, query))

	matmul = key_mag * query_mag
	theta = np.dot(value, query) / matmul

	theta = np.arccos(theta)

	softmax = 1/((np.e)**(-theta)+1)

	out = softmax * value

	return out

	# print(out)

out_arr = []


for i in range(100):
	out_arr.append(SelfAttention(out, out, out, in_len))


def average_of_array(array):
	sum = np.zeros(len(array[0]))
	for i in array:
		sum = np.add(sum, i)
	return np.divide(sum, len(array))

out_fin = average_of_array(out_arr)

threshold = 0
for b in out_fin:
	if b != 0:
		threshold += b
threshold = threshold/len(out_fin)

threshold += threshold + 2

for i in range(len(out_fin)):
	stat = ""
	if out_fin[i] > threshold:
		stat = "Good"
	elif out_fin[i] == threshold:
		stat = "Meh"
	elif out_fin[i] < threshold:
		stat = "Not"
	print(f"{out_fin[i]:.2f}, {vectorize_layer.get_vocabulary()[vectored[0][i]]}, {stat}")


