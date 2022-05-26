"""Provides basic functions for Google Reverse Image Search and scraping.

GoogleScraper is the main class containing 2 functions: reverse_image_search and download_raw_img_dataset. The function
reverse_image_search takes a given image path and uses a Google API as well as some scraping to find the name of the
object. The function download_raw_img_dataset takes a given keyword and downloads a given quantity of images from Google
images.
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from google_images_search import GoogleImagesSearch
from tqdm import tqdm
import pathlib

from ..LogMaster.log_init import MainLogger


class GoogleScraper:
	"""Main Google Images scraping and downloading tool."""

	def __init__(self, config, dev_api_key, project_cx_id):
		"""Initializes the class and authenticates Google Search API with credentials and parses config file. It also
		initializes the logger.

		:param config: A relative or absolute path to master config JSON file.
		:param dev_api_key: API key acquired from Google Search API webpage.
		:param project_cx_id: The Search Engine ID provided by Google per Google Developer Project.

		Note: The CX ID is hard to find. To find it, first go to: http://www.google.com/cse/manage/all. Select your
		project and the ID will be called: "Search engine ID". Go to this StackOverflow question and PyPi Post for more
		info: https://stackoverflow.com/questions/6562125/getting-a-cx-id-for-custom-search-google-api-python &
		https://pypi.org/project/Google-Images-Search/
		"""

		def my_progressbar(url, progress):
			"""Defines custom progressbar to visualize the download process for the image downloader.

			:param url: The URL from which the downloader is currently downloading the image from.
			:param progress: The percentage of progress in downloading the file.
			:return: None
			"""
			t = tqdm(total=100, desc=url)
			t.update(progress)

		# try:
		#     if(progress == 1):
		#         t = tqdm(total=100, desc=url)
		#     else:
		#         t.update(progress)
		# except:
		#     pass

		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("GoogleScraper")  # Create a script specific logging instance

		self.gis = GoogleImagesSearch(dev_api_key, project_cx_id, progressbar_fn=my_progressbar)  # Authenticate Google
		# Image Search
		self.log.info("Google Image Search initialized and authorized successfully.")

	def reverse_image_search(self, image_path):
		"""Takes a given image path and finds the object name using Google Reverse Image Search and scraping.

		:param image_path: Relative or absolute image path.
		:return: Object name(String)
		"""
		filePath = image_path

		filePath = pathlib.Path(filePath)
		filePath = filePath.resolve() # Find the absolute path from relative one.
		filePath = str(filePath)

		searchUrl = 'http://www.google.com/searchbyimage/upload'
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}  # Change header to ensure that Google Search still functions
		multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}

		response = requests.post(searchUrl, files=multipart, allow_redirects=False)
		fetchUrl = response.headers['Location']

		options = Options()
		options.add_argument("--disable-extensions")
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")  # linux only
		options.add_argument("--headless")
		options.headless = True  # also works
		nav = webdriver.Firefox(options=options)
		nav.get(fetchUrl)
		self.log.info("Selenium reverse search complete.")

		soup = BeautifulSoup(nav.page_source, 'html.parser')
		link = soup.find_all("a", {"class": "fKDtNb"})[0]
		link = str(link)
		start = link.find(">") + len(">")
		end = link.find("</")
		substring = link[start:end]
		self.log.info("Web scraping complete.")
		self.log.info(f"Found '{substring}' class in input image.")
		return substring

	def download_raw_img_dataset(self, keyword, quantity, download_location):
		"""Takes a keyword and downloads images of that object from Google Images.

		:param keyword: Any object name(noun) passed as a String. There is no validation here.
		:param quantity: The number of images the user requires as an integer.
		:param download_location: Path the user wants to download the images into. This can be relative or absolute.
		:return: True if succeeded.
		"""

		_search_params = {
			'q': keyword,
			'num': quantity,
			# 'fileType': 'jpg',
			# 'rights': 'cc_nonderived',
			# 'safe': 'medium',  ##
			'imgType': 'photo',  ##
			'imgSize': 'imgSizeUndefined',  ##
			'imgDominantColor': 'imgDominantColorUndefined',
			##
			'imgColorType': 'imgColorTypeUndefined'  ##
		}

		filePath = pathlib.Path(download_location)
		filePath = filePath.resolve() # Find the absolute path from relative one.
		filePath = str(filePath)

		self.log.info(f"Initiating Google Image Search for key term: {keyword}.")
		self.gis.search(search_params=_search_params, path_to_dir=download_location) # Search and download images. Note:
		# This function hangs for a while after completion but still exits eventually.
		self.log.info(f"Successfully downloaded {quantity} images to {filePath}.")

		return True
