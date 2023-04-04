# PYTHON 3.10.0
from typing import List, Tuple
import matplotlib.patheffects as path_effects
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ------------------ CONFIG ------------------
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 16,
    "errorbar.capsize": 4
})

COLORS = {
    r'\emph{black scholes}': 'darkblue',
    r'\emph{canneal}': 'royalblue', # suggest something yellow-ish
    r'\emph{dedup}': 'maroon',
    r'\emph{ferret}': 'darkgreen',
    r'\emph{freqmine}': 'darkorange',
    r'\emph{radix}': 'orangered',
    r'\emph{vips}': 'purple'
}


# ------------------ FUNCTIONS ------------------

def create_plot(xticks, xtick_labels, response_times, name):
    # generate plot
    plt.figure(figsize=(12, 12))

    for i in range(len(response_times)):
        plt.plot(xticks, response_times[i], marker='o', markersize=10, color=COLORS[list(COLORS.keys())[i]],
                 label=list(COLORS.keys())[i])

    # move title and labeling
    ax = plt.gca()
    plt.xlabel(r"\bf{Number of Threads}", size=15)
    plt.ylabel(r'\bf{Speedup}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.03)
    plt.title(r"\bf{Measured Parsec Parallel Speedup}", loc='left', pad=60, size=18)
    plt.legend(prop={'size': 14.5}, loc='upper left', title=r'\bf{Job type}')
    plt.tight_layout()

    # axes adjustments
    plt.ylim([0, 7])

    # plt.yscale('linear')
    # plt.xscale('log', base=2)
    # coordinates diplayed on axes
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, fontsize=14)

    plt.yticks(fontsize=14)
    # plt.xscale('log', base=2)
    # grid and background
    ax.set_facecolor((0.92, 0.92, 0.92))
    plt.grid(axis='y', color='white', linewidth=2.0)
    plt.grid(axis='x', color='white', linewidth=2.0)
    plt.savefig('plot_2b_' + name + '.pdf')
    plt.close()


def compute_normalized_speedup(response_times):
    normalized = np.zeros_like(response_times)
    for i in range(len(response_times)):
        normalized[i] = response_times[i][0] / response_times[i]
    return normalized


def main():
    black_scholes = np.array([125.102, 72.709, 47.359, 36.309], dtype=np.float64)
    canneal = np.array([252.449, 188.145, 131.056, 107.335], dtype=np.float64)
    dedup = np.array([20.522, 13.405, 11.784, 11.503], dtype=np.float64)
    ferret = np.array([320.171, 163.943, 95.431, 81.764], dtype=np.float64)
    freqmine = np.array([490.138, 252.886, 127.461, 101.923], dtype=np.float64)
    radix = np.array([53.043, 30.083, 15.014, 9.585], dtype=np.float64)
    vips = np.array([99.068, 52.883, 26.044, 22.201], dtype=np.float64)
    xticks = [1, 2, 4, 8]
    xtick_labels = [1, 2, 4, 8]
    # xtick_labels = [r'$2^0$', r'$2^1$', r'$2^2$', r'$2^3$']
    response_times = np.stack((black_scholes, canneal, dedup, ferret, freqmine, radix, vips), axis=0)
    response_times = compute_normalized_speedup(response_times)
    print(response_times)
    create_plot(xticks, xtick_labels, response_times, 'speedup-linear')


if __name__ == "__main__":
    main()
