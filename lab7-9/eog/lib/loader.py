#! /usrbin/python
# -*- coding: utf-8 -*-

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
        self.frequency      = options.frequency

        self.data_buffer    = []
        self.signal_set     = None
        self.window         = 128
        self.ready          = False

        for i in xrange(channel_number):
            self.data_buffer.append([])

    def set_window(self, window):
        """
        """
        self.window = window

    def load_pack(self, pack):
        """
        """
        channel = 0
        for val in pack:
            self.data_buffer[channel].append(val)
            channel += 1
            channel %= self.channel_number

        all_done = True
        for c in xrange(self.channel_number):
            all_done = all_done and (len(self.data_buffer[c]) >= self.window)
            if len(self.data_buffer[c] > self.window):
                self.data_buffer[c] = self.data_buffer[c][-self.window:]

        self.ready = all_done

    def get_signal_set(self):
        """
        """
        signal_set = None
        if self.ready:
            self.apply_filters()
            signal_set = self.montage_signal_set()
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
        for x in enumerate(self.data_buffer):
            print x
        self.data_buffer = [apply_all(c, ix + 1) for ix, c in enumerate(self.data_buffer)]

    def _bipolar_montage(self):
        """
        """
        return self.cut_channels

    def montage_signal_set(self):
        """
        """
        montage = self._bipolar_montage()
        return SignalSet(montage,
                self.prepare_timeline(),
                self._channel_number)
