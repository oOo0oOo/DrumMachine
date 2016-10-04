from time import time
import random
import pickle

import numpy as np
import matplotlib.pyplot as plt

from wavenet.utils import load_sample, generate_sample, save_sample
from wavenet.models import Model, Generator

model_path = 'networks/snare_20/'
samples_path = 'data/drum_samples'
wav_template = 'rendered/snare_20/epoch{}.wav'

len_sample = 0.2 # [s] # 0.1s hi-hat_20, kick_20n = 0.2s
len_sample = int(16000 * len_sample)

# Unpickle and form two lists (filnames, instrument_id)
sorted_f = pickle.load(open(samples_path, 'rb'))
samples = sorted_f['Snare']

# Sample random samples
for i in range(1):
    # j = 450   # kick_20
    # j = 840 # hihat_20
    j = 948 # snare_20

    batches = [load_sample(s, len_sample) for s in samples[j:j+20]]
    inputs = np.array([b[0] for b in batches])
    targets = np.array([b[1] for b in batches])
    print 'Loaded {} samples'.format(len(batches))

    all_inputs = inputs[:,0,:,0].flatten()
    save_sample(all_inputs, 'rendered/snare_20/inputs_{}.wav'.format(j))

# Create the model
model = Model(num_time_samples=len_sample,
              num_channels=1,
              gpu_fraction=1.0)
last_epoch = model.load_model(model_path)
if last_epoch:
    start = last_epoch + 1
else:
    start = 0

inds = np.arange(len(batches))


for i in xrange(start, 10000000):
    # Shuffle
    random.shuffle(inds)

    inputs = inputs[inds]
    targets = targets[inds]

    before = time()
    avg_loss = model.train_epoch(inputs, targets, batch_size = 2)
    dur = round(time() - before, 1)
    print 'Epoch {} avg loss: {}, t = {} s'.format(i, avg_loss, dur)

    if i and not i%250:
        model.save_model(model_path, step = i)

    if i and not i%1000:
        generator = Generator(model)
        generate_sample(generator, len_sample, wav_template.format(i))

    if avg_loss < 0.01:
        generator = Generator(model)
        generate_sample(generator, len_sample, wav_template.format(i))
        model.save_model(model_path, step = i)
        print 'Stopped: avg loss < 0.01'
        break
