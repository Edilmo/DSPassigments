
import numpy as np

def prototype_filter():
    """ ASSIGNMENT 2

        This function compute the prototype filter h[n] with
        following characteristics:

        - Each subband filter is based on prototype filter h[n] with the following characteristics:
            * Low-pass filter
            * Bandwidth fs/32
            * Cutoff frequency of fs/64 at -3dB
            * FIR

        Returns:
        h[n]
    """

    # You can use the remez routine. The documentation can be found at
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    from scipy.signal import remez

    return remez(512, [0.0, (1.0/(128.0*2.0)), (1.0/(32.0*2.0)), (1.0/2.0)], [2.0, 0.0])


