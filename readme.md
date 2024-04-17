## Three body noise generator

`$ source .venv_3.../bin/activate`

### Three body simulator

Three body simulator is now written.
See `threebody.py` and `draw.ipynb` notebook.

### Noise generator 

From the Center of Mass, say $O$, we will generate noises of three voices. 

* Each voice corresponds to each celestial body.
* At time $t$, 
    * Distance from $O$ to the body $A_1$ corresponds to the tone of the voice. 
    * Magnitude of velocity of the body $A_1$ corresponds to the volume of the voice.