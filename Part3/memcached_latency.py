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

JOB_COLORS = {
    'dedup': '#CCACCA',
    'ferret': '#AACCCA',
    'freqmine': '#0CCA00',
    'vips': '#CC0A00',
    'canneal': '#CCCCAA',
    'blackscholes': '#CCA000',
    'radix': '#00CCA0'
}
XY_LABELS = [
    [
        [(0.118608, 0.015), (0.1635, 0.015), (0.1635, 0.015), (0.22233, 0.015), (0.3352, 0.015), (0.536551, 0.015)],
        [(0.122, 0.015), (0.2415, 0.015), (0.6183, 0.015), (0.706169, 0.015)],
        [(0.122, 0.015), (0.1941, 0.015), (0.2659, 0.015), (0.5805, 0.015)],
    ],
    [
        [(0.0941, 0.015), (0.107, 0.015), (0.1534, 0.015), (0.1565, 0.015), (0.3142, 0.015), (0.5071, 0.015)],
        [(0.107, 0.015), (0.48, 0.015), (0.631, 0.015), (0.71, 0.015)],
        [(0.107, 0.015), (0.182, 0.015), (0.2575, 0.015), (0.565, 0.015)],
    ],
    [
        [(0.1306, 0.015), (0.1635, 0.015), (0.1635, 0.015), (0.1885, 0.015), (0.288, 0.015), (0.5685, 0.015)],
        [(0.197, 0.015), (0.22, 0.015), (0.615, 0.015), (0.709, 0.015)],
        [(0.141, 0.015), (0.182, 0.015), (0.192, 0.015), (0.596, 0.015)],
    ]
]

for runs in XY_LABELS:
    for node in runs:
        for i in range(len(node)):
            node[i] = (node[i][0] + 0.016, node[i][1])


NODE_POS = [
    (0.25, -0.6),
    (0.25, -0.4),
    (0.25, -0.2)
]

JOB_STR_OFFSETS = {
    'dedup': (0.15, -0.2),
    'ferret': (0.1, -0.2),
    'freqmine': (0.14, -0.4),
    'vips': (0.085, -0.4),
    'canneal': (0., -0.6),
    'blackscholes': (0.125, -0.6),
    'radix': (0.055, -0.6)
}

RUNS = 3


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


def generate_horizontal_line(ax, x1, x2, y, color=None):
    ax.annotate('', xy=(x1, y), xytext=(x2, y),
                arrowprops=dict(color=color, arrowstyle='-', lw=2))


