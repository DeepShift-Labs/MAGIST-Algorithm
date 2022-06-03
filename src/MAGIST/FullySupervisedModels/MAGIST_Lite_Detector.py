import tensorflow as tf

EPOCHS = 100
BATCH_SIZE = 32
INPUT_IMAGE_SIZE = (60, 60)
TRAIN_SPLIT = 0.8
DATA_IN_DIR = "Sliced"
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
	validation_split=TRAIN_SPLIT,
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
	validation_split=TRAIN_SPLIT,
	subset='validation',
	interpolation='bilinear',
	follow_links=False,
	crop_to_aspect_ratio=False,
)