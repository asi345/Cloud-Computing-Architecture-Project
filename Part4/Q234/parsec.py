import numpy as np

from utils import *
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

# -----------GLOBALS-------------
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 16,
    "errorbar.capsize": 4
})

RUNS = 3

MARKERS = ['o', '<', '^', 'v', 's', 'X', 'D']
COLORS = ['darkgreen', 'tab:olive', 'blue', 'purple', 'red', 'darkorange', 'aqua']

JOB_COLORS = {
    'dedup': '#CCACCA',
    'ferret': '#AACCCA',
    'freqmine': '#0CCA00',
    'vips': '#CC0A00',
    'canneal': '#CCCCAA',
    'blackscholes': '#CCA000',
    'radix': '#00CCA0'
}

PRIORITY = [2, 7, 3, 4, 5, 6, 5]  # zorder for error bars and lines

parsec_file_name = "results/log_"
memcached_file_name = "results/memcached_output_"

INTERVALS_PLACEMENT = [((0.045, -0.04), (0.807, -0.04)),
                       ((0.045, -0.04), (0.84, -0.04)),
                       ((0.045, -0.04), (0.7, -0.04))]

RELATIVE_OFFSET_XTICKS = [0.803, 0.84, 0.7]

def create_parsec_plot(parsec_data, memcached_data, run):
    fig, ax = plt.subplots(figsize=(20, 12))
    plt.grid(axis='y', color='white', linewidth=2.0, zorder=0)
    plt.grid(axis='x', color='white', linewidth=2.0, zorder=0)
    # label_str = label_mapping(label)
    labels = [r'\bf{CPU Cores}', r'\bf{QPS}']

    # Sample input data
    texts = list(parsec_data.keys())
    texts = [x for x in texts if x != 'memcached']
    colors = []
    x_positions = []
    max_end_time = 0
    min_start_time = 100000
    for job in texts:
        colors.append(JOB_COLORS[job])
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

    print(annotations)

    memcached_run = parsec_data['memcached']
    cores = memcached_run['df']['cores'].astype(float)
    time = memcached_run['df']['time']

    # if difference in cores in 0.2 seconds is 1, then remove it
    for i in range(len(cores) - 1):
        if abs(cores[i] - cores[i + 1]) == 1 and abs(time[i] - time[i + 1]) <= 1:
            cores[i + 1] = cores[i]
            time[i + 1] = time[i]

    # extend time and cores to 1200 seconds
    time = np.append(time, [1200])
    cores = np.append(cores, [cores.iloc[-1]])
    ax.step(time, cores, color=COLORS[2], linewidth=2, zorder=8, label=labels[0], where='post')
    ax.set_xlabel(r"\bf{Time} $(s)$", size=18)
    ax.set_ylabel(r'\bf{CPU Cores}', rotation=0, size=18)
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

    ax2 = ax.twinx()
    ax2.scatter(memcached_data['time'], memcached_data['QPS'], color=COLORS[-2], marker=MARKERS[0], s=50)
    ax2.plot(memcached_data['time'], memcached_data['QPS'], color=COLORS[-2], linewidth=2, label=labels[1])
    ax2.set_ylabel(r'\bf{QPS}', rotation=0, size=18)
    ax.set_ylim([0., 2.5])
    ax2.set_ylim([0, 130000])
    yticks, yticks_labels = get_yticks(130000)
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticks_labels)
    ax.yaxis.set_label_coords(0.01, 1.01)
    ax.xaxis.set_label_coords(0.5, -0.12)
    ax2.yaxis.set_label_coords(1.0, 1.03)

    run_num = str(run + 1)
    type = 'B' + run_num
    plt.suptitle(r"\bf{\textit{" + f"{type}." + r"Controller policy performance under various PARSEC workloads}}",
                 x=0.255,
                 y=0.97,
                 fontsize=20)

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)

    # Combine the legend handles and labels from both plots
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2

    # Add annotations to the plot
    for key, value in annotations.items():
        if value['text'] == r'\bf{radix}':
            offset_x = -55

        else:
            offset_x = 10
        if value['text'] == r'\bf{blackscholes}':
            offset_y = 2.3
        else:
            offset_y = 2.4
        ax.annotate(value['text'], (key, offset_y), (offset_x, offset_y),
                     xycoords='data', textcoords='offset points',
                     # arrowprops=dict(arrowstyle="->", lw=1),
                     color=value['color'], fontsize=20)
        ax2.axvline(x=key, color=value['color'], linestyle='--', linewidth=2.5, zorder=0)

    # Create a legend with the combined handles and labels
    plt.legend(handles, labels, prop={'size': 14.5}, loc='upper right')
    ax.set_facecolor((0.92, 0.92, 0.92))
    # Automatically adjust the x-axis tick labels to prevent overlapping
    plt.gcf().autofmt_xdate()

    new_ax = ax.twiny()
    new_ax.spines["bottom"].set_linewidth(2)
    new_ax.spines["bottom"].set_color('red')
    new_ax.spines["bottom"].set_position(("axes", -0.05))
    new_ax.set_xlim(ax.get_xlim())
    new_ax.set_xticks([])
    new_ax.spines["bottom"].set_bounds(min_start_time, max_end_time)
    new_ax.annotate(r'\bf{[}', xy=INTERVALS_PLACEMENT[run][0], textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    # round to 2 decimal places
    min_start_time = str(round(min_start_time, 2))
    max_end_time = str(round(max_end_time, 2))

    new_ax.annotate(r'\bf{' + min_start_time + r'}', xy=(0.045, -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{]}', xy=INTERVALS_PLACEMENT[run][1], textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{' + max_end_time + r'}', xy=(RELATIVE_OFFSET_XTICKS[run], -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    new_ax.annotate(r'\bf{PARSEC Jobs Execution Time}', xy=(0.4, -0.07), textcoords='offset points',
                    xycoords='axes fraction', ha='center', va='top', size=16,
                    color='red')
    plt.tight_layout()
    plt.savefig('plot_parsec_' + str(run) + '.pdf')
    plt.close()


if __name__ == "__main__":
    for run in range(RUNS):
        parsec_data = get_parsec_data(parsec_file_name, run)
        memcached_data = get_memcached_data(memcached_file_name, run)
        max_time = parsec_data['memcached']['df']['time'].max()
        # add x seconds to max time, so it reaches 20 minutes
        max_time += (20 * 60 - max_time)
        xticks, xtick_labels = get_xticks(max_time, step=10)
        print(max_time)
        print(len(memcached_data))
        # each row in memcached_data is a 10-second interval so trim it to 20 minutes
        memcached_data = memcached_data.iloc[:120, :]
        # create the time column which is cumulative sum of 10-second intervals
        time_intervals = np.linspace(0, 1200, 120, endpoint=True)
        memcached_data['time'] = time_intervals
        create_parsec_plot(parsec_data, memcached_data, run)
