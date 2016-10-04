# Drum Machine

[WaveNet](https://deepmind.com/blog/wavenet-generative-model-raw-audio/) presents a neural network architecture that can generate raw audio samples.
This repository uses the [FastNet](https://github.com/tomlepaine/fast-wavenet) implementation to generate (overfitted) drum samples.
I customized very little of the original implementation, so all credit goes to the original team...

For input samples and rendered beats check out the [Souncloud Playlist](https://soundcloud.com/oouuli/sets/drummachine)!

## Details

The goal is to generate audio samples for use in a drum machine.
A minimal drumset included 3 instruments: Hi-Hat, Snare & Kick

Since the uncoditional version of WaveNet is used, 3 separate
neural networks were trained sequentially.
Each instrument was trained from 20 samples; the [playlist](https://soundcloud.com/oouuli/sets/drummachine) includes a concatenated version of all the training samples. 16 kHz samples were used, cut to equal length (0.1s for Hi-Hat and 0.2s for the others).

Training was performed for 180k, 132k and 380k epochs respectively
(until the loss reached a threshold of 0.01).
This threshold was probably way too low...

The trained networks were used to generate around 1000 samples each.
Seeds were randomly selected from the initial values of the 20 samples +
a little bit of noise. Generation was around 25x slower than real time on a GTX 1080.

Next a simple sequencer script was used to render random samples into a beat.
Every rendered beat contains no sample twice.
No further post-processing was applied (eq and compression would do wonders).

To repeat: The neural network did not directly generate the output sample.


## Does it grove?

The [playlist](https://soundcloud.com/oouuli/sets/drummachine) includes two examples of rendered beats.

Clearly the instruments didn't converge equally well:
Hi-Hats > Snares > Kicks, in my opinion.

I also suspect the networks overfitted due to the long training, which is audible e.g. the Hi-Hat often replicates a few very distinct samples, which are nearly identical.

Nevertheless I think the final beat could get the powernoise house crowd moving.