#! /usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

from plotting import SignalPlotter
from filter import BandstopFilter, HighpassFilter
from data import DataPreparator, MAX_MULTIPLEXED, CHANNEL_NUMBER
from analysis import EkgAnalyser
from numpy import ones

if __name__ == '__main__':
    represntations = ["raw", "einthoven", "goldberg"]
    channels = map(str, xrange(1, CHANNEL_NUMBER + 1))

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
    parser.add_option("-r",
            "--representation",
            dest = "representation",
            type = "choice",
            default = "raw",
            choices = represntations,
            help = "Signal representation: raw/goldberg/einthoven")
    parser.add_option("-c",
            "--channel",
            dest = "channel",
            type = "choice",
            default = 1,
            choices = channels,
            help = "Channel number for analysis.")
    parser.add_option("-e",
            "--recurrence",
            dest = "recurrence",
            action = "store_true",
            default = False,
            help = "Plots recurrence charts.")

    # parse command-line arguments, exits when fatal error
    options, args = parser.parse_args()
    options.channel = int(options.channel)

    if not options.input_file:
        print "Input file required; type -h for help."
        exit(-1)

    ## construct main agents
    bandstop_filter = BandstopFilter(options.frequency, [49, 51])
    highpass_filter = HighpassFilter(options.frequency, 0.5)
    data_preparator = DataPreparator(options, [bandstop_filter,
        highpass_filter])
    data_preparator.load_file()

    ekg_analyser    = EkgAnalyser(options.frequency, data_preparator.start_time)
    plotter         = SignalPlotter(data_preparator.prepare_timeline())

    data_preparator.prepare_data()
    data_preparator.apply_filters()

    print "%s representation" % options.representation.capitalize()
    print "Analysing channel %s\n" % options.channel

    # plot signal
    if options.representation == "raw":
        signal = data_preparator.raw_signal_set()
    elif options.representation == "einthoven":
        signal = data_preparator.einthoven_signal_set()
    elif options.representation == "goldberg":
        signal = data_preparator.goldberg_signal_set()

    ekg_analyser.load_signal_set(signal)

    data = {}
    for chann in xrange(1, 4):
        data[chann] = []

    for chann, value in ekg_analyser._threshold_strategy.items():
        data[chann].append((plotter._timeline,
                ones(len(plotter._timeline)) * value,
                False))

    for chann in xrange(1, 4):
        xdata = ekg_analyser.get_peaks(chann, seconds = True)
        xdata_frames = ekg_analyser.get_peaks(chann)
        ydata = signal.get_channel(chann)[xdata_frames]
        data[chann].append((xdata, ydata, True))

    plotter.plot_set(signal, extra_info = data)
    # einthoven test
    einthoven  = data_preparator.einthoven_signal_set()
    chann_list = [einthoven.get_channel(1) + einthoven.get_channel(3),
            einthoven.get_channel(2)]
    plotter.plot_channel_list(chann_list, title_list = ["Einthoven: I + III",
        "Einthoven: II"])


    ## Analysing channel
    # peaks
    peaks = ekg_analyser.get_peaks(options.channel)

    ##Difference plot - beats
    peaks_sec = ekg_analyser.get_peaks(options.channel, seconds = True)
    y1 = ekg_analyser.inter_peak_diff(peaks, seconds = True)
    plotter.plot_channel(y1,
        xaxis = peaks_sec[1:],
        ylabel = 'Roznica [s]',
        point_plot = 'x')

    ##Difference plot - beats
    beats = range(1, len(y1) + 1)
    plotter.plot_channel(y1,
        xaxis = beats,
        xlabel = 'uderzenia serca [1]',
        ylabel = 'Roznica [s]',
        point_plot = 'x')


    print "Peak number: ", len(peaks)
    inter_peak = ekg_analyser.mean_inter_peak_time(peaks)
    print "Mean inter-peak time: %s s" % inter_peak
    print "Mean heart-rate: %s beat/min" % (60.0 / inter_peak)

    # plot second peak's spectrum
    if len(peaks) > 2:
        spectra = ekg_analyser.peak_spectra(options.channel, peaks)
        freq, spec = spectra[1]
        plotter.plot_channel(spec,
                xaxis = freq,
                xlabel = "frequency [Hz]",
                ylabel = "magnitude",
                title = "Second peak spectrum")

    # plot full spectrum
    freq, spec = ekg_analyser.signal_spectrum(options.channel)
    plotter.plot_channel(spec,
            xaxis = freq,
            xlabel = "frequency [Hz]",
            ylabel = "magnitude",
            title = "EKG spectrum")

    if options.recurrence:
        pairs = ekg_analyser.get_recurrence_pairs(options.channel, 100)
        plotter.plot_pairs(pairs)

    plotter.show()
