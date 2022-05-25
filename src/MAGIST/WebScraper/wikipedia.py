import wikipedia

from ..LogMaster.log_init import MainLogger

class WikipediaScraper:
	def __init__(self, config):
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("GoogleScraper")

	def get_summary(self, keyword):
		result = wikipedia.search(keyword)
		for r in result:
			try:
				page = wikipedia.page(r, auto_suggest=False, redirect=False)
				summary = page.summary
				break
			except:
				pass
		return summary

	def get_title(self, keyword):
		result = wikipedia.search(keyword)
		for r in result:
			try:
				page = wikipedia.page(r, auto_suggest=False, redirect=False)
				title = page.title
				break
			except:
				pass
		return title
