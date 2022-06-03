"""Provides basic functions to prepare data for MAGIST lite detection.

The class ImageSlicer is the main class containing 3 functions: resizer, coordinate_compute, and crop_segments. The
resizer function takes a given image path and resizes it to a given size. It will resize all images in that directory.
The coordinate_compute function takes a given input image size and divides the image into segments. It will compute the
pixel coordinates of each segment. The crop_segments function will take an array of pixel coordinates, crop the image
segment, and export it to a given directory.
"""
import PIL
from PIL import Image, UnidentifiedImageError
import os, pathlib
from tqdm import tqdm
from ..LogMaster.log_init import MainLogger


class ImageSlicer:
	"""Pre-processing functions for MAGIST Lite Detection"""

	def __init__(self, config):
		"""Initialize the ImageSlicer class and logger

		:param config: A relative or absolute path to master config JSON file.
		"""
		root_log = MainLogger(config)
		self.log = root_log.StandardLogger("ImageSlicer")  # Create a script specific logging instance

	def resizer(self, size, base_path):
		""""Batch rezise images in a given directory to a given size.

		:param size: The size to resize the images to.
		:param base_path: The directory containing the images to resize.
		"""
		base_path = pathlib.Path(base_path)
		base_path = base_path.resolve()  # Find the absolute path from relative one.
		base_path = str(base_path)

		files_os = os.listdir(base_path)
		files = []

		for filename in files_os:
			files.append(filename)

		self.log.info("Discovered {} files in {}".format(len(files), base_path))

		counter = 0

		self.log.info("Resizing images...")

		for f in tqdm(files):  # for i in range(image_count + 1):
			try:
				image_path = os.path.join(base_path, str(f))  # str(base_path) + "/Frame(" + str(i) + ").jpg"
				try:
					img = Image.open(image_path)
					resizedImage = img.resize(size)
					resizedImage = resizedImage.convert('RGB')
					resizedImage.save(image_path)
					counter += 1
				except PIL.UnidentifiedImageError:
					self.log.warning("Unidentified image: {}".format(image_path))


			except (FileNotFoundError, UnidentifiedImageError, ValueError) as error:
				if error == UnidentifiedImageError:
					print("Unidentified image: {}".format(image_path))
				if error == FileNotFoundError:
					print("Image Not Found: {}".format(image_path))
				if error == ValueError:
					print("Image Type Not Supported: {}".format(image_path))

		self.log.info("Resized {} files in {}".format(counter, base_path))

	def coordinate_compute(self, input_size, individual_output_size):
		"""Compute the pixel coordinates of each segment.

		:param input_size: The size of the input image.
		:param individual_output_size: The size of each segment.
		"""
		coordinates = []

		l = input_size[0]
		w = input_size[1]

		final_l = individual_output_size[0]
		final_w = individual_output_size[1]

		if l != w:
			raise RuntimeError("Cannot compute non-square images yet!")
		if final_l != final_w:
			raise RuntimeError("Cannot compute non-square images yet!")

		self.log.info("Computing coordinates for {}x{} image. Preliminary checks complete.".format(l, w))

		l1 = 0
		w1 = 0
		l2 = final_l
		w2 = final_w

		try:
			while w2 <= w:  # for i in range(iterations):
				while l2 <= l:  # for c in range(iterations):
					coordinates.append([l1, w1, l2, w2])
					l1 += final_l
					l2 += final_l

				w1 += final_w
				w2 += final_w
				l1 = 0
				l2 = final_l
			self.log.info("Coordinates computed successfully.")
			return coordinates
		except RuntimeError:
			return "Iteration calculation return non-int value!"

	def crop_segments(self, coordinates, start_path, end_path, img_class):
		"""Crop the image segments and export them to a given directory.

		:param coordinates: The pixel coordinates of each segment.
		:param start_path: The directory containing the images to crop.
		"""

		os.system(f"mkdir {os.path.join(end_path, img_class)}")

		start_path = pathlib.Path(start_path)
		start_path = start_path.resolve()  # Find the absolute path from relative one.
		start_path = str(start_path)

		end_path = pathlib.Path(end_path)
		end_path = end_path.resolve()  # Find the absolute path from relative one.
		end_path = str(end_path)

		files_os = os.listdir(start_path)
		files = []

		for filename in files_os:
			files.append(filename)

		self.log.info("Discovered {} files in {}".format(len(files), start_path))

		counter = 0

		for f in tqdm(files):  # for i in range(image_count + 1):
			image_path = os.path.join(start_path, str(f))
			try:
				img = Image.open(image_path)
			except PIL.UnidentifiedImageError:
				self.log.warning("Unidentified image: {}".format(image_path))

			for c in range(len(coordinates)):
				box = (int(coordinates[c][0]), int(coordinates[c][1]), int(coordinates[c][2]), int(coordinates[c][3]))
				croppedImage = img.crop(box)
				save_location = os.path.join(end_path, img_class, "Frame" + str(counter) + str(c) + ".jpg")
				croppedImage = croppedImage.convert('RGB')
				croppedImage.save(save_location)

				counter += 1

		self.log.info("Cropped {} files in {}".format(counter, start_path))

	def image_integrity_verification(self, path, delete_invalid=True):
		"""Verify the integrity of the images in a given directory.

		:param path: The directory containing the images to verify.
		:param delete_invalid: Whether to delete the invalid images.
		"""
		path = pathlib.Path(path)
		path = path.resolve()  # Find the absolute path from relative one.
		path = str(path)

		onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

		bad_files = 0
		good_files = 0

		if delete_invalid:
			self.log.info("Deleting invalid files...")
		else:
			self.log.info("Delete option disabled. Skipping invalid files...")

		for f in onlyfiles:
			try:
				img = Image.open(os.path.join(path, f)).load()
				good_files += 1
			except (PIL.UnidentifiedImageError, Exception) as error:
				bad_files += 1
				if delete_invalid:
					os.remove(os.path.join(path, f))
				self.log.warning(f'Invalid image: {os.path.join(path, f)}')

		if delete_invalid:
			self.log.info("Deleted {} invalid files of {}.".format(bad_files, bad_files + good_files))
		else:
			self.log.info(f'{bad_files} invalid files of {bad_files + good_files} were found.')

# resizer((500, 500), "Input")
# coordinates = coordinate_compute((500, 500), (100, 100))
# crop_segments(coordinates, "Input", "Testing/")

