#! /usr/bin/python
# -*- coding: utf-8 -*-

from data import DataPreparator

from time import sleep

class FileLoader(DataPreparator):
    """
    """
    def __init__(self, options):
        """
        """
        super(FileLoader, self).__init__(options,
                2,
                2,
                [])
        self.load_file()

        self.to_fetch = list(self.raw_data)

    def get_sample(self):
        if len(self.to_fetch) < self._channel_number:
            return None

        sample = self.to_fetch[:self._channel_number]
        self.to_fetch = self.to_fetch[self._channel_number:]
        sleep(0.01)
        return sample

