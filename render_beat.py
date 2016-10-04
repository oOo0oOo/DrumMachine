import librosa
from os import listdir
import numpy as np
import itertools as it
import random


def render_beat(sample_folders, beat, bpm, repeats = 1):
    # Load all samples
    samples = []
    ind_iter = []
    max_samples = [sum(i) * repeats for i in beat]

    for s_path, max_samp in zip(sample_folders,max_samples):
        track_samples = []

        # Get epoch of each sample and sort by epoch
        # f_names = list(listdir(s_path))
        # epochs = [int(f[5:-4]) for f in f_names if f.startswith('epoch')]
        # for epoch in sorted(epochs):
        #     f_name = 'epoch{}.wav'.format(epoch)
        #     audio = librosa.load(s_path + f_name, sr=16000, mono=True)[0]
        #     track_samples.append(audio)

        f_names = [f for f in listdir(s_path) if f.endswith('.wav')]
        random.shuffle(f_names)
        for f_name in f_names:
            audio = librosa.load(s_path + f_name, sr=16000, mono=True)[0]
            track_samples.append(audio)
            if len(track_samples) == max_samp:
                break

        #ind_iter.append(it.cycle(range(len(track_samples))))
        l = range(len(track_samples))
        random.shuffle(l)
        ind_iter.append(iter(l))
        samples.append(track_samples)

    # Convert samples <--> beats
    n_beats = len(beat[0])
    n_tracks = len(beat)
    samples_per_beat = int((60./bpm) * 16000)
    tot_samples = n_beats * samples_per_beat

    # Render each track
    rendered = []
    for t_id in range(n_tracks):
        # Repeat beat a few times
        rep_tracks = []
        for rep in range(repeats):

            track = np.zeros(tot_samples)
            for b_id in range(n_beats):
                if beat[t_id][b_id]:
                    start = b_id * samples_per_beat

                    # Get a sample
                    ind = ind_iter[t_id].next()
                    audio = samples[t_id][ind]

                    # Write to track
                    if audio.shape[0] > samples_per_beat:
                        end = (b_id+1) * samples_per_beat
                        track[start:end] = audio[:samples_per_beat]
                    else:
                        track[start:start+audio.shape[0]] = audio

            rep_tracks.append(track)

        # Stack rep_tracks
        rep_tracks = np.concatenate(rep_tracks)
        rendered.append(rep_tracks)

    # Concatenate and sum all tracks
    rendered = np.array(rendered)
    track_sum = np.sum(rendered, axis = 0)

    # Save a track
    librosa.output.write_wav('assets/beat_render2.wav', track_sum, 16000)

    print 'Rendered beat...'



if __name__ == '__main__':
    sample_folders = [
        'rendered/hihat_20/final/',
        'rendered/snare_20/final/',
        'rendered/kick_20/final/'
    ]

    # Simple House
    # beat = [
    #     [0,1,0,1,0,1,0,0], # Hihat Track
    #     [0,0,1,0,0,0,1,0], # Snare Track
    #     [1,0,0,0,1,0,0,1], # Kick Track
    # ]

    # Simple House 2
    beat = [
        [0,1,0,0,0,1,0,1], # Hihat Track
        [0,0,1,0,0,0,1,0], # Snare Track
        [1,0,0,1,1,0,0,0], # Kick Track
    ]

    bpm = 124 * 2 # Our beats are 8ths (not 4ths)

    beat = render_beat(sample_folders, beat, bpm, repeats = 8)