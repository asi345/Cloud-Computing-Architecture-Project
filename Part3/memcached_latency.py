# PYTHON 3.10.0
import subprocess
from typing import List, Tuple
import matplotlib.patheffects as path_effects
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import matplotlib.transforms as mtransforms

# ------------------ CONFIG ------------------
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 16,
    "errorbar.capsize": 4
})

FILE_NAMES = ['memcached_output.txt']
RESULTS_METADATA = 'results'
COLORS = ['darkgreen', 'tab:olive', 'darkblue', 'purple', 'red', 'darkorange', 'aqua']

MACHINE_JOB_ALLOCATIONS = {
    'dedup': 'node-a-2core',
    'ferret': 'node-a-2core',
    'freqmine': 'node-b-4core',
    'vips': 'node-b-4core',
    'canneal': 'node-c-8core',
    'blackscholes': 'node-c-8core',
    'radix': 'node-c-8core',
    'memcached': 'node-c-8core',
}

XY_LABELS = [
    [(0.1225, 0.015), (0, 0.015), (0, 0.015), (0, 0.015), (0, 0.015), (0, 0.015), (0, 0.015), (0, 0.015)],
    [(0.1225, 0.015), (0, 0.), (0, 0.), (0, 0.)],
    [(0.1225, 0.015), (0, 0.), (0, 0.), (0, 0.)],
]
NODE_POS = [(0.25, -0.6), (0.25, -0.4), (0.25, -0.2)]
RUNS = 4


# ------------------ FUNCTIONS ------------------
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
            rows = data[1:-1]  # last row is empty

    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} does not exist")

    data = pd.DataFrame(rows, columns=header, dtype=np.float64)
    data['elapsed_time'] = data['ts_end'] - data['ts_start']

    # Calculate cumulative elapsed time
    cumulative_time = [data['elapsed_time'][0]]
    for i in range(1, len(data)):
        delay = data['ts_start'][i] - data['ts_end'][i - 1]
        cumulative_time.append(cumulative_time[-1] + data['elapsed_time'][i] + delay)

    # Add cumulative elapsed time to the DataFrame
    data['cumulative_time'] = cumulative_time

    data = data[['p95', 'elapsed_time', 'cumulative_time']]
    data['elapsed_time'] = data['elapsed_time'] / 1000  # convert to seconds
    data['cumulative_time'] = data['cumulative_time'] / 1000  # convert to seconds
    data['p95'] = data['p95'] / 1000  # convert to seconds
    return data


def get_data_memcached() -> List[pd.DataFrame]:
    """
    :return:`
    data: list of dataframes with curated data, #RUNS dataframes for each file contigiously
    """

    data = []
    for file_name in FILE_NAMES:
        for run in range(RUNS):
            # append the run number to the file name
            file = file_name[:-4] + f"_{run}.txt"
            data.append(preprocess_data(file))
    return data


def create_plots(xticks, runs):
    for i, data in enumerate(runs):
        # get the xtick for the run
        xtick = xticks[i]
        create_plot(xtick, data, i)
        break


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def compute_xtick_labels(xtick_bounds):
    # determine the labels for a given xtick bounds.
    labels = []
    bounds = xtick_bounds.copy()
    bounds = [x.tolist() for x in bounds]

    intervals = [True] * len(xtick_bounds)  # keeps track of which interval is currently open
    indices = list(range(len(xtick_bounds)))  # keeps track of original indices of intervals
    while any(intervals):
        curr_vals = [bound[0] for bound in bounds]  # get the first value in each non-empty interval
        min_val = min(curr_vals)
        for i in range(len(bounds)):
            if bounds[i][0] == min_val:
                orig_index = indices[i]  # get original index of interval
                if len(bounds[i]) == 1:
                    intervals[orig_index] = False  # use orig_index to update intervals
                    del indices[i]
                    del bounds[i]
                    labels.append("]")
                else:
                    labels.append("[")
                    bounds[i].pop(0)
                break
    return labels


