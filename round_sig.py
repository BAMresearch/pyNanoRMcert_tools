import numpy as np

def f_round_sig(x, sig=None):
    """Round a number to a chosen number of significant digest. See answer # 47 in
    https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
    """
    if x == 0.:
        return 0.
    return np.round(x, sig-int(np.floor(np.log10(abs(x))))-1)

def f_round_sig_array(items, sig=4):
    """ round the numbers in an array"""
    return np.array([f_round_sig(item, sig) for item in items])
