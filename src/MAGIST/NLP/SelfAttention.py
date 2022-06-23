"""Contains all necessary functions to train and use unsupervised text prioritization.

This class has numerous functions to run the text prioritization algorithm. You can simply call the class instance to
run the entire algorithm.
"""


import tensorflow as tf
import numpy as np
from ..Utils.LogMaster.log_init import MainLogger

class TextPreprocessing():
	def __init__(self, config):
		"""Initializes the TextPreprocessing class and config.

		:param config: The config file containing all necessary parameters(config.json).
		"""
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("TextPreprocessing")  # Create a script specific logging instance

	def __format_data(self, in_text):
		"""Formats the input text to be compatible with the model.

		:param in_text: The text(string) to be formatted.

		:return: The formatted text.
		"""
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
		def __remove_puctuation(text):
			"""Removes punctuation from the text.

			:param text: The text to be formatted.

			:return: The formatted text.
			"""
			for i in punctuation:
				text = text.replace(i, "")
			return text

		def __lowercase(text):
			"""Converts the text to lowercase.

			:param text: The text to be formatted.

			:return: The formatted text.
			"""
			return text.lower()

		in_text = __remove_puctuation(in_text)
		in_text = __lowercase(in_text)
		return in_text

	def __tokenize(self, input_text):
		"""Splits the input text into tokens.

		:param input_text: The text to be split.

		:return: The tokens.
		"""
		input_text = self.__format_data(input_text)
		return input_text.split(" ")

	def split_positional_encodings(self, input_text):
		"""Splits the input text into positional encodings.

		:param input_text: The text to be split.

		:return: The positional encodings.
		"""
		input_text = self.__format_data(input_text)
		split_text = self.__tokenize(input_text)

		position_dict = []
		count = 1
		for s in split_text:
			position_dict.append([count, s])
			count += 1

		return position_dict

	def vectorize_text(self, raw_input_text):
		"""Vectorizes the input text.

		:param raw_input_text: The text to be vectorized.

		:return: The vectorized text.
		"""
		input_text = self.__format_data(raw_input_text)
		self.vectorize_layer = tf.keras.layers.TextVectorization()
		self.vectorize_layer.adapt([raw_input_text])
		vec = self.vectorize_layer(raw_input_text)

		return np.array(vec)

	def __positional_embedding_function(self, n, scale=0.1, scalar=1):
		"""Computes the positional embedding.

		:param n: The position to be computed.
		:param scale: The scale of the positional embedding function.
		:param scalar: The scalar multiplier to the output of the positional embedding.

		:return: The positional embedding.
		"""
		x = np.multiply(n, scale)
		part1 = np.sin(np.multiply(n, x))
		part2 = np.sin(np.divide(1, x))
		return np.multiply(np.abs(np.multiply(part1, part2)), scalar)

	def positional_embedding(self, split_positional_encodings, vectorized_text, scalar=3):
		"""Computes the positional embedding.

		:param split_positional_encodings: The positional encodings to be computed.
		:param vectorized_text: The vectorized text.
		:param scalar: The scalar multiplier to the output of the positional embedding.

		:return: The positional embedding.
		"""
		position_computed = []
		for i in split_positional_encodings:
			pos = self.__positional_embedding_function(i[0], scalar=scalar)
			position_computed.append(pos)

		final_position_embedding = []

		for i in range(len(position_computed)):
			final_position_embedding.append(int(vectorized_text[i]) + position_computed[i])

		return final_position_embedding

	def SelfAttention(self, value, query, key, in_len):
		"""Computes the self attention.

		:param value: The value to be computed.
		:param query: The query to be computed.
		:param key: The key to be computed.
		:param in_len: The length of the input.

		Note: The value, query, and key must be the same length and are the same thing usually for self-attention.
		"""
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

		softmax = 1 / ((np.e) ** (-theta) + 1)

		out = softmax * value

		return out

	def compute_theshold(self, attention_weights):
		"""Computes the threshold for relevant and irrelevant text.

		:param attention_weights: The attention weights to be computed.

		:return: The threshold(int).
		"""
		threshold = 0
		for b in attention_weights:
			if b != 0:
				threshold += b
		return threshold / len(attention_weights)

	def print_results(self, attention_weights, threshold, vectorized_text, show_only_important=False):
		"""Prints the results.
		"""
		for i in range(len(attention_weights)):
			stat = ""
			if attention_weights[i] > threshold:
				stat = "Good"
			elif attention_weights[i] == threshold:
				stat = "Meh"
			elif attention_weights[i] < threshold:
				stat = "Not"
			if show_only_important:
				if attention_weights[i] >= threshold:
					self.log.info(f"{attention_weights[i]:.2f}, {self.vectorize_layer.get_vocabulary()[vectorized_text[i]]}, {stat}")
			else:
				self.log.info(
					f"{attention_weights[i]:.2f}, {self.vectorize_layer.get_vocabulary()[vectorized_text[i]]}, {stat}")

	def __call__(self, input_text):
		"""Computes everything and returns the importance matrix.

		:param input_text: The text to be computed.

		:return: The simplified importance matrix.
		"""
		s = self.split_positional_encodings(input_text)
		vec = self.vectorize_text(input_text)

		out_fin = self.positional_embedding(s, vec)

		attention_weights = self.SelfAttention(out_fin, out_fin, out_fin, len(out_fin))
		threshold = self.compute_theshold(attention_weights)

		final_output_array = []

		for i in range(len(attention_weights)):
			stat = ""
			if attention_weights[i] > threshold:
				stat = "Good"
			elif attention_weights[i] == threshold:
				stat = "Meh"
			elif attention_weights[i] < threshold:
				stat = "Not"

			final_output_array.append([attention_weights[i], self.vectorize_layer.get_vocabulary()[vec[i]], stat])

		return final_output_array