def create_plot(xtick, data, run_number):
    print(data)
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.subplots_adjust(bottom=0.32)
    x = data['cumulative_time']
    y = data['p95']
    width = data['elapsed_time'].mean()
    ax.bar(x, y, width=width, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Elapsed Time (s)')
    ax.set_ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}')
    ax.set_ylim((0., 2.))
    # plot vertical line at y = 1.
    ax.axhline(y=1., color='r', linestyle='--', linewidth=2)
    # # Create a new twinx axis for each node
    axes = [ax]
    nodes = xtick.__reversed__()
    colors = ['r', 'g', 'b']
    assert len(xtick.keys()) == len(colors)

    # xy_offset = [(0.2, -0.95), (0.2, -0.65), (0.2, -0.35)]
    for i, node in enumerate(nodes):
        xticks = xtick[node]
        xtick_bounds = xticks['xticks']
        collocated_jobs = xticks['collocated_jobs']

        offset = xticks['offset']
        print(xtick_bounds)
        # if memcached is collocated with another job don't count it
        if 'memcached' in collocated_jobs:
            memcached_index = collocated_jobs.index('memcached')
            collocated_jobs.pop(memcached_index)
            xtick_bounds.pop(memcached_index)

        xtick_labels = compute_xtick_labels(xtick_bounds)
        # sort the xtick bounds
        xtick_bounds = [x.tolist() for x in xtick_bounds]
        # flatten the list
        xtick_bounds = [item for sublist in xtick_bounds for item in sublist]
        xtick_bounds = sorted(xtick_bounds)

        for j in range(len(collocated_jobs)):

            new_ax = ax.twiny()
            axes.append(new_ax)
            new_ax.spines["bottom"].set_color(colors[i])  # color of node
            new_ax.tick_params(axis='x', colors=colors[i])
            new_ax.spines["bottom"].set_linewidth(2)
            new_ax.spines["bottom"].set_position(("axes", offset))
            new_ax.set_xlim(ax.get_xlim())

            new_ax.set_xticks(xtick_bounds)
            # new_ax.set_xticklabels(xtick_labels)

            new_ax.spines["bottom"].set_bounds(xtick_bounds[0], xtick_bounds[-1])
            new_ax.tick_params(axis='x', which='major', reset=True, labelsize=12, colors=colors[i])


            for k, xtick_label in enumerate(xtick_labels):
                print(k)
                x_position = NODE_POS[i][0] + XY_LABELS[i][k][0]
                y_position = NODE_POS[i][1] + XY_LABELS[i][k][1]
                position = (x_position, y_position)
                new_ax.annotate(xtick_label, xy=position, textcoords='offset points',
                                xycoords='axes fraction', ha='center', va='top', size=12)

        # place annotation for node
        node_str = r'$\texttt{' + node + '}$'
        ax.annotate(node_str, xy=NODE_POS[i], xycoords='axes fraction',
                    textcoords='offset points', size=15, ha='center', va='center',
                    bbox=dict(boxstyle='round', fc='white', alpha=0.5),

                    # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color=colors[i])
                    )

    ax.set_facecolor((0.92, 0.92, 0.92))
    # plt.grid(axis='y', color='white', linewidth=2.0)
    # plt.grid(axis='x', color='white', linewidth=2.0)
    plt.tight_layout()
    plt.savefig('plot_' + str(run_number) + '.pdf')
    plt.close()


def get_job_run_times():
    # call the get_time.py script to get the job run times

    for run in range(RUNS):
        # append the run number to the file name
        file = RESULTS_METADATA + f"_{run}.json"
        # call the script with arguments
        subprocess.call(['python3', 'get_time.py', file])

    # read the dataframes
    job_run_times = []
    for run in range(RUNS):
        file = 'runtime_jobs' + f"_{run}.csv"
        df = pd.read_csv(file)
        # remove the parsec- prefix from the job names
        df['job'] = df['job'].str.replace('parsec-', '')
        job_run_times.append(df)

    return job_run_times


