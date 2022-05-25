import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from google_images_search import GoogleImagesSearch
from tqdm import tqdm
import pathlib

from ..LogMaster.log_init import MainLogger


class GoogleScraper:
	def __init__(self, config, dev_api_key, project_cx_id):
		def my_progressbar(url, progress):
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
		self.log = root_log.StandardLogger("GoogleScraper")

		self.gis = GoogleImagesSearch(dev_api_key, project_cx_id, progressbar_fn=my_progressbar)
		self.log.info("Google Image Search Initialized and Authorized Successfully")

	def reverse_image_search(self, image_path):
		filePath = image_path

		filePath = pathlib.Path(filePath)
		filePath = filePath.resolve()
		filePath = str(filePath)

		searchUrl = 'http://www.google.com/searchbyimage/upload'
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
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

		soup = BeautifulSoup(nav.page_source, 'html.parser')
		link = soup.find_all("a", {"class": "fKDtNb"})[0]
		link = str(link)
		start = link.find(">") + len(">")
		end = link.find("</")
		substring = link[start:end]
		self.log.info("Selenium Reverse Search Complete")
		self.log.info(f"Found '{substring}' class in input image")
		return substring

	def download_raw_img_dataset(self, keyword, quantity, download_location):
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
		filePath = filePath.resolve()
		filePath = str(filePath)

		self.log.info(f"Initiating Google Image Search for key term: {keyword}")
		self.gis.search(search_params=_search_params, path_to_dir=download_location)
		self.log.info(f"Successfully downloaded {quantity} images to {filePath}")
