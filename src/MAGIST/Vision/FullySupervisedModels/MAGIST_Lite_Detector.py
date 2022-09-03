"""Contains all necessary functions to train and use the MAGIST Lite Detector.

MAGIST Lite is a fully-supervised model that is trained on a large dataset of images. It contains 2 classes: MAGIST_CNN
and MAGIST_CNN_Predictor.
"""

from ...Utils.LogMaster.log_init import MainLogger
from skimage import transform
import numpy as np
from PIL import Image
from tqdm import tqdm
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout
import tensorflow as tf
import datetime
import json
import os
import pathlib

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class _CNN(tf.keras.models.Model):
    def __init__(self):
        """Initialize the model."""
        super(_CNN, self).__init__()
        self.conv1 = Conv2D(32, (3, 3), activation='relu')
        self.conv2 = Conv2D(64, (3, 3), activation='relu')
        # self.conv3 = Conv2D(128, (3, 3), activation='relu')
        # self.conv4 = Conv2D(64, (3, 3), activation='relu')
        self.conv5 = Conv2D(32, (3, 3), activation='relu')
        self.flat = Flatten()
        self.dense1 = Dense(128, activation='relu')
        self.drop1 = Dropout(0.8)
        self.dense2 = Dense(64, activation='relu')
        self.drop2 = Dropout(0.5)
        self.dense3 = Dense(32, activation='relu')
        self.dense4 = Dense(10, activation='softmax')

    def call(self, x):
        """Forward pass of the model.

        :param x: A batch of images.

        :return: A batch of predictions.
        """
        x = self.conv1(x)
        x = self.conv2(x)
        # x = self.conv3(x)
        # x = self.conv4(x)
        x = self.conv5(x)
        x = self.flat(x)
        x = self.dense1(x)
        x = self.drop1(x)
        x = self.dense2(x)
        x = self.drop2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        return x


