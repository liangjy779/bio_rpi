import wavio

import random
import numpy as np
import ffmpeg
import subprocess
import simpleaudio as sa
import pyaudio
import wave
import datetime

audio_format = pyaudio.paInt16
number_of_channels=1
sample_rate=192000
chunk_size = 4096
duration = 5

#directory, create recording filepath
rec_dir = '/home/jana0009/acdnet_on_computer/acdnet/rec_audiomoth/';
rec_timestamp_str = "{}".format(datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))
rec_filename = 'rec_' + str(duration) + 'sec_' + rec_timestamp_str + '.wav'
rec_filepath = rec_dir + rec_filename

#create pyaudio instance and search for AudioMoth

device_index = None
audio = pyaudio.PyAudio()

print(f"audio.get_device_count() = {audio.get_device_count()}")

for i in range(audio.get_device_count()):
    print(f"{i} - {audio.get_device_info_by_index(i).get('name')}")
    if 'AudioMoth' in audio.get_device_info_by_index(i).get('name'):
        device_index = i;
        break

if device_index == None:
    print('No AudioMoth found!')
    exit()
#create pyaudio stream
stream = audio.open(format=audio_format,
                    rate=sample_rate,
                    channels=number_of_channels,
                    input_device_index=device_index,
                    input=True,
                    frames_per_buffer=chunk_size);

#Append audio chunks to array until enough samples have been acquired.
print('Start recording ... SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS');
data = []

total_samples = sample_rate * duration;
print(f"total_samples = {total_samples}");

while (total_samples >0):
    samples = min(total_samples,chunk_size)
    data.append(stream.read(samples))
    total_samples -= samples;

print('Finished recording. EEEEEEEEEEEEEEEEEEEEEEE')

#stop the stream, close it, and terminate the pyaudio instance
stream.stop_stream()
stream.close()
audio.terminate()

#save the audio data as a wav file
wavefile = wave.open(rec_filepath,'wb')
wavefile.setchannels(number_of_channels)
wavefile.setsampwidth(audio.get_sample_size(audio_format)
wavefile.setframerate(sample_rate)
wavefile.writeframes(b''.join(data))
wavefile.close()

random.seed(42);

def normalize(sound,factor):
    return sound/factor

def padding(sound, pad):
    return np.pad(sound, pad, 'constant')

def multi_crop(sound, input_length, n_crops):
    if(n_crops>1):
        stride = (len(sound) - input_length) // (n_crops - 1)
        sounds = [sound[stride * i: stride * i + input_length] for i in range(n_crops)]
    else:
        sounds = [sound];
    return np.array(sounds)

def preprocess(sound, inputLength, nCrops):
    print("PREPROCESS():****************")
    print(f" type(sound)= {type(sound)} -1- PREPROCESS():padding {sound.shape}, {sound.dtype} typed sound data with zeros for both sides: '0' x {inputLength//2} left & right" )
    sound = padding(sound, inputLength // 2);
    print(f" PREPROCESS():padding is over, now normalising...")
    print(f" type(sound)= {type(sound)} -2- PREPOCESS() dtype of sound[] before normalise, after padding= {sound.dtype} ")
    sound = normalize(sound, 32768.0),
    print(f" type(sound)= {type(sound)} -3- PREPROCESS():normalisation is complete. sound = {sound}, type(sound)= {type(sound)}")
    sound = multi_crop(sound[0], inputLength, nCrops);
    print(f"type(sound) = {type(sound)} -4- PREPROCESS():multi cropping is over...")
    return sound;

index_filelist = 313;

wav_dir_input = rec_dir;
wav_dir_output = rec_dir + "output/"
wav_filename_input = rec_filename;
# rec_filename = 'rec_' + str(duration) + 'sec_' + rec_timestamp_str + '.wav'
# rec_filepath = rec_dir + rec_filename
wav_filename_output = "16Hz__" + rec_filename

use_directory_list = False;
if(use_directory_list):
    filelist_textfile = 








