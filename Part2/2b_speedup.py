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

# ------------------ FUNCTIONS ------------------

def create_plot(xticks, xtick_labels, speedup, name):
    # generate plot
    plt.figure(figsize=(12, 12))

    plt.plot(xticks, speedup, marker='o', ms=7, c='goldenrod', linewidth=2.2)

    # move title and labeling
    ax = plt.gca()
    plt.xlabel(r"\bf{Number of Threads}", size=15)
    plt.ylabel(r'\bf{Speedup}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.03)
    plt.title(r"\bf{Measured Parsec Parallel Speedup}", loc='left', pad=60, size=18)
    # plt.legend(prop={'size': 14.5}, loc='upper left')
    plt.tight_layout()

    # axes adjustments
    plt.ylim([0, 7])

    # plt.yscale('linear')
    plt.xscale('log', base=2)
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
    normalized = [1]
    for i in range(1, len(response_times)):
        normalized.append(response_times[0] / response_times[i])
    return normalized


def main():
    response_times = [853.0, 442.0, 270.5, 165.9]
    xticks = [1, 2, 4, 8]
    xtick_labels = [1, 2, 4, 8]
    xtick_labels = [r'$2^0$', r'$2^1$', r'$2^2$', r'$2^3$']
    response_times = compute_normalized_speedup(response_times)
    print(response_times)
    create_plot(xticks, xtick_labels, response_times, 'speedup')


if __name__ == "__main__":
    main()
