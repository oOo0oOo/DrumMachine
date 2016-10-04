from time import time
import random
import pickle

import numpy as np
import matplotlib.pyplot as plt

from wavenet.utils import load_sample, generate_sample, save_sample
from wavenet.models import Model, Generator

model_path = 'networks/snare_20/'
wav_template = 'rendered/snare_20/final/{}.wav'
samples_path = 'data/drum_samples'

len_sample = 0.2 # [s] # 0.1s hi-hat_20, 0.2s snare
len_sample = int(16000 * len_sample)

# Load samples
sorted_f = pickle.load(open(samples_path, 'rb'))
samples = sorted_f['Snare']

# j = 450   # kick_20
# j = 840 # hihat_20
j = 948 # snare_20

init_values = [load_sample(s, len_sample)[0] for s in samples[j:j+20]]

init_values = np.array(init_values)[:,0,0,0]

print init_values.shape
# Create the model
model = Model(num_time_samples=len_sample,
              num_channels=1,
              gpu_fraction=1.0)
last_epoch = model.load_model(model_path)

for i in xrange(1000):
    # Pick a random start
    init_value = np.random.choice(init_values)
    generator = Generator(model)
    generate_sample(generator, len_sample, wav_template.format(i), init_value = init_value)