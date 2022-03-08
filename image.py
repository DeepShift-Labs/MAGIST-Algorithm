from google_images_search import GoogleImagesSearch

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch('AIzaSyD8imJeBtrVtSJdpFuUgdMQ_oRsbFigc1k', 'd768e8d28e79fb322')

# define search params
# option for commonly used search param are shown below for easy reference.
# For param marked with '##':
#   - Multiselect is currently not feasible. Choose ONE option only
#   - This param can also be omitted from _search_params if you do not wish to define any value
_search_params = {
    'q': 'snake',
    'num': 10,
    'fileType': 'jpg',
    #'rights': 'cc_nonderived',
    'safe': 'medium',  ##
    'imgType': 'photo',  ##
    'imgSize': 'imgSizeUndefined',  ##
    'imgDominantColor': 'imgDominantColorUndefined',
    ##
    'imgColorType': 'imgColorTypeUndefined'  ##
}

# this will only search for images:
# gis.search(search_params=_search_params)
print("6666666666666")
# this will search and download:
gis.search(search_params=_search_params, path_to_dir='Initial_Img/')

# this will search, download and resize:
# gis.search(search_params=_search_params, path_to_dir='/path/', width=500, height=500)

# search first, then download and resize afterwards:
# gis.search(search_params=_search_params)
print("174729347")
for image in gis.results():
    print(image.url)  # image direct url
    print(image.referrer_url)  # image referrer url (source)

    image.download('Initial_Img/')  # download image
    image.resize(500, 500)  # resize downloaded image

    print(image.path)  # downloaded local file path