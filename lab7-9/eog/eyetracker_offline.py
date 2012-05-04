#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy

from optparse import OptionParser

from lib.sample_loader import FileLoader
from lib.loader import DataLoader
from lib.filter import BandpassFilter, BandstopFilter, LowpassFilter, HighpassFilter
from lib.analysis import EogAnalyser
from lib.plotting import SignalPlotter

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-i",
            "--input",
            dest = "input_file",
            type = "string",
            help = "Path to raw input file.",
            metavar = "FILE")
    parser.add_option("-s",
            "--start",
            dest = "start_time",
            type = "float",
            default = 0,
            help = "Start second.")
    parser.add_option("-d",
            "--duration",
            dest = "duration",
            type = "float",
            default = -1,
            help = "Data window duration.")
    parser.add_option("-f",
            "--frequency",
            dest = "frequency",
            type = "float",
            default = 256.0,
            help = "Data registration frequency.")

    # parse command-line arguments, exits when fatal error
    options, args = parser.parse_args()

    if not options.input_file:
        print "Input file required; type -h for help."
        sys.exit(-1)

    file_loader  = FileLoader(options)
    eog_analyser = EogAnalyser(options.frequency, 0)
    high_pass    = HighpassFilter(options.frequency, 0.1)
    data_loader  = DataLoader([high_pass],
            2,
            options.frequency)

    data_loader.set_window(64)
    data_loader.set_leftover(4)
    plotter      = SignalPlotter(data_loader.prepare_timeline())

    while True:
        s = file_loader.get_sample()
        if s is None:
            break
        a = numpy.array(s)
        data_loader.load_pack(a)
        signal = data_loader.get_signal_set()

        if signal:
            eog_analyser.load_signal_set(signal)
            print eog_analyser.get_decisions(window = 10,
                    window_seconds = False,
                    jump = 1000,
                    min_sec_diff = 1.5)
            plotter._timeline = data_loader.prepare_timeline()
            plotter.plot_set(signal)
            plotter.show()





