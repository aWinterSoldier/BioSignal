#! /usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from sys import exit

import pylab as py


# returns (I, II, III)
def rawToEinthoven(left, right, foot):
    return (left -right, foot - right, foot - left)

def rawToGoldberg(left, right, foot):
    return (left -(right+foot)/2.0, \
           right- (foot+left)/2.0,          \
           foot - (left+right)/2.0)

def prepare_data(options):
    """
    The function receives an option parser object with all
    command-line parameters and produces a list of numpy
    data arrays for each channel.
    """
    raw_data = np.fromfile(options.input_file)

    start_frame = options.start_time * options.frequency
    frame_number = options.duration * options.frequency

    # start frame number adjusted for channel 0
    adjusted_start = start_frame - (start_frame % options.channel_number)

    start_pos = start_frame * MAX_MULTIPLEXED
    end_pos = (start_frame + frame_number) * MAX_MULTIPLEXED

    if options.duration < 1:
        end_pos = len(raw_data)

    cut_data = raw_data[start_pos:end_pos]

    result_arrays = []
    for n in xrange(options.channel_number):
        result_arrays.append(cut_data[n::MAX_MULTIPLEXED])

    return result_arrays

def prepare_figure(time, channels):
    """
    """
    plot_num = len(channels)
    py.figure()

    for idx, chann in enumerate(channels):
        py.subplot(plot_num, 1, idx + 1)
        py.plot(time, chann)

def prepare_timeline(options, data_len):
    """
    The function creates a timeline for the X axis of the
    experiment data from the command-line options.
    """
    start_time = options.start_time
    if options.duration > 0:
        end_time = options.start_time + options.duration
    else:
        end_time = data_len / 128.0
    ticks = 1.0 / options.frequency
    print start_time, end_time, ticks
    return np.arange(start_time, end_time, ticks)

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

    options, args = parser.parse_args()

    if not options.input_file:
        print "Input file required; type -h for help."
        exit(-1)

    if options.channel_number > MAX_MULTIPLEXED:
        print "Maximum allowed channel number is %s." % MAX_MULTIPLEXED
        exit(-1)


    chann1, chann2, chann3 = prepare_data(options)

    time = prepare_timeline(options, len(chann1))
    print len(time), len(chann1), len(chann2), len(chann3)

    prepare_figure(time, [chann1, chann2, chann3])
    prepare_figure(time, rawToEinthoven(chann1, chann2, chann3))

    py.show()
