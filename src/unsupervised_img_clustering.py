import pandas as pd

import matplotlib.pyplot as plt
from skimage.io import imread, imshow, imsave
from skimage.transform import resize
from sklearn.cluster import KMeans
from skimage.util import img_as_uint
import search

def image_to_pandas(image):
    df = pd.DataFrame([image[:,:,0].flatten(),
                       image[:,:,1].flatten(),
                       image[:,:,2].flatten()]).T
    df.columns = ['Red_Channel','Green_Channel','Blue_Channel']
    return df


def unsupervised_clusters(n_of_clusters, img_location, img_size, masked_img_dir):
    img = imread(img_location)
    img = resize(img, img_size)
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    imshow(img)


    df_img = image_to_pandas(img)

    print(df_img.head())

    kmeans = KMeans(n_clusters=n_of_clusters, random_state=0).fit(df_img)
    print(kmeans.labels_)

    result = kmeans.labels_.reshape(img.shape[0],img.shape[1])
    imshow(result, cmap='viridis')
    plt.show()

    fig, axes = plt.subplots(1,n_of_clusters, figsize=(15, 12))
    for n, ax in enumerate(axes.flatten()):
        img2 = imread(img_location)
        img2 = resize(img2, img_size)
        img2[:, :, 0] = img2[:, :, 0]*(result==[n])
        img2[:, :, 1] = img2[:, :, 1]*(result==[n])
        img2[:, :, 2] = img2[:, :, 2]*(result==[n])
        unit_img = img_as_uint(img2)
        imsave(f'{masked_img_dir}/masked{n}.jpg', unit_img)
        ax.imshow(img2);
        ax.set_axis_off()
    fig.tight_layout()
    plt.show()

# dataset = foz.load_zoo_dataset(
#     "open-images-v6",
#     split="validation",
#     label_types=["segmentations", "classifications"],
#     classes = ["door"],
#     max_samples=100,
#     seed=51,
#     shuffle=True,
#     dataset_name="open-images-food",
# )

# unsupervised_clusters(3, 'test.jpg', (540, 480), "./Masks")
# unsupervised_clusters(2, 'masked2.jpg', (540, 480), ".")
key = search.reverse_image_search('Masks/masked0.jpg')
# os.system(f'mkdir Pics/{key}')
search.download_dataset(key, 15, f'Pics/{key}')
