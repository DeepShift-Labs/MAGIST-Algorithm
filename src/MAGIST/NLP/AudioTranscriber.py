"""This has classes to process audio files and microphone data and transcribe them.

This main class uses the Google Speech API to transcribe audio files. It contains 2 main functions for microphone and
audio file processing respectively.
"""

import speech_recognition as sr
import time
import pathlib

from ..Utils.LogMaster.log_init import MainLogger

class GoogleAudioTranscriber():
	"""Google Audio Transcriber Class."""

	def __init__(self, config):
		"""Initialize the Google Audio Transcriber and Microphone object.

		:param config: The config file(config.json).
		"""

		self.log = MainLogger(config).StandardLogger("GoogleAudioTranscriber")
		self.r = sr.Recognizer()
		self.m = sr.Microphone()

		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("GoogleAudioTranscriber")  # Create a script specific logging instance

		self.log.info("GoogleAudioTranscriber Recognizer Initialized Successfully")

	def microphone_listener(self):
		"""Listen to the microphone and transcribe the audio.

		:return: The transcription of the audio as a string.
		"""

		with self.m as source:
			self.log.info("GoogleAudioTranscriber Listening...")
			audio = self.r.listen(source)
			self.log.info("GoogleAudioTranscriber Listening Complete")
			try:
				start = time.time()
				transcription = self.r.recognize_google(audio)
				self.log.info("Transcribed Prediction: " + transcription)
				end = time.time()
			except sr.UnknownValueError:
				self.log.warning("Google could not understand audio")

			self.log.info("Time taken: " + str(end - start))
		return transcription

	def file_transcriber(self, file):
		"""Transcribe an audio file.

		:param file: The file to be transcribed.

		:return: The transcription of the audio as a string.
		"""
		file = pathlib.Path(file)
		file = file.resolve()  # Find absolute path from a relative one.
		file = str(file)

		audio = sr.AudioFile(file)

		with audio as source:
			self.log.info("GoogleAudioTranscriber Processing...")
			audio = self.r.record(source)
			self.log.info("GoogleAudioTranscriber Processing Complete")
			try:
				start = time.time()
				transcription = self.r.recognize_google(audio)
				self.log.info("Transcribed Prediction: " + transcription)
				end = time.time()
			except sr.UnknownValueError:
				self.log.warning("Google could not understand audio")

			self.log.info("Time taken: " + str(end - start))

		return transcription