def create_plot(xtick, data, run_number):
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.subplots_adjust(bottom=0.32)
    x = data['cumulative_time']
    x = x - x[0] / 2
    y = data['p95']
    width = data['elapsed_time'].mean()
    xy_labels = XY_LABELS[run_number]
    ax.bar(x, y, width=width, edgecolor='black', linewidth=1.5)
    ax.set_xlabel(r'\bf{Elapsed Time (s)}')
    ax.set_ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}')
    ax.set_ylim((0., 2.))
    # plot vertical line at y = 1.
    ax.axhline(y=1., color='red', linestyle='--', linewidth=2)
    ax.annotate(r'\bf{SLO Objective}', xy=(260, 1.15), xytext=(260, 1.1), color='black', fontfamily='sans-serif')
    # Add a horizontal line at y=0.5
    # ax.annotate('', xy=(-.5, 0), xytext=(289.5, 0),
    #             arrowprops=dict(color='red', arrowstyle='-', lw=2))
    generate_horizontal_line(ax, -0.5, 289.5, 0., color='red')
    ax.annotate('[', xy=(-0.45, 0.015), xytext=(-0.45, -0.015), color='red')
    ax.annotate(']', xy=(288.45, 0.015), xytext=(288.45, -0.015), color='red')
    ax.annotate(r'\bf{289}', xy=(286, 0.0), xytext=(286, -0.09), color='red', fontfamily='sans-serif')
    # ax.spines['bottom'].set_color('red')
    # ax.axvspan(0, 300, color='red', alpha=0.2)
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
                x_position = NODE_POS[i][0] + xy_labels[i][k][0]
                y_position = NODE_POS[i][1] + xy_labels[i][k][1]
                position = (x_position, y_position)
                new_ax.annotate(xtick_label, xy=position, textcoords='offset points',
                                xycoords='axes fraction', ha='center', va='top', size=12,
                                color=colors[i])

            if run_number == 1:
                if node == 'node-c-8core':
                    new_ax.set_xticks([100, 104, 120, 170, 232])
                    for tick in plt.gca().xaxis.get_ticklabels():
                        tick.set_rotation(45)

            if run_number == 2:
                if node == 'node-a-2core':
                    new_ax.set_xticks([115, 130, 260])

        # place annotation for node
        node_str = r'$\texttt{' + node + '}$'
        ax.annotate(node_str, xy=NODE_POS[i], xycoords='axes fraction',
                    textcoords='offset points', size=15, ha='center', va='center',
                    bbox=dict(boxstyle='round', fc='white', alpha=0.5),
                    color=colors[i],
                    # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color=colors[i])
                    )

    ax.set_facecolor((0.92, 0.92, 0.92))
    # plt.grid(axis='y', color='white', linewidth=2.0)
    plt.grid(axis='y', color='grey', linewidth=2.0, alpha=0.3)
    y_grid_lines = [0.25, 0.5, 0.75, 1.25, 1.5, 1.75]
    for y_grid_line in y_grid_lines:
        ax.axhline(y=y_grid_line, color='grey', linestyle='-', linewidth=2, alpha=0.3)
    jobs = JOB_COLORS.keys()
    for i, job in enumerate(jobs):
        ax.annotate(job, xy=JOB_STR_OFFSETS[job], xytext=(JOB_STR_OFFSETS[job][0], 0.5), xycoords='axes fraction',
                    textcoords='offset points', size=15, ha='center', va='center',
                    bbox=dict(boxstyle='round', fc='white', alpha=0.5),
                    color=JOB_COLORS[job],
                    # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color=colors[i])
                    )
    plt.title(r'\bf{Memcached Latency (Top) and Collocated Jobs (Bottom)}', fontsize=20)
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


def compute_metrics(normalized_job_run_times):
    print("Computing metrics...")
    # for each run, compute execution_time of each job
    for i, df in enumerate(normalized_job_run_times):
        df['execution_time'] = df['finish_time'] - df['start_time']

    # Create a dictionary to hold the mean and standard deviation for each PARSEC application
    results = {}

    # Loop over each application in the MACHINE_JOB_ALLOCATIONS mapping
    for application in MACHINE_JOB_ALLOCATIONS.keys():
        # Create an empty list to hold the execution times for each run
        execution_times = []
        # Loop over each dataframe
        for df in normalized_job_run_times:
            # Subset the dataframe to only include rows for the current application
            subset = df[df['job'] == application]
            execution_times.append(subset['execution_time'])
        # Compute the mean and standard deviation of the execution times for the current application
        mean_execution_time = np.mean(execution_times)
        std_execution_time = np.std(execution_times)
        # Add the mean and standard deviation to the results dictionary
        results[application] = {
            'mean_execution_time': mean_execution_time,
            'std_execution_time': std_execution_time
        }
    return results

def main():
    memcached_runs = get_data_memcached()
    job_run_times = get_job_run_times()

    memcached_runs_total_time = [df['cumulative_time'].max() for df in memcached_runs]
    normalized_job_run_times = normalize_job_run_times(job_run_times, memcached_runs_total_time)

    machine_job_offsets = compute_offsets_from_machine_job_allocations()
    xticks = compute_xticks(normalized_job_run_times, machine_job_offsets)
    create_plots(xticks, memcached_runs)
    results = compute_metrics(normalized_job_run_times)
    print(results)

if __name__ == "__main__":
    main()
