#! /usr/bin/python
# -*- coding: utf-8 -*-

import pylab as py

class SignalPlotter(object):
    """
    """
    def __init__(self, timeline):
        """
        """
        self._timeline = timeline
        self._figure_done = False

    def _prepare_axes(self, xlabel, ylabel, title):
        """
        """
        py.xlabel(xlabel)
        py.ylabel(ylabel)
        py.title(title)

    def _prepare_figure(self):
        """
        """
        if self._figure_done:
            py.figure()

    def plot_set(self,
            signal_set,
            xaxis = None,
            xlabel = "time [s]",
            ylabel = "",
            ylim = None,
            extra_info = {}):
        """
        """
        self._prepare_figure()

        channels = signal_set.get_channels()

        plot_num = len(channels)

        if xaxis is not None:
            xdata = xaxis
        else:
            xdata = self._timeline

        for idx, chann in enumerate(channels):
            py.subplot(plot_num, 1, idx + 1)
            if idx == 0:
                title = "Hand electrodes"
            else:
                title = "Finger electrodes"
            self._prepare_axes(xlabel, ylabel, title)
            py.plot(xdata, chann)
            if ylim is not None:
                py.ylim(ylim)
            if extra_info:
                for (x, y, point_plot) in extra_info[idx + 1]:
                    if point_plot:
                        py.plot(x, y, "x")
                    else:
                        py.plot(x, y)

        self._figure_done = True

    def plot_channel(self,
            channel,
            xaxis = None,
            xlabel = "time [s]",
            ylabel = "",
            title = "",
            point_plot = False):
        """
        """
        self._prepare_figure()
        self._prepare_axes(xlabel, ylabel, title)

        if xaxis is not None:
            xdata = xaxis
        else:
            xdata = self._timeline
        if point_plot:
            py.plot(xdata, channel, point_plot)
        else:
            py.plot(xdata, channel)
        self._figure_done = True

    def plot_channel_list(self,
            channel_list,
            xaxis = None,
            xlabel = "time [s]",
            ylabel = "magnitude",
            title_list = None):
        """
        """
        self._prepare_figure()

        plot_num = len(channel_list)
        if plot_num != len(title_list):
            raise ValueError("Title list and channel list " +
                 "should have matching lengths.")

        if xaxis is not None:
            xdata = xaxis
        else:
            xdata = self._timeline

        for idx in xrange(plot_num):
            py.subplot(plot_num, 1, idx + 1)
            self._prepare_axes(xlabel, ylabel, title_list[idx] + (16 * " "))
            py.plot(xdata, channel_list[idx])
        self._figure_done = True

    def plot_pairs(self, matrix):
        """
        """
        self._prepare_figure()
        box = (self._timeline[0],
            self._timeline[-1],
            self._timeline[-1],
            self._timeline[0])
        py.imshow(matrix, extent = box)
        self._figure_done = True

    def draw_histogram(self,
            values,
            bins = 30,
            xlabel = "",
            ylabel = "",
            title = ""):
        """
        """
        self._prepare_figure()
        self._prepare_axes(xlabel, ylabel, title)
        py.hist(values, bins = bins)
        self._figure_done = True

    def show(self):
        """
        """
        py.show()