class MAGIST_CNN():
    def __init__(self, config):
        """Initializes the model and sets training variables.

        :param config: The configuration file(JSON).
        """
        root_log = MainLogger(config)
        # Create a script specific logging instance
        self.log = root_log.StandardLogger("MAGIST_Lite_CNN")

        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
        f = open(config)
        config = json.load(f)

        for i in config['tf_lite_detector']:
            try:
                self.data_path = i["data_path"]
            except KeyError:
                pass
            try:
                self.TensorBoard_log_dir = i["TensorBoard_log_dir"]
            except KeyError:
                pass
            try:
                self.TF_ckpt_path = i["TF_ckpt_path"]
            except KeyError:
                pass
            try:
                self.input_image_size = i["input_image_size"]
            except KeyError:
                pass
            try:
                self.epochs = i["epochs"]
            except KeyError:
                pass
            try:
                self.batch_size = i["batch_size"]
            except KeyError:
                pass
            try:
                self.seed = i["seed"]
            except KeyError:
                pass
            try:
                self.validation_split = i["validation_split"]
            except KeyError:
                pass
            try:
                self.export_path = i["export_full_model"]
            except KeyError:
                pass
            try:
                self.grayscale = i["grayscale"]
            except KeyError:
                pass

        self.data_path = pathlib.Path(self.data_path)
        # Find absolute path from a relative one.
        self.data_path = self.data_path.resolve()
        self.data_path = str(self.data_path)

        self.TensorBoard_log_dir = pathlib.Path(self.TensorBoard_log_dir)
        # Find absolute path from a relative one.
        self.TensorBoard_log_dir = self.TensorBoard_log_dir.resolve()
        self.TensorBoard_log_dir = str(self.TensorBoard_log_dir)

        self.TF_ckpt_path = pathlib.Path(self.TF_ckpt_path)
        # Find absolute path from a relative one.
        self.TF_ckpt_path = self.TF_ckpt_path.resolve()
        self.TF_ckpt_path = str(self.TF_ckpt_path)

        self.export_path = pathlib.Path(self.export_path)
        # Find absolute path from a relative one.
        self.export_path = self.export_path.resolve()
        self.export_path = str(self.export_path)

        self.epoch_arr = []
        self.train_loss_arr = []
        self.train_accuracy_arr = []
        self.test_loss_arr = []
        self.test_accuracy_arr = []

    def load_data(self):
        """Loads the text_ds from the data_path.

        :return: The train_ds and test_ds.
        """
        if self.grayscale:
            self.train_ds = tf.keras.utils.image_dataset_from_directory(
                self.data_path,
                labels='inferred',
                label_mode='int',
                class_names=None,
                color_mode='grayscale',
                batch_size=self.batch_size,
                image_size=tuple(self.input_image_size),
                shuffle=True,
                seed=self.seed,
                validation_split=self.validation_split,
                subset='training',
                interpolation='bilinear',
                follow_links=False,
                crop_to_aspect_ratio=False,
                # class_mode='sparse'
            )

            self.val_ds = tf.keras.utils.image_dataset_from_directory(
                self.data_path,
                labels='inferred',
                label_mode='int',
                class_names=None,
                color_mode='grayscale',
                batch_size=self.batch_size,
                image_size=tuple(self.input_image_size),
                shuffle=True,
                seed=self.seed,
                validation_split=self.validation_split,
                subset='validation',
                interpolation='bilinear',
                follow_links=False,
                crop_to_aspect_ratio=False,
                # class_mode='sparse'
            )
        else:
            self.train_ds = tf.keras.utils.image_dataset_from_directory(
                self.data_path,
                labels='inferred',
                label_mode='int',
                class_names=None,
                color_mode='rgb',
                batch_size=self.batch_size,
                image_size=tuple(self.input_image_size),
                shuffle=True,
                seed=self.seed,
                validation_split=self.validation_split,
                subset='training',
                interpolation='bilinear',
                follow_links=False,
                crop_to_aspect_ratio=False,
                # class_mode='sparse'
            )

            self.val_ds = tf.keras.utils.image_dataset_from_directory(
                self.data_path,
                labels='inferred',
                label_mode='int',
                class_names=None,
                color_mode='rgb',
                batch_size=self.batch_size,
                image_size=tuple(self.input_image_size),
                shuffle=True,
                seed=self.seed,
                validation_split=self.validation_split,
                subset='validation',
                interpolation='bilinear',
                follow_links=False,
                crop_to_aspect_ratio=False,
                # class_mode='sparse'
            )

        self.log.info("Data loaded and batched")

        return self.train_ds, self.val_ds

    def compile_model(self):
        """Compiles the model.

        :return: The compiled model.
        """
        self.model = _CNN()

        self.loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True)

        self.optimizer = tf.keras.optimizers.Adam()

        self.train_loss = tf.keras.metrics.Mean(name='train_loss')
        self.train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
            name='train_accuracy')

        self.test_loss = tf.keras.metrics.Mean(name='test_loss')
        self.test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
            name='test_accuracy')

        self.log.info("Model optimizer and loss function set and compiled.")

        return self.model

    def callbacks_init(self):
        """Initializes the callbacks.

        :return: The configured callbacks.
        """
        self.current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.train_log_dir = f'{self.TensorBoard_log_dir}/train_logs/gradient_tape/' + self.current_time + '/train'
        self.test_log_dir = f'{self.TensorBoard_log_dir}/train_logs/gradient_tape/' + self.current_time + '/test'
        self.train_summary_writer = tf.summary.create_file_writer(
            self.train_log_dir)
        self.test_summary_writer = tf.summary.create_file_writer(
            self.test_log_dir)

        self.log_dir = f"{self.TensorBoard_log_dir}/tf_histograms/fit/" + \
                       datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.tensorboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir=self.log_dir, histogram_freq=1, update_freq='batch')
        self.tensorboard_callback.set_model(self.model)

        self.callbacks = tf.keras.callbacks.CallbackList(
            [self.tensorboard_callback])

        self.ckpt = tf.train.Checkpoint(
            step=tf.Variable(1),
            optimizer=self.optimizer,
            net=self.model,
            iterator=self.train_ds)
        self.manager = tf.train.CheckpointManager(
            self.ckpt, f'{self.TF_ckpt_path}', max_to_keep=4000)

        self.log.info(
            f"Callbacks initialized. TensorBoard histograms are logged to {self.log_dir}/tf_histograms. "
            f"TensorBoard training text_ds is stored in {self.log_dir}/train_logs/gradient_tape. Checkpoint "
            f"saved to {self.TF_ckpt_path}!")

        self.ckpt.restore(self.manager.latest_checkpoint)
        if self.manager.latest_checkpoint:
            self.log.info(
                "Restored from {}".format(
                    self.manager.latest_checkpoint))
        else:
            self.log.info("Initializing from scratch.")

        return self.ckpt, self.manager, self.callbacks

    @tf.function
    def __train_step(self, images, labels):
        with tf.GradientTape() as tape:
            # training=True is only needed if there are layers with different
            # behavior during training versus inference (e.g. Dropout).
            self.predictions = self.model(images, training=True)
            self.loss = self.loss_object(labels, self.predictions)
        self.gradients = tape.gradient(
            self.loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(
            zip(self.gradients, self.model.trainable_variables))

        self.train_loss(self.loss)
        self.train_accuracy(labels, self.predictions)

    @tf.function
    def __test_step(self, images, labels):
        # training=False is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = self.model(images, training=False)
        t_loss = self.loss_object(labels, predictions)

        self.test_loss(t_loss)
        self.test_accuracy(labels, predictions)

    def train(self):
        """Trains the model and exports training data.
        """
        self.callbacks.on_train_begin()
        self.log.info("Training started successfully.")
        for epoch in (pbar_epoch:= tqdm(range(self.epochs), ascii="░▒█")):
            self.callbacks.on_epoch_begin(epoch)
            pbar_epoch.set_description("Epoch Progress: ")
            # Reset the metrics at the start of the next epoch
            self.train_loss.reset_states()
            self.train_accuracy.reset_states()
            self.test_loss.reset_states()
            self.test_accuracy.reset_states()

            for images, labels in (pbar_train:= tqdm(self.train_ds.take(self.batch_size), leave=False, ascii="░▒█")):
                self.callbacks.on_train_batch_begin(images)
                pbar_train.set_description("Train Step: ")
                self.__train_step(images, labels)
                pbar_train.set_postfix(
                    {"loss": float(self.train_loss.result()),
                     "accuracy": float(self.train_accuracy.result()) * 100})
                self.ckpt.step.assign_add(1)
            with self.train_summary_writer.as_default():
                tf.summary.scalar('loss', self.train_loss.result(), step=epoch)
                tf.summary.scalar(
                    'accuracy',
                    self.train_accuracy.result(),
                    step=epoch)

            for test_images, test_labels in (
                    pbar_test:= tqdm(self.val_ds.take(self.batch_size), leave=False, ascii="░▒█")):
                pbar_test.set_description("Test Step: ")
                self.__test_step(test_images, test_labels)
                pbar_test.set_postfix(
                    {"loss": float(self.test_loss.result()),
                     "accuracy": float(self.test_accuracy.result()) * 100})
            with self.test_summary_writer.as_default():
                tf.summary.scalar('loss', self.test_loss.result(), step=epoch)
                tf.summary.scalar(
                    'accuracy',
                    self.test_accuracy.result(),
                    step=epoch)

            if ((int(self.ckpt.step) - 1) % self.batch_size) == 0:
                save_path = self.manager.save()
                self.log.info("Saved checkpoint for step {}: {}".format(
                    int(self.ckpt.step) - 1, save_path))

            self.epoch_arr.append(epoch + 1)
            self.train_loss_arr.append(self.train_loss.result())
            self.train_accuracy_arr.append(self.train_accuracy.result() * 100)
            self.test_loss_arr.append(self.test_loss.result())
            self.test_accuracy_arr.append(self.test_accuracy.result() * 100)

            pbar_epoch.set_postfix(
                {"train_loss": float(self.train_loss.result()),
                 "test_loss": float(self.test_loss.result()),
                 "test_accuracy": float(self.test_accuracy.result()) * 100,
                 "train_accuracy": float(self.train_accuracy.result()) * 100})
            self.callbacks.on_epoch_end(epoch)
        self.callbacks.on_train_end()

        for i in range(len(self.epoch_arr)):
            self.log.info(
                f'Epoch {self.epoch_arr[i]}, '
                f'Loss: {self.train_loss_arr[i]}, '
                f'Accuracy: {self.train_accuracy_arr[i]}, '
                f'Test Loss: {self.test_loss_arr[i]}, '
                f'Test Accuracy: {self.test_accuracy_arr[i]}'
            )

            self.model.save(
                self.export_path,
                save_format="tf",
                include_optimizer=True)
            self.log.info("Model exported to {}.".format(self.export_path))

    def get_class_names(self):
        """Returns the class names.

        :return: List of class names.
        """
        if self.train_ds is None or self.val_ds is None:
            self.log.error(
                "Dataset not loaded! Please load dataset first using 'class.load_data()'.")
            return None
        train_classes = self.train_ds.class_names
        test_classes = self.val_ds.class_names
        if train_classes == test_classes:
            return train_classes
        else:
            self.log.error(
                "Class names do not match between train and test datasets. Please check your text_ds.")
            return None

    def __call__(self):
        """Calls the train method."""
        self.log.info("Automated Trainer --> Loading data...")
        train, test = self.load_data()
        self.log.info("Automated Trainer --> Data loaded successfully.")
        self.log.info("Automated Trainer --> Building model...")
        self.compile_model()
        self.log.info("Automated Trainer --> Model built successfully.")
        self.log.info("Automated Trainer --> Setting up callbacks...")
        self.callbacks_init()
        self.log.info("Automated Trainer --> Callbacks setup successfully.")
        self.log.info("Automated Trainer --> Training model...")
        self.train()
        self.log.info("Automated Trainer --> Training completed successfully.")


class MAGIST_CNN_Predictor():
    def __init__(self, config):
        """Initializes the predictor and config.

        :param config: A dictionary containing the config.json.
        """
        root_log = MainLogger(config)
        # Create a script specific logging instance
        self.log = root_log.StandardLogger("MAGIST_Lite_Predictor")

        config = pathlib.Path(config)
        config = config.resolve()  # Find absolute path from a relative one.
        f = open(config)
        config = json.load(f)

        for i in config['tf_lite_detector']:
            try:
                self.TF_ckpt_path = i["TF_ckpt_path"]
            except KeyError:
                pass
            try:
                self.export_path = i["export_full_model"]
            except KeyError:
                pass
            try:
                self.input_image_size = i["input_image_size"]
            except KeyError:
                pass
            try:
                self.grayscale = i["grayscale"]
            except KeyError:
                pass

        self.export_path = pathlib.Path(self.export_path)
        # Find absolute path from a relative one.
        self.export_path = self.export_path.resolve()
        self.export_path = str(self.export_path)

        self.TF_ckpt_path = pathlib.Path(self.TF_ckpt_path)
        # Find absolute path from a relative one.
        self.TF_ckpt_path = self.TF_ckpt_path.resolve()
        self.TF_ckpt_path = str(self.TF_ckpt_path)

        self.imported = tf.keras.models.load_model(
            self.export_path, compile=False)
        self.log.info("Model imported from {}.".format(self.export_path))

        # latest = tf.train.latest_checkpoint(self.TF_ckpt_path)

        # self.imported.load_weights(latest)
        self.imported.summary()

    def __load(self, filename):
        """Loads a file from the given filename.

        :param filename: The filename to load.

        :return: The loaded image file as np.array.
        """
        np_image = Image.open(filename)
        np_image = np.array(np_image).astype('float32') / 255
        if self.grayscale:
            np_image = transform.resize(
                np_image, (self.input_image_size[0], self.input_image_size[1], 1))
        else:
            np_image = transform.resize(
                np_image, (self.input_image_size[0], self.input_image_size[1], 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    def img_prediction(self, img_path):
        """Predicts the class of the given image.

        :param img_path: The path to the image.

        :return: The softmax array of predictions and the id of the prediction from class names.
        """
        img_path = pathlib.Path(img_path)
        # Find absolute path from a relative one.
        img_path = img_path.resolve()
        img_path = str(img_path)

        image = self.__load(img_path)
        p = self.imported.predict(image)

        p_id = np.array(p)
        p_id = np.squeeze(p)
        max = p_id.max()
        id = np.where(p_id == max)

        return p, id

    def predict_from_batch_data(self, in_batch_ds):
        """Predicts the class of the given batch of images.

        :param in_batch_ds: The batch of images.

        :return: The softmax array of predictions and the id of the prediction from class names.
        """
        test_ds = in_batch_ds

        img, label = next(iter(test_ds))
        # print(len(img))
        self.log.info("Predicting on batch of {} images.".format(len(img)))

        ids = []
        for i in img:
            i = np.array(i)
            i = np.expand_dims(i, axis=0)
            p = self.imported.predict(i)
            p = np.array(p)
            p = np.squeeze(p)
            max = p.max()
            id = np.where(p == max)
            ids.append(id[0])
        return np.array(label), np.squeeze(np.array(ids))
