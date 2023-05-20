import ast

# PYTHON 3.10.0
from memcached_parallelism import *

# ------------------ CONFIG ------------------

MEMCACHED_NAMES = [
    'memcached_output_C1_',
    'memcached_output_C2_',
]

UTILISATION_NAMES = [
    'usage_C1_',
    'usage_C2_',
]

MEMCACHED_NAMES = list(map(lambda x: 'results2/' + x, MEMCACHED_NAMES))  # add path to file names
UTILISATION_NAMES = list(map(lambda x: 'results2/' + x, UTILISATION_NAMES))  # add path to file names

RUNS = 2

MARKERS = ['o', '<', '^', 'v', 's', 'X', 'D']
COLORS = ['darkgreen', 'darkorange', 'darkblue', 'purple', 'red', 'tab:olive', 'aqua']

PRIORITY = [2, 7, 3, 4, 5, 6, 5]  # zorder for error bars and lines


# ------------------ FUNCTIONS ------------------
def preprocess_utilisation(file_name) -> pd.DataFrame:
    """
    :param file_name: relative path to file
    :param label: label for the data
    :return:
        data: dataframe with curated data
    """

    header = ['cpu_0', 'cpu_1', 'cpu_2', 'cpu_3']
    try:
        with open(file_name, 'r') as f:
            data = f.read()
            data = data.split('\n')
            data = [ast.literal_eval(row) for row in data[:-1]]  # last string is empty

    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} does not exist")
    data = pd.DataFrame(data, columns=header, dtype=np.float64)

    # Set the threshold for CPU utilization
    threshold = 40.0

    # Find the columns where utilization is above the threshold
    active_cpus = data.columns[data.max() > threshold]

    # Drop the rows where utilization is below the threshold
    df_active = data[data[active_cpus].max(axis=1) > threshold]

    # Sum the utilization for active CPUs if more than one is detected
    df_active['total_utilization'] = df_active[active_cpus].sum(axis=1)
    return df_active['total_utilization'].reset_index(drop=True)


def get_data(file_names, preprocess_fn, runs) -> dict[str, List[pd.DataFrame]]:
    """
    :return:
    data: list of dataframes with curated data, #RUNS dataframes for each file contigiously
    """

    data = {
    }

    for file_name in file_names:
        for run in range(runs):
            # append the run number to the file name
            file = file_name + f"{run}.txt"

            if "memcached" in file_name:
                label = f"C{file_name[27]}"
            else:
                label = f"C{file_name[16]}"
            if label not in data:
                data[label] = []
            data[label].append(preprocess_fn(file))

    return data


def compute_metrics_utilisation(s1, runs) -> pd.DataFrame:
    assert len(s1) == runs
    util = [s.to_numpy() for s in s1]
    # compute means

    util = np.array(util)
    util = np.transpose(util)
    mean_util = np.mean(util, axis=1)
    # compute standard deviation
    y_std = np.std(util, axis=1)

    # package everything back into a dataframe
    df = pd.DataFrame(
        {'utilisation': mean_util,
         'std': y_std,
         })
    df.dropna(inplace=True)
    return df


def create_plot(xticks, xtick_labels, measured_statistics, measured_utilisation, label, name):

    fig, ax = plt.subplots(figsize=(12, 12))

    # label_str = label_mapping(label)
    label_str = 'C = 1' if label == 'C1' else 'C = 2'
    s = measured_statistics[label]
    error_bar = ax.errorbar(s['QPS'], s['p95'], yerr=s['y_std'], xerr=s['x_std'],
                                 fmt=MARKERS[0],
                                 color=COLORS[0],
                                 capthick=2,
                                 elinewidth=1,
                                 markersize=7,
                                 markeredgewidth=1,
                                 markeredgecolor='black',
                                 zorder=PRIORITY[0],
                                 label=label_str)
    # add line to connect markers
    ax.plot(s['QPS'], s['p95'], color=COLORS[0], linewidth=2, zorder=PRIORITY[i])

    # border on error bars
    for cap in error_bar[1]:
        cap.set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
                              path_effects.Normal()])
    # for error_bar in error_bars:
    #     for cap in error_bar[1]:
    #         cap.set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
    #                               path_effects.Normal()])
    #
    #     error_bar[1][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
    #                                       path_effects.Normal()])
    #     error_bar[1][1].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
    #                                       path_effects.Normal()])
    #     error_bar[2][0].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
    #                                       path_effects.Normal()])
    #     error_bar[2][1].set_path_effects([path_effects.Stroke(linewidth=4, foreground='black'),
    #                                       path_effects.Normal()])

    plt.xlabel(r"\bf{Queries Per Second} $(QPS)$", size=15)
    plt.ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.03)
    plt.suptitle(r"\bf{\textit{Measured Tail Latency of Memcached and CPU Utilisation} }",
                 x=0.485,
                 y=0.9,
                 fontsize=20)
    plt.title("\n" "\n" "\n"
              r"\bf{Average across }" + f"{RUNS}" + r"\bf{ runs. }", loc='left', pad=60, size=18)


    # axes adjustments
    plt.ylim([0, 2])

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, fontsize=14)

    plt.yticks(fontsize=14)
    # plt.xscale('log', base=2)
    # grid and background
    ax.set_facecolor((0.92, 0.92, 0.92))
    plt.grid(axis='y', color='white', linewidth=2.0)
    plt.grid(axis='x', color='white', linewidth=2.0)

    ax2 = ax.twinx()
    ax2.set_ylabel(r'\bf{CPU Utilisation (\%)}', rotation=0, size=15)
    ax2.yaxis.set_label_coords(1.0, 1.05)

    if label == 'C1':
        ax2.set_ylim([0, 100])
        ax2.set_yticks([0, 20, 40, 60, 80, 100])
    else:
        ax2.set_ylim([0, 200])
        ax2.set_yticks([0, 50, 100, 150, 200])

    util = measured_utilisation[label]
    if len(s['QPS'] != len(util['utilisation'])):
        utilisation = util['utilisation'][len(util['utilisation']) - len(s['QPS']):]
        std = util['std'][len(util['std']) - len(s['QPS']):]

    ax2.plot(s['QPS'], utilisation, color=COLORS[1], linewidth=2, zorder=PRIORITY[1], label=r'CPU Utilisation')
    ax2.fill_between(s['QPS'], utilisation - std, utilisation + std, color=COLORS[1], alpha=0.2)
    ax.axhline(y=1, color='red', linestyle='--', linewidth=2, zorder=2)
    plt.annotate(r"\bf{SLO Objective}", xy=(0.8, .47), xycoords='axes fraction', size=14)
    # Combine the legend handles and labels from both plots
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2

    # Create a legend with the combined handles and labels
    plt.legend(handles, labels, prop={'size': 14.5}, loc='upper left')
    plt.tight_layout()
    plt.savefig('Q1' + name + label + '.pdf')
    plt.close()



if __name__ == '__main__':
    data = get_data(MEMCACHED_NAMES, preprocess_data, RUNS)
    aggregated_data = aggregate_data(data, compute_metrics, RUNS)
    xticks, xticks_labels = get_xticks(stop=130000)
    utilisation = get_data(UTILISATION_NAMES, preprocess_utilisation, RUNS)
    aggregated_utilisation = aggregate_data(utilisation, compute_metrics_utilisation, RUNS)

    # ------------------ PLOT ------------------
    labels = aggregated_utilisation.keys()
    for i, label in enumerate(labels):
        create_plot(xticks, xticks_labels, aggregated_data, aggregated_utilisation, label, "PART4")
