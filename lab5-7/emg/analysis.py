#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import math

class EmgAnalyser:
    """
    Class responsible for signal analysis.
    """
    def __init__(self, frequency, start_time, trigger_channel):
        """
        """
        self._frequency       = frequency
        self._start_time      = start_time
        self._trigger_channel = trigger_channel

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

    def get_trigger_times(self,
            seconds = False,
            min_sec_diff = 0.5):
        """
        """
        trigger      = self._signal_set.get_channel(self._trigger_channel)
        difference   = min_sec_diff * self._frequency
        last_trigger = -difference - 1
        times        = []
        for i in range(1, len(trigger)):
            if trigger[i - 1] < trigger[i] and\
                    i - last_trigger > difference:
                last_trigger = i
                if seconds:
                    times.append((i / self._frequency) + self._start_time)
                else:
                    times.append(i)
        return times

    def get_emg_times(self,
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
        print "Threshold: ", threshold

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

    def get_time_differences(self,
            trg,
            emg,
            max_allowed = 0.5,
            warning = True,
            full_info = False):
        """
        """
        result = []
        t, e = 0, 0
        while t < len(trg) and e < len(emg):
            if (abs(trg[t] - emg[e]) < max_allowed):
                if full_info:
                    print "Matched trigger %s with emg %s, difference: %s" %\
                        (trg[t], emg[e], (trg[t] - emg[e]))
                result.append(trg[t] - emg[e])
                t += 1
                e += 1
            else:
                if warning:
                    print "Cannot match event times: trigger %s and emg %s" %\
                            (trg[t], emg[e])
                if trg[t] < emg[e]:
                    t += 1
                else:
                    e += 1
        if warning and t != e:
            print "%s unmatched element(s) remained" % abs(t - e)
        return result

    def get_mean_std(self, data):
        """
        """
        return np.mean(data), np.std(data)
