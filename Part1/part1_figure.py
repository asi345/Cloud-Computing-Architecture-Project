# PYTHON 3.10.0
from typing import List, Tuple
import matplotlib.patheffects as path_effects
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

FILE_NAMES = ['data/memcached_interference_ibench_cpu.txt', 'data/memcached_no_interference.txt',
              'data/memcached_interference_ibench_l1d.txt', 'data/memcached_interference_ibench_l1i.txt',
              'data/memcached_interference_ibench_llc.txt', 'data/memcached_interference_ibench_membw.txt',
              'data/memcached_interference_ibench_l2.txt']

RUNS = 5


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
    data: list of dataframes with curated data, #RUNS dataframes for each file contigiously
    """

    data = []
    for file_name in FILE_NAMES:
        for run in range(RUNS):
            # append the run number to the file name
            file = file_name[:-4] + f"_{run}.txt"
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
    # sort by QPS
    qps = data['QPS']
    # data = data.sort_values(by='QPS')
    data = data.iloc[:, :-1] / 1000
    data['QPS'] = qps
    return data


def create_plot(xticks, xtick_labels, measured_statistics, flags, name):
    # generate plot
    plt.figure(figsize=(12, 12))
    error_bars = []
    markers = ['o', '*', '^', 'v', 's', 'X', 'D']
    colors = ['tab:olive', 'darkgreen', 'darkblue', 'darkorange', 'red', 'purple', 'aqua']
    labels = [r'$\texttt{--interference-ibench-cpu}$', R'$\texttt{--no-interference}$',
              r'$\texttt{--interference-ibench-l1d}$', r'$\texttt{--interference-ibench-l1i}$',
              r'$\texttt{--interference-ibench-llc}$', r'$\texttt{--interference-ibench-membw}$',
              r'$\texttt{--interference-ibench-l2}$']

    priority = [2, 7, 3, 4, 5, 6, 5] # zorder for error bars and lines

    for i, s in enumerate(measured_statistics):
        error_bar = plt.errorbar(s['QPS'], s['p95'], yerr=s['std'], fmt=markers[i], color=colors[i],
                                 label=labels[i], capsize=4, capthick=2, elinewidth=1, markersize=7,
                                 markeredgewidth=1, markeredgecolor='black', zorder=priority[i])
        # add line to connect markers, add black border to line
        plt.plot(s['QPS'], s['p95'], color=colors[i], linewidth=2, linestyle='-', zorder=priority[i])


        error_bars.append(error_bar)

    for error_bar in error_bars:
        error_bar[1][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])
        error_bar[1][1].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])
        error_bar[2][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])

    # move title and labeling
    ax = plt.gca()
    plt.xlabel(r"\bf{Queries Per Second} $(QPS)$", size=15)
    plt.ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.03)
    plt.suptitle(r"\bf{\textit{Measured Tail Latency of Memcached}}",
                 x=0.535,
                 y=0.9,
                 fontsize=36)
    plt.title("\n" "\n" "\n"
              r"\bf{Average across }" + f"{RUNS}" + r"\bf{ runs. Insert other }" + flags, loc='left', pad=60, size=18)
    plt.legend(prop={'size': 14.5}, loc='upper left')
    plt.tight_layout()

    # axes adjustments
    plt.ylim([0, 8])

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
    plt.savefig('plot_1_' + name + '.pdf')


# return array from 0 to index-1
def take_subset(array, start, end):
    assert end <= len(array) and start >= 0
    return array[start:end]


def compute_metrics(s1):
    assert len(s1) == RUNS
    tail_latencies = [s['p95'].to_numpy() for s in s1]
    qps = [s['QPS'].to_numpy() for s in s1]
    # compute means
    tail_latencies = np.array(tail_latencies)
    tail_latencies = np.transpose(tail_latencies)
    qpses = np.array(qps)
    qpses = np.transpose(qpses)
    average_tail_latency = np.mean(tail_latencies, axis=1)
    average_qps = np.mean(qpses, axis=1)
    # compute standard deviation
    std = np.std(tail_latencies, axis=1)
    # package everything back into a dataframe
    df = pd.DataFrame(
        {'QPS': average_qps,
         'p95': average_tail_latency,
         'std': std
         })

    return df


def main():
    data = get_data()
    xticks, xticks_labels = get_xticks(data[0].to_numpy())  # we assume all dataframes have the same size
    data = [prepare_data(df) for df in data]

    # unpack dataframes, #RUNS dataframes for each file contiguously
    measured_statistics = []
    try:
        for i in range(0, len(FILE_NAMES)):
            s1 = take_subset(data, i * RUNS, (i + 1) * RUNS)
            s1 = compute_metrics(s1)
            measured_statistics.append(s1)

        create_plot(xticks, xticks_labels, measured_statistics, "flags", "no-sort")
    except ValueError:
        print("Not enough dataframes")


if __name__ == "__main__":
    main()
