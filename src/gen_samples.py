#!/usr/bin/env python3
# color maps trials
import numpy as np
# import pandas as pd
import os
import scipy as sp
from scipy import signal
from scipy.io.wavfile import read as wavread
# import subprocess
from multiprocessing import Process, Queue, Pool
# import wave
# graphical libraries
import matplotlib.pyplot as plt
# from matplotlib import cm
# import matplotlib.colors as mcolors
# from colorspacious import cspace_converter
from collections import OrderedDict

import itertools

cmaps = OrderedDict()
# %matplotlib inline
cmaps['Perceptually Uniform Sequential'] = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis']

cmaps['Sequential'] = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

cmaps['Sequential (2)'] = [
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper']

cmaps['Diverging'] = [
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c']

cmaps['Miscellaneous'] = [
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

all_cmaps = list(itertools.chain(*cmaps.values()))


def load_wav(fpath):
    return wavread(fpath)


def resample(song, nsamples=1024, abs=False, max_val=2 * np.pi):
    """
    returns left channel as positive values, right channel as negative ones and the time position
    :param song: numpy array with the signal to resample
    :param nsamples: number of samples of the output array
    :param abs:  if True returns absolute values only
    :param max_val: maximum value of the x value indices, defauls to 2*PI for circular displays
    :return: (sampled_arr,x values indices)
    """
    res = sp.signal.resample(song, nsamples)
    x = np.linspace(0, max_val, nsamples)
    if abs:
        res = np.abs(res)

    return res, x


# FIXME something about this function makes it take TOOOO long time to plot anything so it's useless
def img_add_subplot(fig, x, y, colormap, title=None, plottype="bar",
                    pos=111, alpha=0.75, width=0.015,
                    projection="rectilinear", polar_origin=-50):
    """

    :param fig:  figure object to use where to add the subplot
    :param x: x values (or radial values if polar)
    :param y: values to plot will add as many as channels there are here
    :param colormap: colormap with the same size as x
    :param title: title of the subplot
    :param plottype: type of plot, default is barplot
    :param pos: size and position of the subplot in matplotlib format()
    :param alpha: transparency
    :param width: with for bars
    :param projection: value between: [u'aitoff', u'hammer', u'lambert', u'mollweide', u'polar', u'rectilinear'].
    :param polar_origin: origin displacement for polar graphs
    :return: adds the subplot to the given figure
    """
    # print(x.shape, y.shape, colormap.shape)
    for yv in y:
        ax = fig.add_subplot(pos, projection='polar')
        if title:
            ax.title.set_text(title)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        if plottype == "bar":
            ax.bar(x, yv, alpha=alpha, width=width, color=colormap)
        elif plottype == "scatter":
            ax.scatter(x, yv, alpha=alpha, width=width, color=colormap)
        else:
            ax.plot(x, yv, alpha=alpha, width=width, color=colormap)
        if projection == "polar":
            ax.set_rorigin(polar_origin)


def brute_savefig(x, yl, yr, cmap, outfname):
    fig = plt.figure(figsize=(24, 24))

    ax = fig.add_subplot(2, 3, 1, projection='polar')
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    ax.bar(x, yl, alpha=0.75, width=0.015, color=cmap)
    # c = ax.scatter(x, yl+15, c=colors, s=area, cmap='hsv', alpha=0.75)
    ax.set_rorigin(-50)
    # ax.set_theta_zero_location('W', offset=10)
    ax2 = fig.add_subplot(2, 3, 2, projection='polar')
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    # ax2.bar(x, yl, alpha=0.75, width=0.015,  color=cmap)
    ax2.bar(x, yr, alpha=0.75, width=0.015, color=cmap)
    # c = ax.scatter(x, yl+15, c=colors, s=area, cmap='hsv', alpha=0.75)
    ax2.set_rorigin(-50)

    ax3 = fig.add_subplot(2, 3, 3, projection='polar')
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax3.axes.xaxis.set_visible(False)
    ax3.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    ax3.bar(x, yl, alpha=0.75, width=0.015, color=cmap)
    ax3.bar(x, yr, alpha=0.75, width=0.015, color=cmap)
    # c = ax.scatter(x, yl+15, c=colors, s=area, cmap='hsv', alpha=0.75)
    ax3.set_rorigin(-50)

    ax4 = fig.add_subplot(2, 3, 4)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax4.axes.xaxis.set_visible(False)
    ax4.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    ax4.bar(x, yl, alpha=0.75, width=0.015, color=cmap)
    # ax.set_theta_zero_location('W', offset=10)
    ax5 = fig.add_subplot(2, 3, 5)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax5.axes.xaxis.set_visible(False)
    ax5.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    # ax2.bar(x, yl, alpha=0.75, width=0.015,  color=cmap)
    ax5.bar(x, yr, alpha=0.75, width=0.015, color=cmap)
    # c = ax.scatter(x, yl+15, c=colors, s=area, cmap='hsv', alpha=0.75)

    ax6 = fig.add_subplot(2, 3, 6)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.], polar=True)
    # ax = fig.add_axes([00.0, 0.0, 2., 2.])
    ax6.axes.xaxis.set_visible(False)
    ax6.axes.yaxis.set_visible(False)
    # ax.plot(th2-20,r2, 'b', alpha=0.3)
    ax6.bar(x, yl, alpha=0.75, width=0.015, color=cmap)
    ax6.bar(x, yr, alpha=0.75, width=0.015, color=cmap)
    # c = ax.scatter(x, yl+15, c=colors, s=area, cmap='hsv', alpha=0.75)

    plt.savefig(outfname)


def create_sample_tile(wavfile, outpath, colornames, title=None, nsamples=500, figsize=(16, 16),
                       plottypes=("bar",), projections=(u'polar', u'rectilinear'),
                       left_channel=True, right_channel=True
                       ):
    """
    :param left_channel:
    :param right_channel:
    :param plottypes:
    :param projections:
    :param wavfile:
    :param outpath:
    :param colornames:
    :param title:
    :param nsamples:
    :param figsize:
    :return:
    """
    _, wav = load_wav(wavfile)  # drop sampling rate as I don't need it

    swav_polar, x_polar = resample(wav, nsamples=nsamples, abs=False, max_val=2 * np.pi)
    swav_lin, x_lin = resample(wav, nsamples=nsamples, abs=False, max_val=nsamples)

    y = np.abs(np.transpose(swav_lin))
    y[1, :] *= -1
    # compute the shape of the output
    mult = 1
    if left_channel and right_channel:
        mult = 3
    nsubplots = mult * len(projections) * len(plottypes)
    vert = int(np.sqrt(nsubplots))
    hor = int(np.ceil(np.sqrt(nsubplots)))
    base_pos = 100 * vert + 10 * hor

    for cname in colornames:
        try:
            print("starting graph file for ", cname)
            fig = plt.figure(figsize=figsize)
            figtitle = "" if not title else title
            figtitle = figtitle + " " + cname
            fig.suptitle(figtitle)

            cmap = plt.get_cmap(cname, nsamples)

            splt_count = 1
            for plottype in plottypes:
                for proj in projections:
                    x = x_lin
                    if proj == "polar":
                        x = x_polar
                    try:
                        cmap = cmap.colors
                    except:
                        try:
                            cmap = cmap(x)
                        except:
                            pass
                    # add only the absolute values if not there are too many sample images
                    # TODO take out repeated code and replace by function, left like this by lazyness
                    if left_channel:
                        try:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname))
                            img_add_subplot(fig, x, y[0], pos=base_pos + splt_count,
                                            title=plottype + " " + proj + " " + str(splt_count),
                                            colormap=cmap)
                            splt_count += 1
                        except Exception as e:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname), cname,
                                  "with error: ", e)
                    if right_channel:
                        try:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname))
                            img_add_subplot(fig, x, y[1], pos=base_pos + splt_count,
                                            title=plottype + " " + proj + " " + str(splt_count),
                                            colormap=cmap)
                            splt_count += 1
                        except Exception as e:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname),
                                  cname, "with error: ", e)
                    if left_channel and right_channel:
                        try:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname))
                            img_add_subplot(fig, x, y, pos=base_pos + splt_count,
                                            title=plottype + " " + proj + " " + str(splt_count),
                                            colormap=cmap)
                            splt_count += 1
                        except Exception as e:
                            print("processing tile {} of {} in pos {} for example {}".format(splt_count, nsubplots,
                                                                                             base_pos + splt_count,
                                                                                             cname),
                                  cname, "with error: ", e)
            # saving figure
            outfname = outpath + cname + ".png"
            print("saving figure", outfname)
            plt.savefig(outfname, fig)
            plt.close(fig)
        except Exception as e:
            print("failed trying figure for color ", cname, "with error: ", e)
            outfname = outpath + cname + ".png"
            print("saving figure despite failure", outfname)
            plt.savefig(outfname)
            plt.close(fig)


# def test_pool(arg1, arg2, arg3, arg4):
#     print("got args: ", arg1, arg2, arg3, arg4)


selectedcnames = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'
]


def main():
    wav = "/home/leo/Music/lucaStragnoli-FeelGoodINC.wav"
    outbasename = "/home/leo/projects/MUSIC-ART/samples/sample-tile-"
    title = "test colormap: "
    cpus = os.cpu_count()
    n = int(np.ceil(len(all_cmaps) / cpus))
    chunks = [all_cmaps[i:i + n] for i in range(0, len(all_cmaps), n)]
    # print(n, len(chunks))
    arguments = zip(cpus * [wav], cpus * [outbasename], chunks, cpus * [title])
    # cmaplen = len(all_cmaps)
    # arguments = zip(cmaplen * [wav], cmaplen * [outbasename], all_cmaps, cmaplen * [title])
    # print(len(chunks), list(arguments))
    # with Pool(processes=cpus) as pool:
    #     pool.starmap(create_sample_tile, arguments)
    #     # pool.starmap(test_pool, arguments)
    #
    create_sample_tile(wavfile=wav, outpath=outbasename, colornames=selectedcnames, title=title)


if __name__ == "__main__":
    main()