def normalize_job_run_times(job_run_times, memcached_run_times):
    # for each dataframe, normalize the start_time and finish_time of each row by the start_time of entry 'memcached' in
    # the 'job' column
    normalized_job_run_times = []
    for i, df in enumerate(job_run_times):
        start_time = pd.to_datetime(df['start_time'])
        finish_time = pd.to_datetime(df['finish_time'])
        memcached_start_time = pd.to_datetime(df[df['job'] == 'memcached']['start_time'].values[0])

        start_time = (start_time - memcached_start_time).dt.total_seconds().astype(float)
        finish_time = (finish_time - memcached_start_time).dt.total_seconds().astype(float)
        df['start_time'] = start_time
        df['finish_time'] = finish_time

        df.loc[df['job'] == 'memcached', 'finish_time'] = memcached_run_times[i]

        normalized_job_run_times.append(df)

    return normalized_job_run_times


def compute_xticks_run(df, machine_job_offsets):
    # compute the xticks and xticks_labels PER RUN. These will serve to setup the Spines of the plot

    xticks = {}
    for job in MACHINE_JOB_ALLOCATIONS.keys():
        node = MACHINE_JOB_ALLOCATIONS[job]
        xtick_job_bounds = df.loc[df['job'] == job, ['start_time', 'finish_time']].to_numpy().squeeze()

        if node not in xticks:
            xticks[node] = {}
            xticks[node]['collocated_jobs'] = []
            xticks[node]['xticks'] = []
        if job != 'memcached':
            xticks[node]['collocated_jobs'].append(job)
            xticks[node]['xticks'].append(xtick_job_bounds)
            xticks[node]['offset'] = machine_job_offsets[node]

    return xticks


def compute_xticks(job_dfs, offsets) -> List[dict]:
    xticks_runs = []
    for df in job_dfs:
        xticks_dict = compute_xticks_run(df, offsets)
        xticks_runs.append(xticks_dict)
    return xticks_runs


def compute_offsets_from_machine_job_allocations():
    memcached_offset = -0.2
    counter = 1
    machine_job_counts = {}

    # count the number of machines for each machine type
    for machine_type in MACHINE_JOB_ALLOCATIONS.values():
        if machine_type not in machine_job_counts:
            machine_job_counts[machine_type] = counter * memcached_offset
            counter += 1

    return machine_job_counts


def main():
    memcached_runs = get_data_memcached()
    print("memcached runs: ", memcached_runs)
    job_run_times = get_job_run_times()

    memcached_runs_total_time = [df['cumulative_time'].max() for df in memcached_runs]
    normalized_job_run_times = normalize_job_run_times(job_run_times, memcached_runs_total_time)
    print("normalized job run times: ", normalized_job_run_times)
    #
    # print("xticks: ", xticks)
    # print("xticks_labels: ", xticks_labels)
    machine_job_offsets = compute_offsets_from_machine_job_allocations()
    xticks = compute_xticks(normalized_job_run_times, machine_job_offsets)
    create_plots(xticks, memcached_runs)
    print(xticks[0])
    exit(0)
    xticks, xticks_labels = get_xticks(data[0].to_numpy())  # we assume all dataframes have the same size
    data = [prepare_data(df) for df in data]

    # unpack dataframes, #RUNS dataframes for each file contiguously
    measured_statistics = []
    try:
        for i in range(0, len(FILE_NAMES)):
            s1 = take_subset(data, i * RUNS, (i + 1) * RUNS)
            s1 = compute_metrics(s1)
            measured_statistics.append(s1)

        create_plot(xticks, xticks_labels, measured_statistics, "flags", "sort-drop")
    except ValueError:
        print("Not enough dataframes")


if __name__ == "__main__":
    main()
