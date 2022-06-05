import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization
import os, datetime

EPOCHS = 100
BATCH_SIZE = 32
INPUT_IMAGE_SIZE = (60, 60)
VAL_SPLIT = 0.2
DATA_IN_DIR = "PetImages"
SEED = 42

train_ds = tf.keras.utils.image_dataset_from_directory(
	DATA_IN_DIR,
	labels='inferred',
	label_mode='int',
	class_names=None,
	color_mode='rgb',
	batch_size=BATCH_SIZE,
	image_size=INPUT_IMAGE_SIZE,
	shuffle=True,
	seed=SEED,
	validation_split=VAL_SPLIT,
	subset='training',
	interpolation='bilinear',
	follow_links=False,
	crop_to_aspect_ratio=False,
	# class_mode='sparse'
)

val_ds = tf.keras.utils.image_dataset_from_directory(
	DATA_IN_DIR,
	labels='inferred',
	label_mode='int',
	class_names=None,
	color_mode='rgb',
	batch_size=BATCH_SIZE,
	image_size=INPUT_IMAGE_SIZE,
	shuffle=True,
	seed=SEED,
	validation_split=VAL_SPLIT,
	subset='validation',
	interpolation='bilinear',
	follow_links=False,
	crop_to_aspect_ratio=False,
	# class_mode='sparse'
)

model = tf.keras.Sequential([
	Flatten(input_shape=(60, 60, 3)),
	Dense(28, activation='relu'),
	Dense(2, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss="sparse_categorical_crossentropy", metrics=['accuracy'])
checkpoint_path = "training_ckpt/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=False, verbose=1)

log_dir = "tensorboard_logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq='batch')

history = model.fit(train_ds, epochs=EPOCHS, steps_per_epoch=10, validation_data=val_ds, validation_steps=10, batch_size=BATCH_SIZE, validation_batch_size=BATCH_SIZE, use_multiprocessing=True, callbacks=[cp_callback, tensorboard_callback])
