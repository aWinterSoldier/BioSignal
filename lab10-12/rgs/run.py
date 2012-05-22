#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

from filter import BandstopFilter,  HighpassFilter
from data import GSRDataPreparator
from plotting import SignalPlotter
from analysis import GSRAnalyser

if __name__ == '__main__':
    # configure option parser
    parser = OptionParser()

    parser.add_option("-i",
            "--input",
            dest = "input_file",
            type = "string",
            help = "Path to raw input file.",
            metavar = "FILE")
    parser.add_option("-x",
            "--decision-file",
            dest = "decision_file",
            type = "string",
            help = "Path to decision file.",
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
    high_pass       = HighpassFilter(options.frequency, 0.1)
    data_preparator = GSRDataPreparator(options,
            [band_stop, high_pass])
    data_preparator.load_file()
    plotter      = SignalPlotter(data_preparator.prepare_timeline())

    data_preparator.prepare_data()
    data_preparator.apply_filters(exclude = [3])

    signal = data_preparator.montage_signal_set()
    
    analyser = GSRAnalyser(options.frequency, options.start_time)
    analyser.load_signal_set(signal)

    triggers = analyser.load_emo_reactions(options.decision_file)
    dec_dict = analyser.get_decisions(options.decision_file, jump = 300)
    increase = dec_dict["increase"]
    peaks    = dec_dict["peak"]
    print triggers
    print increase
    print peaks
    
    
    
    
    
    # plot signal
    
    ######eog_analyser.load_signal_set(signal)

    plotter.plot_set(signal, ylabel = "potential [uV]")

    plotter.show()
