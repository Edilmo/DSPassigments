
import numpy as np

def quantization(sample, sf, ba, QCa, QCb):
    """ ASSIGNMENT 4

        Arguments:
        sample: the sample to quantize
        sf:     the scale factor
        ba:     the bit allocation
        QCa:    the multiplicative uniform quantization parameter
        QCb:    the additive uniform quantization parameter

        Returns:
        The uniformly quantized sample.
    """

    #
    q = np.floor(np.multiply(((np.multiply(QCa,(sample/sf)))+QCb),np.power(2.0,(ba-1))))
    return q


