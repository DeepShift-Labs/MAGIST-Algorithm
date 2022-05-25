import wikipedia

from ..LogMaster.log_init import MainLogger

class WikipediaScraper:
	def __init__(self, config):
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("GoogleScraper")

	def get_summary(self, keyword):
		result = wikipedia.search(keyword)
		self.log.info("Wikipedia keyword search successful")
		for r in result:
			try:
				page = wikipedia.page(r, auto_suggest=False, redirect=False)
				summary = page.summary
				break
			except:
				self.log.warning("Wikipedia search retreival failed! Retrying with different search result...")
				pass
		return summary

	def get_title(self, keyword):
		result = wikipedia.search(keyword)
		self.log.info("Wikipedia keyword search successful")
		for r in result:
			try:
				page = wikipedia.page(r, auto_suggest=False, redirect=False)
				title = page.title
				break
			except:
				self.log.warning("Wikipedia search retreival failed! Retrying with different search result...")
				pass
		return title
