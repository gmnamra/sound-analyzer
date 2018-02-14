import numpy as np
import os, sys
thisdir = os.path.abspath('engines')
sys.path.append(thisdir)
import audio_algorithms as aa
import graph_functions as gf
from scipy.signal import butter, lfilter

# Generate f, psd from data:
def procdata(data, bandpass):
    data = aa.bandpass_filter(data, bandpass)
    f, psd = aa.spectrum(data, bandpass = bandpass)
    return f, psd

# Generate multiple curves on same data and save all of it.
def datagen(filename):
    psdlists = []
    for each in aa.split_seconds(filename):
        f, psd = procdata(each, [80, 2000])
        # gf.just_plot(f, psd)
        psdlists.append(psd)
    psdlist = np.asarray(psdlists)
    return f, psdlist

# Generate a background curve from big data.
def background(f, psdlist, plot = False):
    psd = np.average(psdlist, axis = 0)
    if plot:
        psddecimal = np.log10(psd)*10 + 120
        gf.just_plot(f, psddecimal, std=True, xlabel = 'Hz', ylabel = 'dB')
    return psd

# Generate noise over this frequency background from psdlist and background.
def getpowerhistogram(f, psdlist, backgroundpsd):
    diffs = []
    for each in psdlist:
        diff = each - backgroundpsd
        diff = diff.clip(min = 0)
        sumdiff = np.sum(diff)
        if sumdiff < 1e-12:
            sumdiff = 1e-12
        diffdecimal = np.log10(sumdiff)*10 + 120
        diffs.append(diffdecimal)
    return diffs

# data = np.load('soundfiles/Trial0107/50ft_0ft_0.npy')
# freq = aa.bandpass_filter(data, [80, 2000])
# gf.just_plot(np.arange(len(freq)), freq, std=True)

def noise_signal(signalfile, backgroundfile):
    f, psd = datagen(backgroundfile)
    backgroundpsd = background(f, psd)
    noise = getpowerhistogram(f, psd, backgroundpsd)
    f, psd = datagen(signalfile)
    signals = getpowerhistogram(f, psd, backgroundpsd)
    return noise, signal

def just_signal(signalfile, backgroundpsd):
    f, psd = datagen(signalfile)
    signals = getpowerhistogram(f, psd, backgroundpsd)
    return noise, signal

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Not enough arguments')
    signalfile = sys.argv[1]
    backgroundfile = sys.argv[2]
    if len(sys.argv) > 3:
        backgroundpsd = aa.load_npy(sys.argv[3])
    noise, signal = noise_signal(signalfile, backgroundfile)
    
