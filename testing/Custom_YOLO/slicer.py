from PIL import Image
import os, pathlib
from tqdm import tqdm

def resizer(size, base_path):
    base_path = pathlib.Path(base_path)
    base_path = base_path.resolve()  # Find the absolute path from relative one.
    base_path = str(base_path)

    files_os = os.listdir(base_path)
    files = []

    for filename in files_os:
        files.append(filename)

    for f in files: #for i in range(image_count + 1):
        try:
            image_path = os.path.join(base_path, str(f)) #str(base_path) + "/Frame(" + str(i) + ").jpg"
            print(image_path)
            img = Image.open(image_path)
            resizedImage = img.resize(size)
            resizedImage.save(image_path)

        except FileNotFoundError:
            print("Resize Skip")

def coordinate_compute(input_size, individual_output_size):
    coordinates = []

    l = input_size[0]
    w = input_size[1]

    final_l = individual_output_size[0]
    final_w = individual_output_size[1]

    if l != w:
        raise RuntimeError("Cannot compute non-square images yet!")
    if final_l != final_w:
        raise RuntimeError("Cannot compute non-square images yet!")
    l1 = 0
    w1 = 0
    l2 = final_l
    w2 = final_w

    try:
        while w2 <= w: #for i in range(iterations):
            while l2 <= l: #for c in range(iterations):
                coordinates.append([l1, w1, l2, w2])
                l1 += final_l
                l2 += final_l

            w1 += final_w
            w2 += final_w
            l1 = 0
            l2 = final_l
        return coordinates
    except RuntimeError:
        return "Iteration calculation return non-int value!"

def crop_segments(coordinates, start_path, end_path):
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

    counter = 0

    for f in tqdm(files): #for i in range(image_count + 1):
        image_path = os.path.join(start_path, str(f))
        img = Image.open(image_path)

        for c in range(len(coordinates)):
            box = (int(coordinates[c][0]), int(coordinates[c][1]), int(coordinates[c][2]), int(coordinates[c][3]))
            croppedImage = img.crop(box)
            save_location = os.path.join(end_path, "Frame" + str(counter) + str(c) + ".jpg")
            croppedImage.save(save_location)

        counter += 1

resizer((500, 500), "Input")
coordinates = coordinate_compute((500, 500), (100, 100))
crop_segments(coordinates, "Input", "Testing/")

