import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

jobs_list = ["memcached", "dedup", "radix", "canneal", "ferret", "blackscholes", "freqmine", "vips"]

JOB_COLORS = {
    'dedup': '#CCACCA',
    'ferret': '#AACCCA',
    'freqmine': '#0CCA00',
    'vips': '#CC0A00',
    'canneal': '#CCCCAA',
    'blackscholes': '#CCA000',
    'radix': '#00CCA0'
}

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 16,
    "errorbar.capsize": 4
})


def array_to_time_string(array) -> list[str]:
    """
    convert a list of float values to a list of timesteps e.g. 300 becomes 300s
    :param array: numpy array of float values
    :return: list of formatted strings
    """
    array = array.astype(int).astype(str)
    array = [f"{int(x)}s" for x in array]
    # remove s from 0s
    array[0] = "0"

    # insert latex math mode
    array = [f"${x}$" for x in array]
    return array


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


def get_xticks(stop, step=10):
    """
    :param stop: int, stop value for the x-axis (in seconds)
    :return: np.ndarray, np.ndarray
    """
    start = 0
    steps = np.linspace(start, stop, step, endpoint=True)
    steps = np.round(steps, -1)
    step_labels = array_to_time_string(steps)
    return steps, step_labels


def get_yticks(stop, step=11):
    """
    :param stop: int, stop value for the y-axis (in QPS)
    :return: np.ndarray, np.ndarray
    """
    start = 0
    steps = np.linspace(start, stop, step, endpoint=True)
    steps = np.round(steps, -3)
    step_labels = array_to_string(steps)
    return steps, step_labels


def preprocess_memcached(file):
    """
    :param file_name: relative path to file
    :param label: label for the data
    :return:
        data: dataframe with curated data
    """

    try:
        with open(file, 'r') as f:
            data = f.read()
            data = data.split('\n')
            data = [row.split()[1:] for row in data]  # remove first column with type of OP
            header = data[0]
            rows = data[1:]
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file} does not exist")

    data = pd.DataFrame(rows, columns=header, dtype=np.float64)
    # take only the 'p95' and 'QPS' columns
    data = data[['p95', 'QPS']]
    data = prepare_data(data)
    return data


def prepare_data(data):
    # y-axis should be between 0 and 8 ms
    # measurements currently in microseconds
    # sort by QPS
    qps = data['QPS']
    data = data / 1000
    data['QPS'] = qps
    return data


def get_memcached_data(file_name, run) -> pd.DataFrame:
    """
    :return:
    data: dataframe with curated data
    """

    # append the run number to the file name
    file = file_name + f"{run}.txt"

    assert "memcached" in file_name and file_name.startswith("results")

    return preprocess_memcached(file)


def get_parsec_data(file_name, run) -> dict:
    # append the run number to the file name
    file = file_name + f"{run}.txt"

    # Read the file and extract lines
    with open(file, 'r') as file:
        lines = file.readlines()

    data = {}
    # Initialize empty lists for start time, end time, and job

    last_core = 0
    # Process each line
    for line in lines:
        parts = line.strip().split(' ')
        timestamp = parts[0]
        event = parts[1]
        job = parts[2]

        if job == "scheduler":
            continue
        if event == "start":
            core = int(parts[-1])
            last_core = core
        elif event == "update_cores":
            core_array = parts[-1]
            total_cores = 0
            # count the number of ints in the string
            for ch in core_array:
                if ch.isdigit():
                    total_cores += 1
            core = total_cores
            last_core = core
        elif event == "end":
            core = last_core
        else:
            raise ValueError(f"Unknown event {event}")

        if job in jobs_list:
            if job not in data.keys():
                data[job] = {}
                data[job]['cores'] = []
                data[job]['time'] = []

            data[job]['cores'].append(core)
            data[job]['time'].append(timestamp)

    for job in data.keys():
        # Create a dataframe from the extracted data
        df = {'time': data[job]['time'], 'cores': data[job]['cores']}

        df = pd.DataFrame(df)
        df['time'] = pd.to_datetime(df['time'])
        df['time'] = (df['time'] - df['time'][0]).dt.total_seconds()
        data[job]['df'] = df
        if job != "memcached":
            memcached_start_time = pd.to_datetime(data['memcached']['time'][0])
            job_start_time = pd.to_datetime(data[job]['time'][0])
            data[job]['start_time'] = (job_start_time - memcached_start_time).total_seconds()
            data[job]['end_time'] = (job_start_time - memcached_start_time).total_seconds() + df['time'].max()

    return data


def annotate_plot(annotations, ax, ax2, default_offset_x=10, default_offset_y=2.4, offset_x=-55, offset_y=2.3):
    # Add annotations to the plot
    print(annotations)
    for key, value in annotations.items():
        if value['text'] == r'\bf{radix}':
            x = offset_x
        else:
            x = default_offset_x
        if value['text'] == r'\bf{blackscholes}':
            y = offset_y
        else:
            y = default_offset_y
        ax.annotate(value['text'], (key, y), (x, y),
                    xycoords='data', textcoords='offset points',
                    color=value['color'], fontsize=20)
        ax2.axvline(x=key, color=value['color'], linestyle='--', linewidth=2.5, zorder=0)


def configure_xticks(annotations, ax, max_end_time, min_start_time):
    xticks = ax.get_xticks()
    xticks_jobs = list(annotations.keys())

    xticks = np.append(xticks, xticks_jobs)
    # xticks = xticks_jobs
    xticks.sort()
    new_xticks = []
    for x in xticks:
        if x == min_start_time or x == max_end_time:
            continue
        new_xticks.append(x)
    ax.set_xticks(new_xticks)
    return new_xticks


def create_parsec_annotations(parsec_data, job_colors):
    texts = list(parsec_data.keys())
    texts = [x for x in texts if x != 'memcached']
    colors = []
    x_positions = []
    max_end_time = 0
    min_start_time = 100000
    for job in texts:
        colors.append(job_colors[job])
        x_positions.append(parsec_data[job]['start_time'])
        max_end_time = max(parsec_data[job]['end_time'], max_end_time)
        min_start_time = min(parsec_data[job]['start_time'], min_start_time)
    # Create the annotations dictionary dynamically
    annotations = {}
    for i in range(len(texts)):
        x = x_positions[i]
        text = texts[i]
        text = r'\bf{' + text + '}'
        color = colors[i]
        annotations[x] = {'text': text, 'color': color}
    return annotations, max_end_time, min_start_time


def add_annotated_text_plot(ax, max_end_time, min_start_time, intervals_placement, relative_offset_xticks, run):
    new_ax = ax.twiny()
    new_ax.spines["bottom"].set_linewidth(2)
    new_ax.spines["bottom"].set_color('red')
    new_ax.spines["bottom"].set_position(("axes", -0.05))
    new_ax.set_xlim(ax.get_xlim())
    new_ax.set_xticks([])
    new_ax.spines["bottom"].set_bounds(min_start_time, max_end_time)
    new_ax.annotate(r'\bf{[}', xy=intervals_placement[run][0], textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    # round to 2 decimal places
    min_start_time = str(round(min_start_time, 2))
    max_end_time = str(round(max_end_time, 2))
    new_ax.annotate(r'\bf{' + min_start_time + r'}', xy=(0.045, -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{]}', xy=intervals_placement[run][1], textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{' + max_end_time + r'}', xy=(relative_offset_xticks[run], -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{PARSEC Jobs Execution Time}', xy=(0.4, -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
