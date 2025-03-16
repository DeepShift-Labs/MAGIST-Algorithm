import os

import numpy
import tensorflow as tf
import tensorflow_addons as tfa
print("TensorFlow version:", tf.__version__)

from tensorflow.keras.layers import Dense, Flatten, Conv2D
import pathlib

# tf.compat.v1.disable_eager_execution()
AUTOTUNE = tf.data.AUTOTUNE

dirs = os.listdir(str(pathlib.Path("Data").resolve()))


train_ds_arr = []
print(dirs)


BATCH_SIZE = 32

class SiameseNet(tf.keras.models.Model):
    def __init__(self):
        super(SiameseNet, self).__init__()
        self.conv1 = Conv2D(64, 3, activation='relu')
        self.conv2 = Conv2D(32, 3, activation='relu')
        self.conv3 = Conv2D(64, 3, activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        self.d2 = Dense(64, activation='relu')
        self.d3 = Dense(32, )

    def call(self, x1, x2):
        # x1 = self.conv1(x1)
        # x1 = self.conv2(x1)
        x1 = self.conv3(x1)
        x1 = self.flatten(x1)
        x1 = self.d1(x1)
        x1 = self.d2(x1)
        x1 = self.d3(x1)

        # x2 = self.conv1(x2)
        # x2 = self.conv2(x2)
        x2 = self.conv3(x2)
        x2 = self.flatten(x2)
        x2 = self.d1(x2)
        x2 = self.d2(x2)
        x2 = self.d3(x2)
        return x1, x2

snn = SiameseNet()
optimizer = tf.keras.optimizers.Adam()
# loss = tf.keras.losses.contrastive_loss()

def get_label(file_path):
    # Convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    one_hot = parts[-2] == dirs
    # Integer encode the label
    return tf.argmax(one_hot)

def decode_img(img):
    # Convert the compressed string to a 3D uint8 tensor
    img = tf.io.decode_jpeg(img, channels=3)
    # Resize the image to the desired size
    return tf.image.resize(img, [100, 100])

def process_path(file_path):
    label = get_label(file_path)
    # Load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

for d in dirs:
    data_dir = pathlib.Path(os.path.join("Data", d)).with_suffix('')
    x = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=False)

    x = x.map(process_path, num_parallel_calls=AUTOTUNE)
    train_ds_arr.append(x)

class ContrastiveLoss(tf.keras.losses.Loss):
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin

    def forward(self, x0, x1, y):
        # euclidian distance
        part1 = (1-y) * tf.pow(tf.subtract(x0, x1), 2)
        part2 = y * tf.maximum(0.0, (self.margin-tf.pow(tf.subtract(x0, x1), 2)))
        return part1 + part2

snn.compile(optimizer=optimizer, loss=ContrastiveLoss, metrics=["accuracy"])
lossModel = tfa.losses.ContrastiveLoss()#ContrastiveLoss()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tfa.losses.ContrastiveLoss()

@tf.function
def train():
    for _ in range(10):
        for (img1, label1), (img2, label2) in zip(train_ds_arr[0].take(BATCH_SIZE), train_ds_arr[1].take(BATCH_SIZE)):
            img1 = tf.expand_dims(img1, axis=0) / 255.0
            img2 = tf.expand_dims(img2, axis=0) / 255.0
            with tf.GradientTape() as tape:
                predictions = snn(img1, img2, training=True)
                loss = lossModel(predictions[0], predictions[1], 1)
            gradients = tape.gradient(loss, snn.trainable_variables)
            optimizer.apply_gradients(zip(gradients, snn.trainable_variables))

            # train_loss(loss)
            print(loss)


train()