# Sorts warbeats samples into instrument categories
# and saves a pickled dictionary {'instrument': [path1, path2]}

import fnmatch
import os
import pickle

from scipy.io.wavfile import read, write

def test_wav_file(filename):
    print filename
    try:
        waveform = read(filename)
        return True
    except ValueError:
        return False

# Retrieve all filenames in warbeats directory recursively
matches = []
src_path = 'data/WarBeats'
for root, dirnames, filenames in os.walk(src_path):
    for filename in fnmatch.filter(filenames, '*.*'):
        matches.append(os.path.join(root, filename))

# Only keep wav (too lazy to change fnmatch)
wavs = []
for i, f_name in enumerate(matches):
    f_low = f_name.lower()

    # Is wav file
    if not f_low[-4:] == '.wav':
        continue

    # Is valid wav file
    if not test_wav_file(f_name):
        continue

    # Try to load the file
    wavs.append(f_name)

    if not i%250:
        print 'Tested {}/{} files'.format(len(wavs), len(matches))


# Sort into categories using matching words (not case sensitive)
categories = {
    'Hi-Hat': ['hat', 'hh', 'ht'],
    'Snare': ['sn', 'sd'],
    'Rim': ['rim', 'rm'],
    'Clap': ['cla', 'hc'],
    'Kick': ['kick', 'kik', 'bd'],
    'Tom': ['tom', 'bong', 'cong'],
    'Percussion': ['per', 'cow', 'shaker',
        'agogo', 'cabasa', 'tamb', 'hit',
        'cli'],
    'Cymbal': ['rid', 'cra', 'cym'],
    'Bass': ['bass']
}

sorted_f = {f:[] for f in categories.keys()}
sorted_f['Other'] = []

for f_name in wavs:
    f_low = f_name.lower()

    # Is wav file
    if not f_low[-4:] == '.wav':
        continue

    # Sort into bins (or other)
    for cat, f_str in categories.items():
        if any([f in f_low for f in f_str]):
            sorted_f[cat].append(f_name)
            break
    else:
        sorted_f['Other'].append(f_name)

# Pickle and save the dictionary
pickle.dump(sorted_f, open('data/drum_samples', 'wb'))

t = len(wavs)
s = t - len(sorted_f['Other'])
p = round(100. * s/t, 2)
c = len(categories.keys())
print 'Sorted {}/{} samples ({} %) into {} instrument categories'.format(s,t,p,c)