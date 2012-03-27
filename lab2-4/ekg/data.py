#! /usrbin/python
# -*- coding: utf-8 -*-

import numpy as np

CHANNEL_NUMBER = 3

MAX_MULTIPLEXED = 8

class DataPreparator:
    """
    Responsible for loading raw data and creating data sets for
    future use.
    options -> OptionParser object with command-line options
    filters -> list of filters
    """
    def __init__(self, options, filters = []):
        self._filters     = filters

        self.file_name    = options.input_file
        self.start_time   = options.start_time
        self.duration     = options.duration
        self.frequency    = options.frequency

        self.raw_data     = None
        self.cut_channels = None

    def load_file(self):
        """
        Loads the raw data file and calculates a valid duration.
        """
        self.raw_data = np.fromfile(self.file_name)
    
        max_len = len(self.raw_data) / (MAX_MULTIPLEXED * self.frequency)
        
        if self.duration <= 0 or self.duration > max_len:
            self.duration = max_len - self.start_time
            
        if self.duration <= 0:
            raise ValueError("Negative duration, or start time exceeds data length.")

    def prepare_data(self):
        """
        Processes the raw data into channels within specified time
        window.
        """
        start_frame  = self.start_time * self.frequency
        frame_number = self.duration * self.frequency

        # start frame adjusted for channel 1
        valid_start = start_frame - (start_frame % CHANNEL_NUMBER)

        start_pos = start_frame * MAX_MULTIPLEXED
        end_pos   = (start_frame + frame_number) * MAX_MULTIPLEXED

        cut_data  = self.raw_data[start_pos:end_pos]

        self.cut_channels = []
        for n in xrange(CHANNEL_NUMBER):
            self.cut_channels.append(cut_data[n::MAX_MULTIPLEXED])

    def apply_filters(self):
        """
        Applies specified filters to all channels.
        """
        def apply_all(channel):
            for filt in self._filters:
                channel = filt.run(channel)
            return channel

        self.cut_channels = [apply_all(c) for c in self.cut_channels]

    def prepare_timeline(self):
        """
        Sets the timeline variable to an X axis timeline array.
        """
        start = self.start_time
        end   = self.start_time + self.duration
        ticks = 1.0 / self.frequency

        return np.arange(start, end, ticks)

    def _raw_to_einthoven(self):
        """
        Transforms signal from raw to Einthoven representation.
        """
        if not len(self.cut_channels) == 3:
            raise ValueError("Channel number must be equal to 3.")
        c = self.cut_channels
        return [c[0] - c[1], c[2] - c[1], c[2] - c[0]]

    def _raw_to_goldberg(self):
        """
        Transforms signal from raw to Goldberg representation.
        """
        if not len(self.cut_channels) == 3:
            raise ValueError("Channel number must be equal to 3.")
        c = self.cut_channels
        return [c[0] - (c[1] + c[2]) / 2.0, \
                c[1] - (c[0] + c[2]) / 2.0, \
                c[2] - (c[0] + c[1]) / 2.0]


    def raw_signal_set(self):
        return SignalSet(self.cut_channels, self.prepare_timeline())

    def einthoven_signal_set(self):
        return SignalSet(self._raw_to_einthoven(), self.prepare_timeline)

    def goldberg_signal_set(self):
        return SignalSet(self._raw_to_goldberg(), self.prepare_timeline)

class SignalSet:
    """
    Conveys a set of signals in a given representation.
    """
    def __init__(self, channels, timeline):
        self._channels = channels
        self._timeline = timeline

    def get_channel(self, number):
        """
        Returns a channel under a given index (1 - 3).
        """
        if number < 1 or number > CHANNEL_NUMBER:
            raise ValueError("Invalid channel number: %s" % number)
        return self._channels[number - 1]

    def get_channels(self):
        """
        """
        return self._channels

    def get_timeline(self):
        """
        Returns the timeline for the experiment.
        """
        return _timeline
