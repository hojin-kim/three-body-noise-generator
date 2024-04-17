# Three-body noise generator

## Virtual environment

`$ source .venv_3.../bin/activate`

## What I have done so far

### The Three-Body Simulator(TBS)

The Three-Body simulator is now written.
See `threebody.py` and `draw.ipynb` notebook.

The below is something I am planning to do.

## What I am planning to do

### Noise Generator based on TBS

From the Center of Mass, say $O$, we will generate noises of three voices.

* Each voice corresponds to each celestial body.
* At time $t$,
  * The distance from $O$ to the body $A_1$ corresponds to the tone of the voices.
  * The magnitude of the velocity of the body $A_1$ corresponds to the volume of the voice.
