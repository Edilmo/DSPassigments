
import numpy as np

N = 512
MAX_VALUE_DB = np.float(96.0)
MIN_VALUE = np.float(1.0e-05)

def scaled_fft_db(x):
    """ ASSIGNMENT 1

        Computes the FFT of the input buffer windowed by a Hann window, scales
        the output so that the maximum is at 96 dB. The output should be in
        decibels.

        Arguments:
        x:  a 512-point audio data buffer

        Returns:
        X: The FFT of x (windowed by Hanning window) in dB, scaled to have maximum at 96 dB.
        a 257-point array of spectral magnitude values in dBs, normalized to 96dB.
    """

    # Window the input signal by a Hanning window, i.e. compute y[n]=x[n]w[n] where x[n] is a Hanning window defined as
    #       w[n]=(c/2).(1-cos(2.Pi.n/(N-1)))
    #   N is the length of the window (512 in our case) and c is a constant such that Sum(w[n]pow2)=511
    w = compute_hanning_window()
    y = np.multiply(x,w)
    # Compute the Fourier transform of the windowed input. To do so, use the appropriate FFT function from numpy
    y = np.fft.fft(y)
    # Normalize the FFT output by the size of input (i.e. divide by 512)
    y = np.divide(y,N)
    # Since the input data is real-valued, we need only half of the magnitude spectrum, so just keep the first 257 values and take the magnitude
    y = y[0:((N/2)+1)]
    y = np.absolute(y)
    # Convert the magnitude to dBs, |X[k]|dB=20log10|X[k]|; to avoid numerical warnings, if the original magnitude is zero, set the value in dBs to -100dB
    for i in range(0, len(y)):
        if y[i] < MIN_VALUE:
            y[i] = MIN_VALUE
    y = np.multiply(np.log10(y),20)
    # Rescale the output so that the maximum value is 96dB. Remember that rescaling in a log scale is a simple addition!
    m = np.max(y)
    m = m - MAX_VALUE_DB
    y = y - m
    return y


def compute_hanning_window():
    w = np.zeros(N)
    for i in range(0,N):
        w[i] = ((2*np.pi*i)/(N-1))
    w = 1 - np.cos(w)
    c = np.sqrt((511*4)/np.sum(np.square(w)))
    c /= 2
    w = np.multiply(w,c)
    return w



