import math

import numpy as np
import video_audio_libs
from PIL import Image
import os
from tqdm import tqdm

# mic_frequency = 44100 #Hz
# fps = 30
# audio1 = []
# video1 = []


def group_audio_video_sync(image_in_dir, audio_in, fps):
  audio1 = []
  video1 = []

  time, signal, mic_freq = video_audio_libs.audio2numpy(audio_in)
  print(len(signal))

  file1 = os.listdir(image_in_dir)

  for f in tqdm(file1):
    img = Image.open(f"{image_in_dir}/{f}")
    np_img = np.array(img)
    video1.append(np_img)

  index = 0
  for f in tqdm(file1):
    chunk = []
    for s in range(int(math.floor(len(signal)/len(file1)))): #mic_freq/fps
      chunk.append(signal[index])
      index = index + 1
    audio1.append(chunk)
  print(index)

  return audio1, video1

def data_to_wave(data):
  signal = []

  for i in tqdm(data):
    for a in i:
      signal.append(a)

audio, video = group_audio_video_sync("Frames/1", "Raw_Data/Audio/1.wav", 30)

# print(len(audio[0])*len(video))
print(video)