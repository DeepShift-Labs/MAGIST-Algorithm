import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from google_images_search import GoogleImagesSearch
from tqdm import tqdm




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

gis = GoogleImagesSearch('AIzaSyD8imJeBtrVtSJdpFuUgdMQ_oRsbFigc1k', 'd768e8d28e79fb322', progressbar_fn=my_progressbar)

def reverse_image_search(image):
    filePath = image
    searchUrl = 'http://www.google.com/searchbyimage/upload'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}

    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']

    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox") # linux only
    options.add_argument("--headless")
    options.headless = True # also works
    nav = webdriver.Firefox(options=options)
    nav.get(fetchUrl)

    soup = BeautifulSoup(nav.page_source, 'html.parser')
    link = soup.find_all("a", {"class": "fKDtNb"})[0]
    link = str(link)
    start = link.find(">") + len(">")
    end = link.find("</")
    substring = link[start:end]
    print(f"FOUND: {substring}")
    return substring

def download_dataset(keyword, quantity, download_location):
    _search_params = {
        'q': keyword,
        'num': quantity,
        #'fileType': 'jpg',
        #'rights': 'cc_nonderived',
        #'safe': 'medium',  ##
        'imgType': 'photo',  ##
        'imgSize': 'imgSizeUndefined',  ##
        'imgDominantColor': 'imgDominantColorUndefined',
        ##
        'imgColorType': 'imgColorTypeUndefined'  ##
    }

    gis.search(search_params=_search_params, path_to_dir=download_location)