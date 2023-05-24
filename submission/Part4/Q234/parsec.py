import argparse

from utils import *

# -----------GLOBALS-------------

RUNS = 3

MARKERS = ['o', '<', '^', 'v', 's', 'X', 'D']
COLORS = ['darkgreen', 'tab:olive', 'blue', 'purple', 'red', 'darkorange', 'aqua']

PRIORITY = [2, 7, 3, 4, 5, 6, 5]  # zorder for error bars and lines

def create_parsec_plot(parsec_data, memcached_data, run, q_num):
    fig, ax = plt.subplots(figsize=(20, 12))
    plt.grid(axis='y', color='white', linewidth=2.0, zorder=0)
    plt.grid(axis='x', color='white', linewidth=2.0, zorder=0)
    # label_str = label_mapping(label)
    labels = [r'\bf{CPU Cores}', r'\bf{QPS}']

    # Sample input data
    annotations, max_end_time, min_start_time = create_parsec_annotations(parsec_data, JOB_COLORS)

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
    configure_xticks(annotations, ax, max_end_time, min_start_time)

    ax2 = ax.twinx()
    ax2.scatter(memcached_data['time'], memcached_data['QPS'], color=COLORS[-2], marker=MARKERS[0], s=50, alpha=0.6)
    ax2.plot(memcached_data['time'], memcached_data['QPS'], color=COLORS[-2], linewidth=2, label=labels[1], alpha=0.6)
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
    plt.suptitle(r"\bf{\textit{" + f"{type}" + r"  -  Controller policy performance under various PARSEC workloads" + ' (QPS interval = ' + str(qps_interval) + 's)}' + "}",
                 x=0.5,
                 y=0.97,
                 fontsize=20)

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)

    # Combine the legend handles and labels from both plots
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2

    annotate_plot(annotations, ax, ax2)

    # Create a legend with the combined handles and labels
    plt.legend(handles, labels, prop={'size': 14.5}, loc='upper right')
    ax.set_facecolor((0.92, 0.92, 0.92))
    # Automatically adjust the x-axis tick labels to prevent overlapping
    plt.gcf().autofmt_xdate()

    add_annotated_text_plot(ax, max_end_time, min_start_time, INTERVALS_PLACEMENT, RELATIVE_OFFSET_XTICKS, run)
    plt.tight_layout()
    plt.savefig('B' + run_num + 'Q' + q_num + '.pdf')
    plt.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Plot memcached data')
    parser.add_argument('-q', type=str, help='Question to run', required=True)

    args = parser.parse_args()

    if args.q == '3':
        results_path = 'Q3'
        INTERVALS_PLACEMENT = [((0.045, -0.04), (0.766, -0.04)),
                               ((0.045, -0.04), (0.764, -0.04)),
                               ((0.045, -0.04), (0.705, -0.04))]

        RELATIVE_OFFSET_XTICKS = [0.77, 0.77, 0.708]
        qps_interval = 10
    elif args.q == '4':
        results_path = 'Q4'
        INTERVALS_PLACEMENT = [((0.045, -0.04), (0.766, -0.04)),
                               ((0.045, -0.04), (0.764, -0.04)),
                               ((0.045, -0.04), (0.705, -0.04))]

        RELATIVE_OFFSET_XTICKS = [0.77, 0.77, 0.708]
        qps_interval = 7
    else:
        raise ValueError('Invalid question number')

    memcached_file_name = f'{results_path}/memcached_'
    parsec_file_name = f'{results_path}/log_'

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
        create_parsec_plot(parsec_data, memcached_data, run, args.q)
