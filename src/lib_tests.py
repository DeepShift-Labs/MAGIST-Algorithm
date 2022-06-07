import datetime

import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout
from tqdm import tqdm

EPOCHS = 5
BATCH_SIZE = 32
INPUT_IMAGE_SIZE = (60, 60)
VAL_SPLIT = 0.2
DATA_IN_DIR = "Data"
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
).repeat()

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
).repeat()


class CNN(tf.keras.models.Model):
	def __init__(self):
		super(CNN, self).__init__()
		self.conv1 = Conv2D(32, (3, 3), activation='relu')
		self.conv2 = Conv2D(64, (3, 3), activation='relu')
		# self.conv3 = Conv2D(128, (3, 3), activation='relu')
		# self.conv4 = Conv2D(64, (3, 3), activation='relu')
		self.conv5 = Conv2D(32, (3, 3), activation='relu')
		self.flat = Flatten()
		# self.dense1 = Dense(128, activation='relu')
		# self.drop1 = Dropout(0.5)
		self.dense2 = Dense(64, activation='relu')
		self.drop2 = Dropout(0.5)
		self.dense3 = Dense(32, activation='relu')
		self.dense4 = Dense(2)

	def call(self, x):
		x = self.conv1(x)
		x = self.conv2(x)
		# x = self.conv3(x)
		# x = self.conv4(x)
		x = self.conv5(x)
		x = self.flat(x)
		# x = self.dense1(x)
		# x = self.drop1(x)
		x = self.dense2(x)
		x = self.drop2(x)
		x = self.dense3(x)
		x = self.dense4(x)
		return x


model = CNN()

loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
	name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
	name='test_accuracy')

current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'TensorBoard/train_logs/gradient_tape/' + current_time + '/train'
test_log_dir = 'TensorBoard/train_logs/gradient_tape/' + current_time + '/test'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer = tf.summary.create_file_writer(test_log_dir)

log_dir = "TensorBoard/tf_histograms/fit/" + \
          datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(
	log_dir=log_dir, histogram_freq=1, update_freq='batch')
tensorboard_callback.set_model(model)

ckpt = tf.train.Checkpoint(step=tf.Variable(1), optimizer=optimizer, net=model, iterator=train_ds)
manager = tf.train.CheckpointManager(ckpt, './tf_ckpts', max_to_keep=4000)


@tf.function
def train_step(images, labels):
	with tf.GradientTape() as tape:
		# training=True is only needed if there are layers with different
		# behavior during training versus inference (e.g. Dropout).
		predictions = model(images, training=True)
		loss = loss_object(labels, predictions)
	gradients = tape.gradient(loss, model.trainable_variables)
	optimizer.apply_gradients(zip(gradients, model.trainable_variables))

	train_loss(loss)
	train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
	# training=False is only needed if there are layers with different
	# behavior during training versus inference (e.g. Dropout).
	predictions = model(images, training=False)
	t_loss = loss_object(labels, predictions)

	test_loss(t_loss)
	test_accuracy(labels, predictions)


epoch_arr = []
train_loss_arr = []
train_accuracy_arr = []
test_loss_arr = []
test_accuracy_arr = []

ckpt.restore(manager.latest_checkpoint)
if manager.latest_checkpoint:
	print("Restored from {}".format(manager.latest_checkpoint))
else:
	print("Initializing from scratch.")

# callbacks.on_train_begin()
for epoch in (pbar_epoch := tqdm(range(EPOCHS))):
	# callbacks.on_epoch_begin(epoch)
	pbar_epoch.set_description("Epoch Progress: ")
	# Reset the metrics at the start of the next epoch
	train_loss.reset_states()
	train_accuracy.reset_states()
	test_loss.reset_states()
	test_accuracy.reset_states()

	for images, labels in (pbar_train := tqdm(train_ds.take(BATCH_SIZE), leave=False)):
		# callbacks.on_train_batch_begin(images)
		pbar_train.set_description("Train Step: ")
		train_step(images, labels)
		ckpt.step.assign_add(1)
	with train_summary_writer.as_default():
		tf.summary.scalar('loss', train_loss.result(), step=epoch)
		tf.summary.scalar('accuracy', train_accuracy.result(), step=epoch)

	for test_images, test_labels in (pbar_test := tqdm(val_ds.take(BATCH_SIZE), leave=False)):
		pbar_test.set_description("Test Step: ")
		test_step(test_images, test_labels)
	with test_summary_writer.as_default():
		tf.summary.scalar('loss', test_loss.result(), step=epoch)
		tf.summary.scalar('accuracy', test_accuracy.result(), step=epoch)

	if ((int(ckpt.step) - 1) % BATCH_SIZE) == 0:
		save_path = manager.save()
		print("Saved checkpoint for step {}: {}".format(int(ckpt.step) - 1, save_path))

	epoch_arr.append(epoch + 1)
	train_loss_arr.append(train_loss.result())
	train_accuracy_arr.append(train_accuracy.result() * 100)
	test_loss_arr.append(test_loss.result())
	test_accuracy_arr.append(test_accuracy.result() * 100)
# callbacks.on_epoch_end(epoch)
# callbacks.on_train_end()


for i in range(len(epoch_arr)):
	print(
		f'Epoch {epoch_arr[i]}, '
		f'Loss: {train_loss_arr[i]}, '
		f'Accuracy: {train_accuracy_arr[i]}, '
		f'Test Loss: {test_loss_arr[i]}, '
		f'Test Accuracy: {test_accuracy_arr[i]}'
	)
