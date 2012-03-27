#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pylab as py
from scipy.signal import filtfilt, cheby2, freqz

import sys

def widmoEKG(syg):
    widmo = np.abs(np.fft.fft(syg))**2
    freq = np.fft.fftfreq(len(syg), 1./128)
    return freq, widmo

def pikEKG(syg, prog):
    piki = []
    for i in range(len(syg)):
        if i > 0 and \
                i < len(syg) - 1 and \
                syg[i] > prog and \
                syg[i - 1] < syg[i] and \
                syg[i + 1] < syg[i]:
            piki.append(i)

    return piki

def usrednienie(piki):
    roznice = []
    for i in range(len(piki)-1):
        roznica = piki[i+1] - piki[i]
        roznice.append(roznica)
    srednia = np.mean(roznice)/128.
    return srednia

def widmopiku(syg,piki):
    srednia = usrednienie(piki) * 128.0
    print "sygnał: ", syg, len(syg)
    print "piki ", piki
    print "średnia ", srednia
    widma = []
    for i in piki:
        left = max(0, i - srednia / 2.0)
        right = min(len(syg) - 1, i + srednia / 2.0)
        widma.append(np.abs(np.fft.fft(syg[left:right]))**2)
    return widma

# returns (I, II, III)
def rawToEinthoven(left, right, foot):
    return (left -right, foot - right, foot - left)

def rawToGoldberg(left, right, foot):
    return (left -(right+foot)/2.0, \
           right- (foot+left)/2.0,          \
           foot - (left+right)/2.0)

if __name__ == '__main__':
    file_name = sys.argv[1]
    start = int(sys.argv[2])*128*8
    end = int(sys.argv[3])*128*8
    data = np.fromfile(file_name)
    #data = data[:2048]

    #chann1 = data[::8]
    fn=128/2.
    [b,a]=cheby2(1, 10, np.array([49,51])/fn, btype='bandstop')
    [c,d] = cheby2(1,10, np.array([0,4])/fn, btype = 'bandstop')
    s1 = data[start:end:8]
    chann1 = filtfilt(b,a,s1)
    chann1 = filtfilt(c,d,chann1)
    #chann2 = data[1::8]
    s2=data[start+1:end:8]
    chann2 = filtfilt(b,a,s2)
    chann2 = filtfilt(c,d,chann2)
    #chann3 = data[2::8]
    s3=data[start+2:end:8]
    chann3 = filtfilt(b,a,s3)
    chann3 = filtfilt(c,d,chann3)


    sigI, sigII, sigIII = rawToEinthoven(chann1, chann2, chann3)


#    py.subplot(3, 1, 1)
#    py.plot(chann1)
#
#    py.subplot(3, 1, 2)
#    py.plot(chann2)
#
#    py.subplot(3, 1, 3)
#    py.plot(chann3)
#
#    py.figure()

    py.subplot(3, 1, 1)
    py.plot(sigI)

    py.subplot(3, 1, 2)
    py.plot(sigII)

    py.subplot(3, 1, 3)
    py.plot(sigIII)

    py.figure()#sprawdzenie zasady Einthovena
    py.plot(sigI+sigIII)
    py.plot(sigII)

    py.figure()
    py.subplot(3, 1, 1)
    #py.show()
    #freq = np.fft.fftfreq(usrednienie(pikEKG(sigI, -35000)), 1./128)
    print "piki: ",  pikEKG(sigI, -20000)
    print "widmo: ", widmopiku(sigI,pikEKG(sigI, -20000))
    py.plot(widmopiku(sigI,pikEKG(sigI, -20000))[0])
    print widmopiku(sigI,pikEKG(sigI, -20000))[0]
    a = raw_input()


    print 'czasy wystepowania pikow sigI:', pikEKG(sigI, -20000)
    print 'sredni czas miedzy pikami', usrednienie(pikEKG(sigI, -20000)), 's'

    print 'czasy wystepowania pikow sigII:', pikEKG(sigII, -116000)
    print 'czasy wystepowania pikow sigIII:', pikEKG(sigIII, -80000)


    py.show()
