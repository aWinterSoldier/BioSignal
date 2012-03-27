#! /usrbin/python
# -*- coding: utf-8 -*-

import numpy as np

class DataPreparator:
    """
    Responsible for loading raw data and creating data sets for
    future use.
    options -> OptionParser object with command-line options
    filters -> list of filters
    """
    def __init__(self, options, channel_number, max_multiplexed, filters = []):
        self._filters         = filters
        self._channel_number  = channel_number
        self._max_multiplexed = max_multiplexed

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
        max_len = len(self.raw_data) / (self._max_multiplexed * self.frequency)

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
        valid_start = start_frame - (start_frame % self._channel_number)

        start_pos = start_frame * self._max_multiplexed
        end_pos   = (start_frame + frame_number) * self._max_multiplexed

        cut_data  = self.raw_data[start_pos:end_pos]

        self.cut_channels = []
        for n in xrange(self._channel_number):
            self.cut_channels.append(cut_data[n::self._max_multiplexed])

    def apply_filters(self, exclude = []):
        """
        Applies specified filters to all channels.
        """
        def apply_all(channel, ix):
            if ix not in exclude:
                for filt in self._filters:
                    channel = filt.run(channel)
            return channel

        self.cut_channels = [apply_all(c, ix + 1) for ix, c in enumerate(self.cut_channels)]

    def prepare_timeline(self):
        """
        Sets the timeline variable to an X axis timeline array.
        """
        start = self.start_time
        end   = self.start_time + self.duration
        ticks = 1.0 / self.frequency

        return np.arange(start, end, ticks)


    def _signal_difference(self):
        """
        """
        c = self.cut_channels
        return [c[0] - c[1], c[1] - c[0]]

    def _signal_difference_trigger(self, just_trigger):
        """
        """
        c = self.cut_channels
        if just_trigger:
            return [c[0]]
        return [c[0] - c[1], c[1] - c[0], c[2]]

    def raw_signal_set(self):
        return SignalSet(self.cut_channels, self.prepare_timeline(), self._channel_number)

    def difference_signal_set(self):
        return SignalSet(self._signal_difference(), self.prepare_timeline(), self._channel_number)

    def trigger_signal_set(self, just_trigger = False):
        return SignalSet(self._signal_difference_trigger(just_trigger), self.prepare_timeline(), self._channel_number)

class SignalSet:
    """
    Conveys a set of signals in a given representation.
    """
    def __init__(self, channels, timeline, channel_number):
        self._channels = channels
        self._channel_number  = channel_number
        self._timeline = timeline

    def get_channel(self, number):
        """
        Returns a channel under a given index (1 - self._channel_number).
        """
        if number < 1 or number > self._channel_number:
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
