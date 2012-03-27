#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

class EkgAnalyser:
    """
    Class responsible for signal analysis.
    """
    def __init__(self, frequency, start_time):
        """
        """
        self._frequency  = frequency
        self._start_time = start_time

        self._signal_set = None
        self._threshold_strategy = None

    def load_signal_set(self, signal_set, strategy = None):
        """
        Stores an EKG signal set.
        """
        self._signal_set = signal_set
        if strategy:
            self._threshold_strategy = strategy
        else:
            strategy = {}
            for idx, chann in enumerate(signal_set.get_channels()):
                sig_max = np.max(chann)
                sig_avg = np.median(chann)
                strategy[idx + 1] = sig_max * 0.4 + sig_avg * 0.6

            self._threshold_strategy = strategy

    def inter_peak_diff(self, peaks, seconds = False):
        diffs = []
        for i in xrange(len(peaks) - 1):
            if seconds:
                diffs.append((peaks[i + 1] - peaks[i])/self._frequency)
            else:
                diffs.append(peaks[i + 1] - peaks[i])
        return diffs

    def mean_inter_peak_time(self, peaks, frames = False):
        """
        Returns the mean time between two peaks. The time is
        presented in seconds by default or in frames if the "frames"
        argument is set to True.
        """
        diffs = []
        for i in xrange(len(peaks) - 1):
            diffs.append(peaks[i + 1] - peaks[i])

        frame_mean = np.mean(diffs)
        if frames:
            return frame_mean
        else:
            return frame_mean / self._frequency

    def get_peaks(self, channel, seconds = False):
        """
        """
        peaks = []
        signal = self._signal_set.get_channel(channel)
        threshold = self._threshold_strategy[channel]

        for i in xrange(1, len(signal) - 1):
            if signal[i] > threshold and\
                    signal[i - 1] < signal[i] and\
                    signal[i + 1] < signal[i]:
                if seconds:
                    peaks.append(i / self._frequency + self._start_time)
                else:
                    peaks.append(i)

        return peaks

    def _get_spectrum(self, signal):
        """
        Returns the signal's spectrum in form of a pair
        (frequencies, spectrum).
        """
        spec = np.abs(np.fft.fft(signal)) ** 2
        freq = np.abs(np.fft.fftfreq(len(signal), 1 / self._frequency))
        return freq, spec

    def signal_spectrum(self, channel_number):
        """
        Creates the full signal spectrum of the given channel.
        Returns a 2-tuple: (frequencies, spectrum) ready to
        by plotted on (X, Y).
        """
        signal = self._signal_set.get_channel(channel_number)
        return self._get_spectrum(signal)

    def peak_spectra(self, channel_number, peaks):
        """
        Returns a list of 2-tuples: (frequencies, spectrum)
        for each peak found in the signal.
        """
        signal     = self._signal_set.get_channel(channel_number)
        frame_mean = self.mean_inter_peak_time(peaks, frames = True)
        spectra    = []
        for p in peaks:
            left  = max(0, p - frame_mean / 2.0)
            right = min(len(signal) - 1, p + frame_mean / 2.0)
            spectra.append(self._get_spectrum(signal[left:right]))
        return spectra

    def get_recurrence_pairs(self, channel_number, error):
        """
        """
        signal = self._signal_set.get_channel(channel_number)
        matrix = np.zeros((len(signal), len(signal)))

        for idx1, x1 in enumerate(signal):
            for idx2, x2 in enumerate(signal):
                if abs(x1 - x2) < error:
                    matrix[idx1][idx2] = 1

        return matrix



