import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt



def format_data(in_text): # remove punctuation and lowercase
	punctuation = [".", ",", ";", ":", "!", "?", "\"", "'", "`", "~", "`", "´", "’", "‘", "“", "”", "„", "‟", "‹", "›",
	               "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”",
	               "„",
	               "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘",
	               "’",
	               "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»",
	               "‹",
	               "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹",
	               "›",
	               "«", "»", "‹", "›", "‘", "’", "“", "”", "„", "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’", "“", "”",
	               "„",
	               "‟", "‹", "›", "«", "»", "‹", "›", "‘", "’"]
	def remove_puctuation(text):
		for i in punctuation:
			text = text.replace(i, "")
		return text

	def lowercase(text):
		return text.lower()

	in_text = remove_puctuation(in_text)
	in_text = lowercase(in_text)
	return in_text


input_text = "I am a student at the University of Texas at Austin and I am extremely boring."

input_text = format_data(input_text)

split_text = input_text.split(" ")

position_dict = []
count = 1
for s in split_text:
	position_dict.append([count, s])
	count += 1



vectorize_layer = tf.keras.layers.TextVectorization()
vectorize_layer.adapt([input_text])
vectored = vectorize_layer(input_text)

def positional_embedding(n, scale=0.1, scalar=1):
	x = np.multiply(n, scale)
	part1 = np.sin(np.multiply(n, x))
	part2 = np.sin(np.divide(1, x))
	return np.multiply(np.abs(np.multiply(part1, part2)), scalar)

position_computed = []
for i in position_dict:
	pos = positional_embedding(i[0], scalar=3)
	position_computed.append(pos)

final_position_embedding = []

for i in range(len(position_computed)):
	final_position_embedding.append(int(vectored[i]) + position_computed[i])





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

	# theta = np.arccos(theta)

	softmax = 1/((np.e)**(-theta)+1)

	out = softmax * value

	return out



out_fin = SelfAttention(final_position_embedding, final_position_embedding, final_position_embedding, len(final_position_embedding))


threshold = 0
for b in out_fin:
	if b != 0:
		threshold += b
threshold = threshold/len(out_fin)



for i in range(len(out_fin)):
	stat = ""
	if out_fin[i] > threshold:
		stat = "Good"
	elif out_fin[i] == threshold:
		stat = "Meh"
	elif out_fin[i] < threshold:
		stat = "Not"
	if out_fin[i] >= threshold:
		print(f"{out_fin[i]:.2f}, {vectorize_layer.get_vocabulary()[vectored[i]]}, {stat}")