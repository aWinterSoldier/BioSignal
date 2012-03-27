#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

from filter import BandpassFilter, BandstopFilter
from data import DataPreparator
from plotting import SignalPlotter
from analysis import EmgAnalyser
from numpy import ones

def parse_cross_times(filename, xstart):
    """
    """
    times = []
    with open(filename) as f:
        for time in f:
            if len(time) > 0:
                times.append(float(time) - xstart)
    return times

if __name__ == '__main__':
    # configure option parser
    parser = OptionParser()
    modes = ["simple", "trigger", "file"]

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
            default = 1024.0,
            help = "Data registration frequency.")
    parser.add_option("-c",
            "--channel",
            dest = "channel",
            type = "int",
            default = 1,
            help = "Channel number for analysis.")
    parser.add_option("-m",
            "--mode",
            dest = "mode",
            type = "choice",
            choices = modes,
            default = "simple",
            help = "Program mode.")
    parser.add_option("-x",
            "--file",
            dest = "xfile",
            type = "string",
            help = "Path to cross experiment file.",
            metavar = "FILE")
    parser.add_option("-b",
            "--experiment_start_second",
            dest = "xstart",
            type = "float",
            default = 0.0,
            help = "Start second of cross experiment.")


    # parse command-line arguments, exits when fatal error
    options, args = parser.parse_args()
    options.channel = options.channel

    if options.mode == "trigger":
        channel_number = 3
        max_multiplexed = 3
        emg_analyser = EmgAnalyser(options.frequency, options.start_time, 3)
    elif options.mode == "simple":
        channel_number = 2
        max_multiplexed = 2
        emg_analyser = EmgAnalyser(options.frequency, options.start_time, 3)
    else:
        channel_number = 1
        max_multiplexed = 1
        emg_analyser = EmgAnalyser(options.frequency, options.start_time, 1)

    if not options.input_file:
        print "Input file required; type -h for help."
        exit(-1)

    ## construct main agents
    bandpass_filter = BandpassFilter(options.frequency, [20, 180])
    data_preparator = DataPreparator(options,
            channel_number,
            max_multiplexed,
            [bandpass_filter])
    data_preparator.load_file()
    plotter      = SignalPlotter(data_preparator.prepare_timeline())

    data_preparator.prepare_data()
    if options.mode == "trigger":
        data_preparator.apply_filters(exclude = [3])
    elif options.mode == "simple":
        data_preparator.apply_filters()
    else:
        data_preparator.apply_filters(exclude = [1])

    print "Analysing channel %s\n" % options.channel

    # plot signal
    if options.mode == "trigger":
        signal = data_preparator.trigger_signal_set()
    elif options.mode == "simple":
        signal = data_preparator.difference_signal_set()
    else:
        signal = data_preparator.trigger_signal_set(just_trigger = True)
    emg_analyser.load_signal_set(signal)

    plotter.plot_set(signal, ylabel = "potential [uV]")

    print "Mean amplitude: %s [uV]" % emg_analyser.mean_amplitude(options.channel)

    # plot full spectrum
    freq, spec = emg_analyser.signal_spectrum(options.channel)
    plotter.plot_channel(spec,
            xaxis = freq,
            xlabel = "frequency [Hz]",
            ylabel = "magnitude [(uV s) ^ 2]",
            title = "EMG spectrum")

    if options.mode in ["trigger", "file"]:
        trigger_moments = emg_analyser.get_trigger_times(seconds = True)
        emg_moments = emg_analyser.get_emg_times(options.channel,
                window = 10,
                jump = 2.0,
                min_sec_diff = 0.3,
                seconds = True)
        if options.mode == "trigger":
            times = emg_analyser.get_time_differences(trigger_moments,
                    emg_moments,
                    max_allowed = 0.3,
                    full_info = True)
            print "Matched times: %s" % len(times)
            all_positive = all(map(lambda x: x > 0, times))
            if not all_positive:
                print "Found negative instances."
            mean, std = emg_analyser.get_mean_std(times)
            print "Mean difference: %s s" % mean
            print "Standard deviation: %s s" % std
        else:
            xfile = options.xfile
            press = parse_cross_times(options.xfile, options.xstart)
            times = emg_analyser.get_time_differences(trigger_moments,
                    press,
                    max_allowed = 2.0,
                    full_info = True)
            mean, std = emg_analyser.get_mean_std(times)
            print "Mean reaction time: %s s" % mean
            print "Standard deviation: %s s" % std

        plotter.draw_histogram(times,
                xlabel = "trigger delay [s]",
                ylabel = "values",
                title = "Trigger delay histogram")

    plotter.show()
