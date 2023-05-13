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

FILE_NAMES = [
    'memcached_output_T1_C1_',
    'memcached_output_T1_C2_',
    'memcached_output_T2_C1_',
    'memcached_output_T2_C2_'
]
FILE_NAMES = list(map(lambda x: 'results/' + x, FILE_NAMES))  # add path to file names

RUNS = 3

MARKERS = ['o', '<', '^', 'v', 's', 'X', 'D']
COLORS = ['darkgreen', 'tab:olive', 'darkblue', 'purple', 'red', 'darkorange', 'aqua']
LABELS = [r'$\texttt{--interference-ibench-cpu}$', R'$\texttt{--no-interference}$',
          r'$\texttt{--interference-ibench-l1d}$', r'$\texttt{--interference-ibench-l1i}$',
          r'$\texttt{--interference-ibench-llc}$', r'$\texttt{--interference-ibench-membw}$',
          r'$\texttt{--interference-ibench-l2}$']

PRIORITY = [2, 7, 3, 4, 5, 6, 5]  # zorder for error bars and lines


# ------------------ FUNCTIONS ------------------
def preprocess_data(file_name) -> pd.DataFrame:
    """
    :param file_name: relative path to file
    :param label: label for the data
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
    # take only the 'p95' and 'QPS' columns
    data = data[['p95', 'QPS']]
    data = prepare_data(data)
    return data


def get_data() -> dict[str, List[pd.DataFrame]]:
    """
    :return:
    data: list of dataframes with curated data, #RUNS dataframes for each file contigiously
    """

    data = {
    }

    for file_name in FILE_NAMES:
        for run in range(RUNS):
            # append the run number to the file name
            file = file_name + f"{run}.txt"
            label = f"T{file_name[26]}_C{file_name[29]}"
            if label not in data:
                data[label] = []
            data[label].append(preprocess_data(file))

    return data


def array_to_string(arr) -> np.ndarray:
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


def get_xticks() -> Tuple[np.ndarray, np.ndarray]:
    start = 0
    stop = 125000

    steps = np.linspace(start, stop, 11, endpoint=True)
    steps = np.round(steps, -3)
    step_labels = array_to_string(steps)
    return steps, step_labels


def prepare_data(data):
    # y-axis should be between 0 and 8 ms
    # measurements currently in microseconds
    # sort by QPS
    qps = data['QPS']
    data = data.sort_values(by='QPS')
    data = data / 1000
    data['QPS'] = qps
    return data


def create_plot(xticks, xtick_labels, measured_statistics, name):
    # generate plot
    plt.figure(figsize=(12, 12))
    error_bars = []

    for i, (label, s) in enumerate(measured_statistics.items()):
        label_str = label_mapping(label)

        error_bar = plt.errorbar(s['QPS'], s['p95'], yerr=s['y_std'], xerr=s['x_std'],
                                 fmt=MARKERS[i],
                                 color=COLORS[i],
                                 label=label_str,
                                 capthick=2,
                                 elinewidth=1,
                                 markersize=7,
                                 markeredgewidth=1,
                                 markeredgecolor='black',
                                 zorder=PRIORITY[i])
        # add line to connect markers
        plt.plot(s['QPS'], s['p95'], color=COLORS[i], linewidth=2, zorder=PRIORITY[i])
        error_bars.append(error_bar)

    # border on error bars
    for error_bar in error_bars:
        for cap in error_bar[1]:
            cap.set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                  path_effects.Normal()])

        error_bar[1][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])
        error_bar[1][1].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])
        error_bar[2][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                                          path_effects.Normal()])
        error_bar[2][1].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
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
              r"\bf{Average across }" + f"{RUNS}" + r"\bf{ runs. }", loc='left', pad=60, size=18)
    plt.legend(prop={'size': 14.5}, loc='upper left')
    plt.tight_layout()

    # axes adjustments
    plt.ylim([0, 2])

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
    plt.close()


def take_subset(array, start, end):
    assert end <= len(array) and start >= 0
    return array[start:end]


def compute_metrics(s1) -> pd.DataFrame:
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
    y_std = np.std(tail_latencies, axis=1)
    x_std = np.std(qpses, axis=1)

    # create a mask of indices to drop
    mask = np.zeros(len(average_tail_latency), dtype=bool)
    for i in range(1, len(average_tail_latency)):
        if (average_qps[i] - average_qps[
            i - 1] < 1000):  # and np.abs(average_tail_latency[i] - average_tail_latency[i - 1]) < 0.01:
            mask[i] = True

    # drop rows
    average_tail_latency = np.ma.masked_array(average_tail_latency, mask=mask)
    average_qps = np.ma.masked_array(average_qps, mask=mask)
    y_std = np.ma.masked_array(y_std, mask=mask)
    x_std = np.ma.masked_array(x_std, mask=mask)
    # package everything back into a dataframe
    df = pd.DataFrame(
        {'QPS': average_qps,
         'p95': average_tail_latency,
         'y_std': y_std,
         'x_std': x_std
         })
    df.dropna(inplace=True)
    return df


def aggregate_data(data):
    keys = data.keys()
    aggregated_data = {}
    for key in keys:
        runs_data = data[key]
        aggregated_data[key] = compute_metrics(runs_data)
    return aggregated_data


def label_mapping(label):
    thread_num = int(label[1])  # Extract the thread number
    core_num = int(label[4])  # Extract the core number
    label_str = f"cores {core_num} - threads {thread_num}"
    return r"\texttt{" + label_str + r"}"


def main():
    data = get_data()
    aggregated_data = aggregate_data(data)
    xticks, xticks_labels = get_xticks()
    create_plot(xticks, xticks_labels, aggregated_data, "memcached")


if __name__ == "__main__":
    main()
