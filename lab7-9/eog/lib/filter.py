#! /usr/bin/python
# -*- coding: utf-8 -*-

from scipy.signal import filtfilt, cheby2

import numpy as np

class AbstractSignalFilter(object):
    """
    Abstract class representing a runnable signal filter.
    """
    def run(self, channel):
        """
        Method stub for running the filter on a channel.
        It returns a modified (filtered) version of that channel.
        """
        self.a = None
        self.b = None
        raise NotImplementedError("Abstract class")

    def run(self, channel):
        """
        """
        return filtfilt(self.b, self.a, channel)

class BandstopFilter(AbstractSignalFilter):
    """
    Banstop filter of Chebyshev type.
    """
    def __init__(self, frequency, band):
        """
        """
        fn = frequency / 2.0
        b, a = cheby2(1, 10, np.array(band) / fn, btype = "bandstop")

        self.b = b
        self.a = a

class BandpassFilter(AbstractSignalFilter):
    """
    """
    def __init__(self, frequency, band):
        """
        """
        fn = frequency / 2.0
        b, a = cheby2(1, 10, np.array(band)/ fn, btype = "bandpass")

        self.b = b
        self.a = a

class HighpassFilter(AbstractSignalFilter):
    """
    """
    def __init__(self, frequency, threshold):
        """
        """
        fn = frequency / 2.0
        b, a = cheby2(1, 10, threshold / fn, btype = "highpass")

        self.b = b
        self.a = a

class LowpassFilter(AbstractSignalFilter):
    """
    """
    def __init__(self, frequency, threshold):
        """
        """
        fn = frequency / 2.0
        b, a = cheby2(1, 10, threshold / fn, btype = "lowpass")

        self.b = b
        self.a = a
