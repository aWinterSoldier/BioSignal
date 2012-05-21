#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

from filter import BandstopFilter,  HighpassFilter
from data import DataPreparator
from plotting import SignalPlotter
from analysis import EogAnalyser

if __name__ == '__main__':
    # configure option parser
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
            default = 128.0,
            help = "Data registration frequency.")
    bipolar = True


    # parse command-line arguments, exits when fatal error
    options, args = parser.parse_args()

    if not options.input_file:
        print "Input file required; type -h for help."
        exit(-1)

    ## construct main agents
    band_stop       = BandstopFilter(options.frequency, [49,51])
    band_stop2      = BandstopFilter(options.frequency, [99,101])
    high_pass       = HighpassFilter(options.frequency, 2)
    data_preparator = DataPreparator(options,
            [band_stop, band_stop2])
    data_preparator.load_file()
    plotter      = SignalPlotter(data_preparator.prepare_timeline())

    data_preparator.prepare_data()
    data_preparator.apply_filters()

    # plot signal
    signal = data_preparator.montage_signal_set()
    print signal.get_channel(1)
    ######eog_analyser.load_signal_set(signal)

    plotter.plot_set(signal, ylabel = "potential [uV]")

    plotter.show()
