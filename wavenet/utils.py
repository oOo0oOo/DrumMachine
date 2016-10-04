import numpy as np
from scipy import signal
import librosa
from time import time


def normalize(data):
    temp = np.float32(data) - np.min(data)
    out = (temp / np.max(temp) - 0.5) * 2
    return out


def trim_silence(audio, threshold=0.3):
    '''
        From: https://github.com/ibab/tensorflow-wavenet/blob/master/audio_reader.py
        Removes silence at the beginning and end of a sample.
    '''
    energy = librosa.feature.rmse(audio)
    frames = np.nonzero(energy > threshold)
    indices = librosa.core.frames_to_samples(frames)[1]

    # Note: indices can be an empty array, if the whole audio was silence.
    return audio[indices[0]:indices[-1]] if indices.size else audio[0:0]


def load_sample(path, max_len):
    # data = wavfile.read(path)[1]
    data, _ = librosa.load(path, sr=16000, mono=True)
    #data = trim_silence(data, 0.3)
    data = data.reshape(-1)

    data_ = normalize(data)

    # pad or crop
    l = data_.shape[0]
    if l > max_len:
        data_ = data_[:max_len+1]
    else:
        # We repeat the sample instead of padding with 0
        n_repeats = (max_len/l)+1
        data_ = np.tile(data_, n_repeats)
        data_ = data_[:max_len+1]

        # data_ = np.pad(data_, [0, max_len - l + 1], 'constant')

    # data_f = np.sign(data_) * (np.log(1 + 255*np.abs(data_)) / np.log(1 + 255))
    bins = np.linspace(-1, 1, 256)

    # Quantize inputs.
    inputs = np.digitize(data_[0:-1], bins, right=False) - 1
    inputs = bins[inputs][None, :, None]

    # Encode targets as ints.
    targets = (np.digitize(data_[1::], bins, right=False) - 1)[None, :]
    return inputs, targets


def save_sample(y, path, sampling_rate = 44000):
    # ATTENTION: a sampling rate of 16kHz is assumed
    len_sample = y.shape[0]
    n_frames = (float(len_sample)/16000) * sampling_rate
    y = signal.resample(y, n_frames)
    librosa.output.write_wav(path, y, sampling_rate)


def generate_sample(generator, len_sample, path, sampling_rate = 44000, init_value = False):
    before = time()

    if not init_value:
        d = 0.1
        init_value = np.random.uniform(-d,d, (1,1))
    else:
        init_value = np.array(init_value).reshape((1,1))
        d = 0.01
        init_value += np.random.uniform(-d,d)
        assert init_value.shape == (1,1)

    predictions = generator.run(init_value, len_sample)[0]
    save_sample(predictions, path, sampling_rate = sampling_rate)

    dur = round(time() - before, 1)
    l_samp = float(len_sample)/16000
    real = round(l_samp / dur,3)
    print 'Generated {} s in {} s, Realtime factor: {}, Path: {}'.format(l_samp, dur, real, path)