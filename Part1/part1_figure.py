# PYTHON 3.10.0
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 16,
    "errorbar.capsize": 4
})

FILES = ['data/memcached_interference_ibench_cpu.txt', 'data/memcached_no_interference.txt',
         'data/memcached_interference_ibench_l1d.txt', 'data/memcached_interference_ibench_l1i.txt',
         'data/memcached_interference_ibench_llc.txt', 'data/memcached_interference_ibench_membw.txt',
         'data/memcached_interference_ibench_l2.txt']


def preprocess_data(file_name) -> pd.DataFrame:
    """
    :param file_name: relative path to file
    :return:
        data: dataframe with curated data
    """

    try:
        with open(file_name, 'r') as f:
            data = f.read()
            data = data.split('\n')
            data = [row.split()[1:] for row in data]  # remove first column with type of OP
            header = data[0]
            rows = data[1:]

            # strip last 3 rows with warning messages
            rows = rows[:-3]
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} does not exist")

    data = pd.DataFrame(rows, columns=header, dtype=np.float64)

    # take only the 'avg', 'std', 'p95' and 'QPS' columns
    data = data[['avg', 'std', 'p95', 'QPS']]
    return data


def get_data() -> List[pd.DataFrame]:
    """
    :return:
    data: list of dataframes
    """
    data = []
    for file in FILES:
        data.append(preprocess_data(file))
    return data


def array_to_string(arr):
    """
    convert a list of float values to a list of formatted strings e.g. 7000 becomes 7k
    :param arr: numpy array of float values
    :return:  list of formatted strings
    """
    arr = arr.astype(int).astype(str)
    arr = [f"{int(x) / 1000:.0f}k" for x in arr]
    # remove k from 0k
    arr[0] = "0"
    # insert latex math mode
    arr = [f"${x}$" for x in arr]

    arr = np.array(arr)
    return arr


def get_xticks(data) -> Tuple[np.ndarray, np.ndarray]:
    n = data.shape[0]
    # range is [0, 110000]
    start = 0
    stop = 110000

    steps = np.linspace(start, stop, 11, endpoint=True)
    steps = np.round(steps, -3)
    step_labels = array_to_string(steps)
    return steps, step_labels


def prepare_data(data):
    # y-axis should be between 0 and 8 ms
    # measurements currently in microseconds
    # don't include QPS column when converting
    qps = data['QPS']
    data = data.iloc[:, :-1] / 1000
    data['QPS'] = qps
    return data


def create_plot(xticks, xtick_labels, s1, s2, s3, s4, s5, s6, s7, flags, name):
    # generate plot
    plt.figure(figsize=(12, 12))

    # add error bars
    plt.errorbar(s1['QPS'], s1['p95'], yerr=s1['std'], marker='o', ms=7, c='tab:olive', linewidth=2.2,
                 label=r'$\texttt{--interference-ibench-cpu}$')
    plt.errorbar(s2['QPS'], s2['p95'], yerr=s2['std'], marker='o', ms=7, c='darkgreen', linewidth=2.2,
                 label=R'$\texttt{--no-interference}$')
    plt.errorbar(s3['QPS'], s3['p95'], yerr=s3['std'], marker='o', ms=7, c='darkblue', linewidth=2.2,
                 label=R'$\texttt{--interference-ibench-l1d}$')
    plt.errorbar(s4['QPS'], s4['p95'], yerr=s4['std'], marker='o', ms=7, c='darkorange', linewidth=2.2,
                 label=R'$\texttt{--interference-ibench-l1i}$')
    plt.errorbar(s5['QPS'], s5['p95'], yerr=s5['std'], marker='o', ms=7, c='red', linewidth=2.2,
                 label=R'$\texttt{--interference-ibench-llc}$')
    plt.errorbar(s6['QPS'], s6['p95'], yerr=s6['std'], marker='o', ms=7, c='purple', linewidth=2.2,
                 label=R'$\texttt{--interference-ibench-membw}$')
    plt.errorbar(s7['QPS'], s7['p95'], yerr=s7['std'], marker='o', ms=7, c='aqua', linewidth=2.2,
                 label=R'$\texttt{--interference-ibench-l2}$')

    # move title and labeling
    ax = plt.gca()
    plt.xlabel(r"\bf{Queries Per Second} $(QPS)$", size=15)
    plt.ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.03)
    plt.suptitle(r"\bf{\textit{Chart Title}}",
                 x=0.25,
                 y=0.9,
                 fontsize=36)
    plt.title("\n" "\n" "\n"
              r"\bf{Average across X runs }" + flags, loc='left', pad=60, size=18)
    plt.legend(prop={'size': 14.5}, loc='upper left')
    plt.tight_layout()

    # axes adjustments
    plt.ylim([0, 8])
    # plt.yscale('log', base=10)
    plt.yscale('linear')
    # plt.xscale('log', base=2)
    # coordinates diplayed on axes
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, fontsize=14)

    plt.yticks(fontsize=14)

    # grid and background
    ax.set_facecolor((0.92, 0.92, 0.92))
    plt.grid(axis='y', color='white', linewidth=2.0)
    plt.savefig('plot_1' + name + '.pdf')


# return array from 0 to index-1
def take_subset(array, start, end):
    return array[start:end]


def main():
    data = get_data()
    xticks, xticks_labels = get_xticks(data[0].to_numpy())  # we assume all dataframes have the same size
    data = [prepare_data(df) for df in data]

    # unpack dataframes
    try:
        s1, s2, s3, s4, s5, s6, s7 = data
        create_plot(xticks, xticks_labels, s1, s2, s3, s4, s5, s6, s7, "flags", "name")
    except ValueError:
        print("Not enough dataframes")


if __name__ == "__main__":
    main()
