#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

from filter import BandpassFilter, BandstopFilter, LowpassFilter, HighpassFilter
from data import EogDataPreparator
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
            default = 256.0,
            help = "Data registration frequency.")
    bipolar = True


    # parse command-line arguments, exits when fatal error
    options, args = parser.parse_args()

    if not options.input_file:
        print "Input file required; type -h for help."
        exit(-1)

    ## construct main agents
    eog_analyser    = EogAnalyser(options.frequency, options.start_time)
    high_pass       = HighpassFilter(options.frequency, 0.1)
    data_preparator = EogDataPreparator(options,
            [high_pass])
    data_preparator.load_file()
    plotter      = SignalPlotter(data_preparator.prepare_timeline())

    data_preparator.prepare_data()
    data_preparator.apply_filters()

    # plot signal
    signal = data_preparator.montage_signal_set()
    eog_analyser.load_signal_set(signal)

    plotter.plot_set(signal, ylabel = "potential [uV]")

    # print "Mean amplitude: %s [uV]" % eog_analyser.mean_amplitude(1) #TODO: change

    # plot full spectrum
   # freq, spec = eog_analyser.signal_spectrum(1) #TODO: change
   # plotter.plot_channel(spec,
   #         xaxis = freq,
   #         xlabel = "frequency [Hz]",
   #         ylabel = "magnitude [(uV s) ^ 2]",
   #         title = "EMG spectrum")

    print eog_analyser.get_decisions(window = 0.3,
            window_seconds = True,
            jump = 1200,
            min_sec_diff = 1.5)
    plotter.show()
