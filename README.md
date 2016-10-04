# Drum Machine

[WaveNet](https://deepmind.com/blog/wavenet-generative-model-raw-audio/) presents a neural network architecture that can generate raw audio samples.
This repository uses the [FastNet](https://github.com/tomlepaine/fast-wavenet) implementation to generate (overfitted) drum samples.
I customized very little of the original implementation, so all credit goes to the original team...

## Details

The goal is to generate audio samples for use in a drum machine.
A minimal drumset included 3 instruments: Hi-Hat, Snare & Kick

Since the uncoditional version of WaveNet is used, 3 separate
neural networks were trained sequentially.
Each instrument was trained from 20 samples, which are concatenated here:
[Hi-Hats](https://soundcloud.com/oouuli/hihats?in=oouuli/sets/drummachine), [Snares](https://soundcloud.com/oouuli/snares?in=oouuli/sets/drummachine), [Kicks](https://soundcloud.com/oouuli/kicks?in=oouuli/sets/drummachine)
Training was performed for 180k, 132k and 380k epochs respectively
(until the loss reached a threshold of 0.01).
380k was probably way too much...

The trained networks were used to generate approx 100 samples each.
Seeds were randomly selected from the initial values of the 20 samples +
a little bit of noise.

Next a simple sequencer script was used to render random samples into a beat.
To repeat: The neural network did not directly generate the output sample.
No further post-processing was applied (eq and compression would do wonders).


## Does it grove?

Here are two examples of rendered beats: [House1](https://soundcloud.com/oouuli/beat-render1?in=oouuli/sets/drummachine), [House2](https://soundcloud.com/oouuli/beat-render2?in=oouuli/sets/drummachine)
Clearly the instruments didn't converge equally well:
Hi-Hats > Snares > Kicks
Also I suspect the networks overfitted due to the long training, which is audible:
E.g. the Hi-Hat often replicates a few very distinct samples, which are nearly identical.
Nevertheless I think the final beat could get the industrial crowd moving.