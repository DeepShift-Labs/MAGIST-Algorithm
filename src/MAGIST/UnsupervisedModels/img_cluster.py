import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread, imshow, imsave
from skimage.transform import resize
from sklearn.cluster import KMeans
from skimage.util import img_as_uint
from ..LogMaster.log_init import MainLogger
import pathlib, json


class RoughCluster():
    def __init__(self, config):
        """Initialize the class, logger module and parse config.json.

        :param config: A relative or absolute path to master config JSON file.
        """
        root_log = MainLogger(config)
        self.log = root_log.StandardLogger("UnsupervisedClustering")  # Create a script specific logging instance

        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
        f = open(config)
        config = json.load(f)

        for i in config['basic_variables']:
            try:
                self.matplot = i["enable_matplot_display"]
            except:
                pass

    def unsupervised_clusters(self, n_of_clusters, img_location, img_size, masked_img_dir):
        """Make, color, and crop unsupervised clusters.

        :param n_of_clusters: Number of expected objects.
        :param img_location: Location of input image.
        :param img_size: Resized shape of the image in pixels. This is represented as a tuple (length, height). Note:
        This is NOT the current size of the image(it can be though), but rather the size it will be scaled down to for
        efficient processing.
        :param masked_img_dir: Location of the exported image directories.
        :return: None
        """
        def image_to_pandas(image):
            """

            :param image: Location of input image.
            :return: Pandas Dataframe consisting of the image.
            """
            df = pd.DataFrame([image[:, :, 0].flatten(),
                               image[:, :, 1].flatten(),
                               image[:, :, 2].flatten()]).T
            df.columns = ['Red_Channel', 'Green_Channel', 'Blue_Channel']
            return df

        img_location = pathlib.Path(img_location)
        img_location = img_location.resolve()  # Find the absolute path from relative one.
        img_location = str(img_location)

        masked_img_dir = pathlib.Path(masked_img_dir)
        masked_img_dir = masked_img_dir.resolve()  # Find the absolute path from relative one.
        masked_img_dir = str(masked_img_dir)

        img = imread(img_location)
        img = resize(img, img_size)
        plt.figure(num=None, figsize=(8, 6), dpi=80)
        if(self.matplot):
            imshow(img)

        self.log.info("Input image resized and configured for clustering computation.")

        df_img = image_to_pandas(img)

        kmeans = KMeans(n_clusters=n_of_clusters, random_state=0).fit(df_img)
        self.log.info("Image clustering complete!")

        result = kmeans.labels_.reshape(img.shape[0],img.shape[1])
        if(self.matplot):
            imshow(result, cmap='viridis')
            plt.show()

        fig, axes = plt.subplots(1,n_of_clusters, figsize=(15, 12))
        for n, ax in enumerate(axes.flatten()):
            img2 = imread(img_location)
            img2 = resize(img2, img_size)
            img2[:, :, 0] = img2[:, :, 0]*(result==[n]) # Disabling pixels of certain type
            img2[:, :, 1] = img2[:, :, 1]*(result==[n]) # Disabling pixels of certain type
            img2[:, :, 2] = img2[:, :, 2]*(result==[n]) # Disabling pixels of certain type
            unit_img = img_as_uint(img2)
            imsave(f'{masked_img_dir}/masked{n}.jpg', unit_img)
            ax.imshow(img2);
            ax.set_axis_off()
        fig.tight_layout()
        if(self.matplot):
            plt.show()


# unsupervised_clusters(3, 'test.jpg', (540, 480), "./Masks")
# unsupervised_clusters(2, 'masked2.jpg', (540, 480), ".")
