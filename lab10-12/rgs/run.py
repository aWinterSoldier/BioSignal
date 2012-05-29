#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from optparse import OptionParser
from sys import exit

from filter import BandstopFilter,  HighpassFilter
from data import GSRDataPreparator, NameGSRDataPreparator
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
    dec_dict = analyser.get_decisions(options.decision_file, jump = 100)
    increase = dec_dict["increase"]
    peaks    = dec_dict["peak"]
    half     = dec_dict["half"]
    print len(triggers), triggers
    print len(increase), increase
    print len(peaks), peaks
    print len(half), half

    emo_amps = []
    emo_lats = []
    emo_grow = []
    emo_half = []

    neu_amps = []
    neu_lats = []
    neu_grow = []
    neu_half = []
    for i in xrange(len(triggers)):
        t = triggers[i][1]
        if peaks[i] is not None:
            if triggers[i][0] == 'n':
                # neutral
                neu_amps.append(peaks[i][1])
                neu_lats.append(increase[i][0] - t)
                neu_grow.append(peaks[i][0] - increase[i][0])
                neu_half.append(half[i])
            else:
                #emo
                emo_amps.append(peaks[i][1])
                emo_lats.append(increase[i][0] - t)
                emo_grow.append(peaks[i][0] - increase[i][0])
                emo_half.append(half[i])

    print emo_grow
    emo_grow.pop(3)
    emo_grow.pop(4)
    print emo_grow
    print "Emo:"
    print "Amplitude: %.2f | %.2f" % (np.mean(emo_amps), np.max(emo_amps))
    print "Latency: %.2f | %.2f" % (np.mean(emo_lats), np.max(emo_lats))
    print "Growth time: %.2f | %.2f" % (np.mean(emo_grow), np.max(emo_grow))
    print "Half life: %.2f | %.2f" % (np.mean(emo_half), np.max(emo_half))

    print "Neutral:"
    print "Amplitude: %.2f | %.2f" % (np.mean(neu_amps), np.max(neu_amps))
    print "Latency: %.2f | %.2f" % (np.mean(neu_lats), np.max(neu_lats))
    print "Growth time: %.2f | %.2f" % (np.mean(neu_grow), np.max(neu_grow))
    print "Half life: %.2f | %.2f" % (np.mean(neu_half), np.max(neu_half))

    print "\n\n"
    print emo_half, np.mean(emo_half)
    print neu_half, np.mean(neu_half)

    plotter.plot_set(signal, ylabel = "potential [uV]")
    plotter.plot_channel(signal.get_channel(1),
                         triggers = triggers,
                         slopes = increase,
                         peaks = peaks,
                         ylabel = "potential [uV]",
                         title = "Hand electrode")

    plotter.show()
