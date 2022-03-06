import moviepy.editor as mp
import matplotlib.pyplot as plt
import numpy as np
import wave
from pydub import AudioSegment

def mp32wav(file_in, file_out):
    sound = AudioSegment.from_mp3(file_in)
    sound.export(file_out, format="wav")


def split_audio(vid, out):
    my_clip = mp.VideoFileClip(vid)
    my_clip.audio.write_audiofile(out)

def audio2numpy(audio):
    raw = wave.open(audio)
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")
    f_rate = raw.getframerate()
    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )

    return time, signal, f_rate

def visualize(path: str):
    # reading the audio file
    raw = wave.open(path)

    # reads all the frames
    # -1 indicates all or max frames
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")

    # gets the frame rate
    f_rate = raw.getframerate()

    # to Plot the x-axis in seconds
    # you need get the frame rate
    # and divide by size of your signal
    # to create a Time Vector
    # spaced linearly with the size
    # of the audio file
    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )

    # using matplotlib to plot
    # creates a new figure
    plt.figure(1)

    # title of the plot
    plt.title("Sound Wave")

    # label of x-axis
    plt.xlabel("Time")

    # actual plotting
    plt.plot(time, signal)

    # shows the plot
    # in new window
    plt.show()

    # you can also save
    # the plot using
    # plt.savefig('filename')


