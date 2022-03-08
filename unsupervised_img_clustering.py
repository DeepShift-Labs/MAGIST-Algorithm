from PIL import Image
import numpy as np
from tqdm import tqdm
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
from skimage.color import rgb2gray, rgb2hsv, hsv2rgb
from skimage.io import imread, imshow
from sklearn.cluster import KMeans


img = imread('Initial_Img/a/frame1.jpg')
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(img)

def image_to_pandas(image):
    df = pd.DataFrame([image[:,:,0].flatten(),
                       image[:,:,1].flatten(),
                       image[:,:,2].flatten()]).T
    df.columns = ['Red_Channel','Green_Channel','Blue_Channel']
    return df
df_img = image_to_pandas(img)

print(df_img.head())

kmeans = KMeans(n_clusters=3, random_state=0).fit(df_img)
print(kmeans.labels_)

result = kmeans.labels_.reshape(img.shape[0],img.shape[1])
imshow(result, cmap='viridis')
plt.show()

fig, axes = plt.subplots(1,3, figsize=(15, 12))
for n, ax in enumerate(axes.flatten()):
    img2 = imread('Initial_Img/a/frame1.jpg')
    img2[:, :, 0] = img2[:, :, 0]*(result==[n])
    img2[:, :, 1] = img2[:, :, 1]*(result==[n])
    img2[:, :, 2] = img2[:, :, 2]*(result==[n])
    ax.imshow(img2);
    ax.set_axis_off()
fig.tight_layout()

plt.show()