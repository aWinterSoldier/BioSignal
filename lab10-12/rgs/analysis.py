#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import math

from time import sleep

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

    def get_last_and_range(self, data):
        """
        """
        return np.argmax(data) - np.argmin(data), \
            np.max(data) - np.min(data)
            
    def get_max_and_range(self, data):
        """
        """
        max_abs = max(np.max(data), np.abs(np.min(data)))
        return max_abs, \
            np.max(data) - np.min(data)

class GSRAnalyser(SignalAnalyser):
    """
    """
    def __init__(self, frequency, start_time):
        """
        """
        self._trigger_channel = 3
        self.emo_reactions = []
        super(GSRAnalyser, self).__init__(frequency, start_time)

    def load_emo_reactions(self, filename, seconds = True):
        """
        """
        trigger_times = self.get_trigger_times(seconds = seconds, 
                min_sec_diff = 3)
        line = None
        with open(filename, 'r') as f:
            line = f.readline()
        line = line[1:-2].replace("'", '')
        reactions = line.split(", ")
        if not len(trigger_times) == len(reactions):
            print len(trigger_times), len(reactions)
            print "Warning: Trigger times don't match responses in file."
        return zip(reactions, trigger_times)
      
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
        
        
    def get_decisions(self,
            filename,
            jump = 500,
            window = 20,
            window_seconds = False,
            seconds = False,
            min_sec_diff = 0.5):
        """
        """
        gsr = self._signal_set.get_channel(1)
        emo_reactions = self.load_emo_reactions(filename, seconds = False)
        
        trigger_times = [y for (x, y) in emo_reactions]
        
        if window_seconds:
            window = int(window * self._frequency)

        if window % 2 == 0:
            window += 1
        diameter = (window - 1) / 2
        start = diameter
        end = len(gsr) - diameter
        step = diameter / 2

        gsr_values = []
        frames = []
        for i in xrange(start, end, step):
            gsr_part = gsr[i - diameter:i + diameter]

            frames.append(i)
            gsr_max, gsr_range = self.get_max_and_range(gsr_part)
            gsr_values.append(gsr_range)

        values = zip(frames, gsr_values)
        def printf(x):
            print x
        #map(printf, [x for x in zip(times, hvalues, vvalues)])

        decisions = {"increase": [], "peak": []}
        
        #print trigger_times
        #print values

        if len(trigger_times) == 0:
            return decisions
        
        # remove all values before first trigger 
        first_trigger = trigger_times[0]
        first_value = 0
        while values[first_value][0] < first_trigger:
            first_value += 1
        values = values[first_value:]
        
        trg_idx = 0
        val_idx = 0
        
        peak_values = []
        incr_values = []
        new_peak = False
        new_incr = False
        remaining_triggers = True
        #print trigger_times, values
        
        while val_idx < len(values):
            if trg_idx < len(trigger_times):
                trg_frame = trigger_times[trg_idx]
            else:
                remaining_triggers = False
            val_frame, val = values[val_idx]
            gsr_idx = val_idx * step + first_trigger
            if remaining_triggers and val_frame >= trg_frame:
                # analysing new trigger
                new_peak = True
                new_incr = True
                trg_idx += 1
            
            if new_incr and val > jump:
                new_incr = False
                incr_values.append((float(val_frame) / self._frequency, abs(gsr[gsr_idx])))
            
            
            if new_peak and val_idx > 0 and val_idx < len(values) - 1 and not new_incr:
                prev_idx = gsr_idx - step
                next_idx = gsr_idx + step
                #print prev_idx, gsr_idx, next_idx, gsr[prev_idx], gsr[gsr_idx], gsr[next_idx]
                if abs(gsr[gsr_idx]) > abs(gsr[prev_idx]) and\
                        abs(gsr[gsr_idx]) > abs(gsr[next_idx]):
                    new_peak = False
                    peak_values.append((float(val_frame) / self._frequency, abs(gsr[gsr_idx])))
            
            val_idx += 1

        decisions["increase"] = incr_values
        decisions["peak"] = peak_values
        return decisions
