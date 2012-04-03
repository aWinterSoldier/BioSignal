#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import math

class SignalAnalyser(object):
    """
    Class responsible for signal analysis.
    """
    def __init__(self, frequency, start_time):
        """
        """
        self._frequency       = frequency
        self._start_time      = start_time

        self._signal_set = None

    def load_signal_set(self, signal_set):
        """
        Stores a signal set.
        """
        self._signal_set = signal_set

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

    def _mean_from_array(self, array):
        """
        """
        return np.std(array)

    def mean_amplitude(self, channel_number):
        """
        """
        signal = self._signal_set.get_channel(channel_number)
        return self._mean_from_array(signal)

    def get_jump_times(self,
            channel_number,
            jump = 1.6,
            window = 100,
            seconds = False,
            min_sec_diff = 1.0):
        """
        """
        signal = self._signal_set.get_channel(channel_number)
        difference   = min_sec_diff * self._frequency
        last_trigger = -difference - 1

        if window % 2 == 0:
            window += 1
        diameter = (window - 1) / 2
        start = diameter
        end = len(signal) - diameter

        amplitudes = []
        for i in xrange(start, end):
            part = signal[i - diameter:i + diameter]
            amplitudes.append(self._mean_from_array(part))

        mean_amp = np.std(amplitudes)

        threshold = mean_amp * jump

        times = []
        for i in xrange(1, len(amplitudes)):
            if amplitudes[i - 1] <= threshold and\
                    amplitudes[i] > threshold and\
                    i - last_trigger > difference:
                last_trigger = i
                frame = i + diameter
                if seconds:
                    times.append((frame / self._frequency) + self._start_time)
                else:
                    times.append(frame)
        return times

    def get_mean_std(self, data):
        """
        """
        return np.mean(data), np.std(data)


class EogAnalyser(SignalAnalyser):
    """
    """
    def __init__(self, frequency, start_time):
        """
        """
        self._directions = ["l", "r", "u", "d"]
        super(EogAnalyser, self).__init__(frequency, start_time)


    def get_decisions(self,
            jump = 1000,
            window = 100,
            window_seconds = False,
            seconds = False,
            min_sec_diff = 0.5):
        """
        """
        hor = self._signal_set.get_channel(1)
        ver = self._signal_set.get_channel(2)

        if window_seconds:
            window = int(window * self._frequency)

        if window % 2 == 0:
            window += 1
        diameter = (window - 1) / 2
        start = diameter
        end = len(hor) - diameter
        step = diameter / 2

        hvalues = []
        vvalues = []
        hmeans  = []
        vmeans  = []
        times = []
        for i in xrange(start, end, step):
            hpart = hor[i - diameter:i + diameter]
            vpart = ver[i - diameter:i + diameter]

            times.append(i / self._frequency)
            hmean, hstd = self.get_mean_std(hpart)
            vmean, vstd = self.get_mean_std(vpart)
            hvalues.append(hstd)
            vvalues.append(vstd)
            hmeans.append(hmean)
            vmeans.append(vmean)

        print hvalues
        print vvalues

        decisions = []
        difference   = min_sec_diff * self._frequency
        last_v = -difference - 1
        last_h = -difference - 1
        for i in xrange(1, len(times)):
            time = times[i]

            if hvalues[i] - hvalues[i - 1] > jump and i - difference > last_h:
                last_h = i
                if hmeans[i] > hmeans[i - 1]:
                    decisions.append(("l", time))
                else:
                    decisions.append(("r", time))

            if vvalues[i] - vvalues[i - 1] > jump and i - difference > last_v:
                last_v = i
                if vmeans[i] > vmeans[i - 1]:
                    decisions.append(("u", time))
                else:
                    decisions.append(("d", time))

        return decisions
