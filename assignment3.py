
import numpy as np

N = 32

def subband_filtering(x, h):
    """ ASSIGNMENT 3

        Write a routine to implement the efficient version of the subband filter.

        Arguments:
        x:  The length 512 buffer, in time-reversed order e.g. [x[n],x[n-1],...,x[n-511]].
        the 512-point buffer, already updated with 32 new samples and time-reversed
        h:  The prototype filter of the filter bank.
        the 512-point prototype FIR impulse response you computed in the previous assignment

        Returns:
        s: The 32 new output samples of the filter bank.
    """

    # the buffer is already updated and time reversed, so the newest samples are first
    # compute r[k]=h[k]x[k], k=0,...,511
    r = np.multiply(h,x)
    # compute c[q]=SumFromPequeal0to7((-1)powP.r[q+64.P]) ; q=0....63
    c = np.zeros(2*N)
    for q in range(0,len(c)):
        for p in range(0,8):
            c[q] += (np.power((-1.0),p)*r[q+(64*p)])
    # compute the subband outputs as s[i]=SumFromQequal0to63(cos((np.PI/64).(2i+1).(Q-16))) for i=0..31
    s = np.zeros(N)
    for i in range(0,len(s)):
        for q in range(0,64):
            s[i] += (np.cos((np.pi/64)*((2*i)+1)*(q-16))*c[q])
    return s