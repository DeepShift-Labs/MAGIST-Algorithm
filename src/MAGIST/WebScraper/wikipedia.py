"""Provides basic functions for Wikipedia scraping.

WikipediaScraper is the main class containing 1 main function called get_summary. This function, given a keyword, will
search Wikipedia for several results, select the best one, and extract the summary section. There is am additional
function called get_title which grabs the exact title, but is relatively unnecessary.
"""

import wikipedia
from ..LogMaster.log_init import MainLogger


class WikipediaScraper:
	"""Main Wikipedia scraping tool."""

	def __init__(self, config):
		"""Initialize the class and logger module.

		:param config: A relative or absolute path to master config JSON file.
		"""
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("WikipediaScraper")  # Create a script specific logging instance

	def get_summary(self, keyword):
		"""Get summary of Wikipedia post given a keyword.

		:param keyword: Keyword of anything given as a String.
		:return: The summary of the Wikipedia post as a String
		"""
		result = wikipedia.search(keyword) # Get all search results from the keyword.
		self.log.info("Wikipedia keyword search successful.")
		for r in result: # Iterate through each result.
			try: # See is we can aquire the summary.
				page = wikipedia.page(r, auto_suggest=False, redirect=False) # Aquire the summary. Auto-suggestions
				# and redirects bring in wrong results so they are disabled.
				summary = page.summary
				break
			except: # If the scraping fails, skip it and use the next best result.
				self.log.warning("Wikipedia search retreival failed! Retrying with different search result...")
				pass
		return summary

	def get_title(self, keyword):
		"""Get title of Wikipedia post given a keyword.

		:param keyword: Keyword of anything given as a String.
		:return: The title of the Wikipedia post as a String
		"""
		result = wikipedia.search(keyword) # Get all search results from the keyword.
		self.log.info("Wikipedia keyword search successful.")
		for r in result: # Iterate through each result.
			try:
				page = wikipedia.page(r, auto_suggest=False, redirect=False) # Aquire the summary. Auto-suggestions
				# and redirects bring in wrong results so they are disabled.
				title = page.title
				break
			except: # If the scraping fails, skip it and use the next best result.
				self.log.warning("Wikipedia search retrieval failed! Retrying with different search result...")
				pass
		return title
