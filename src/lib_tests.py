import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization
import os

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
)

model = tf.keras.Sequential([
	Conv2D(32, kernel_size=(3,3), strides=(1, 1), padding='same', activation='relu', input_shape=(60, 60, 3)),
	BatchNormalization(),

	Conv2D(64, kernel_size=(3,3), strides=(1, 1), padding='same', activation='relu'),
	BatchNormalization(),

	# Conv2D(128, kernel_size=(3,3), strides=(1, 1), padding='same', activation='relu'),
	# BatchNormalization(),
	#
	# Conv2D(128, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'),
	# BatchNormalization(),

	# Conv2D(128, kernel_size=(4, 4), strides=(1, 1), padding='same', activation='relu'),
	# BatchNormalization(),

	Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'),
	BatchNormalization(),

	Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'),
	BatchNormalization(),

	Flatten(),

	Dense(128, activation='relu'),
	Dropout(0.5),
	Dense(64, activation='relu'),
	Dropout(0.5),
	Dense(2, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
checkpoint_path = "training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=False, verbose=1)

history = model.fit(train_ds, epochs=EPOCHS, steps_per_epoch=10, validation_data=val_ds, validation_steps=10, batch_size=BATCH_SIZE, validation_batch_size=BATCH_SIZE, use_multiprocessing=True, callbacks=[cp_callback])
