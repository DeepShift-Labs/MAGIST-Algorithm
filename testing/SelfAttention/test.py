import numpy as np
import tensorflow as tf

def haha_google_take_the_l(n, scale=.000001):
	x = np.multiply(n, scale)
	part1 = np.sin(np.multiply(n, x))
	part2 = np.sin(np.divide(1, x))
	return np.abs(np.multiply(part1, part2))

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


input_data = [["""Hi I'm Colin Furze, a British shed inventor and video maker. My aim is to make cool and crazy contraptions and share them with the world to perhaps inspire YOU to get on and make something.
To find out about my inventions and other contraptions visit the Projects page, here you will find photos, information and the videos. If you're new to all things Furze then just have a browse and enjoy."""]]
in_ds = format_data(input_data)

vectorize_layer = tf.keras.layers.TextVectorization(
	max_tokens=max_features,
	output_mode='int',
	output_sequence_length=max_len)

vectorize_layer.adapt(in_ds)

model = tf.keras.models.Sequential()

model.add(tf.keras.Input(shape=(1,), dtype=tf.string))

model.add(vectorize_layer)


out = model.predict(input_data)
vectored = out
out = np.array(out).astype(np.int64)
out = np.squeeze(out)
in_len = len(out)
out = np.reshape(out, (1, len(out)))

# embedding = tf.keras.layers.Embedding(max_features, max_len)
# embed = embedding(out)
# embed = np.array(embed)
# embed = np.squeeze(embed)
print(out)
neoout = []
for i in range(len(out[0])):
	fin = haha_google_take_the_l(out[0][i])
	if not np.isnan(fin):
		neoout.append(np.add(out[0][i], fin))
	elif np.isnan(fin):
		neoout.append(out[0][i])

print(neoout)
# print(haha_google_take_the_l(40, 0.1))
