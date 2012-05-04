#! /usrbin/python
# -*- coding: utf-8 -*-
from __future__ import division
from data import SignalSet

import numpy as np

class DataLoader(object):
    """
    """
    def __init__(self,
            filters,
            channel_number,
            frequency):
        """
        """
        self.filters        = filters
        self.channel_number = channel_number
        self.frequency      = frequency

        self.data_buffer    = []
        self.data_filter    = []
        self.signal_set     = None
        self.window         = 128
        self.leftover       = 16
        self.ready          = False

        self.time           = 0.0

        for i in xrange(channel_number):
            self.data_buffer.append(np.array([]))

    def set_window(self, window):
        """
        """
        self.window = window

    def set_leftover(self, leftover):
        """
        """
        self.leftover = leftover
        
    def load_pack(self, pack):
        """
        """
        channel = 0
        for val in pack:
            self.data_buffer[channel] = np.concatenate((self.data_buffer[channel],
                    np.array([val])))
            channel += 1
            channel %= self.channel_number
            if channel % self.channel_number == 0:
                self.time += 1.0 / self.frequency

        all_done = True
        for c in xrange(self.channel_number):
            all_done = all_done and (len(self.data_buffer[c]) >= self.window)
            if len(self.data_buffer[c]) > self.window:
                self.data_buffer[c] = self.data_buffer[c][-self.window:]

        self.ready = all_done

    def get_signal_set(self):
        """
        """
        signal_set = None
        if self.ready:
            self.ready = False

            self.data_filter = self.data_buffer
            self.apply_filters()
            signal_set = self.montage_signal_set()

            for c in xrange(self.channel_number):
                self.data_buffer[c] = self.data_buffer[c][-self.leftover:]

        return signal_set

    def apply_filters(self, exclude = []):
        """
        Applies specified filters to all channels.
        """
        def apply_all(channel, ix):
            if ix not in exclude:
                for filt in self.filters:
                    channel = filt.run(channel)
            return channel
        self.data_filter = [apply_all(c, ix + 1) for ix, c in enumerate(self.data_filter)]

    def prepare_timeline(self):
        """
        Sets the timeline variable to an X axis timeline array.
        """
        start = self.time - float(self.window) / self.frequency
        end   = self.time
        ticks = 1.0 / self.frequency

        return np.arange(start, end, ticks)

    def _bipolar_montage(self):
        """
        """
        return self.data_filter

    def montage_signal_set(self):
        """
        """
        montage = self._bipolar_montage()
        return SignalSet(montage,
                self.prepare_timeline(),
                self.channel_number)

