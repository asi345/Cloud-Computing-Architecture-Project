import argparse

from utils import *

# -----------GLOBALS-------------


RUNS = 3

def create_memcached_plot(xticks, xtick_labels, data, parsec_data, run, q_num):
    fig, ax = plt.subplots(figsize=(20, 12))

    # label_str = label_mapping(label)
    labels = [r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', r'\bf{QPS}']

    # Sample input data
    annotations, max_end_time, min_start_time = create_parsec_annotations(parsec_data, JOB_COLORS)
    print(len(data))
    print(len(xticks))
    # add line to connect markers
    ax.scatter(xticks, data['p95'], color='blue', marker='x', s=100, zorder=9)
    ax.plot(xticks, data['p95'], color='blue', linewidth=3.5, label=labels[0], zorder=9)
    ax.set_xlabel(r"\bf{Time} $(s)$", size=15)
    ax.set_ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', rotation=0, size=15)
    ax.yaxis.set_label_coords(0.0, 1.01)
    ax.xaxis.set_label_coords(0.5, -0.11)
    ax.set_ylim([0, 2])

    ax2 = ax.twinx()
    ax2.set_axisbelow(True)
    ax.grid(axis='y', color='white', linewidth=2.0, zorder=3)

    # ax2.scatter(xticks, data['QPS'], color='darkblue', marker='o', s=50, zorder=9, alpha=0.6)
    # ax2.plot(xticks, data['QPS'], color='darkblue', linewidth=2, label=labels[1], zorder=9, alpha=0.6)
    ax2.fill_between(xticks, data['QPS'], color='darkorange', alpha=0.2, zorder=2, label=labels[1])

    ax2.set_ylabel(r'\bf{QPS}', rotation=0, size=15)
    ax2.set_ylim([0, 130000])
    yticks, yticks_labels = get_yticks(130000)
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticks_labels)
    ax2.yaxis.set_label_coords(1.0, 1.03)

    # formatting xticks
    xticks_jobs = list(annotations.keys())
    xticks_jobs.sort()
    interval = np.arange(200, 1400, 200)
    xticks_jobs = np.concatenate((xticks_jobs, interval))
    xticks_jobs.sort()
    # pop the elements which have absolute difference less than 20
    xticks = []
    for i in range(len(xticks_jobs)):
        if i == 0:
            xticks.append(xticks_jobs[i])
        else:
            if abs(xticks_jobs[i] - xticks_jobs[i - 1]) > 20:
                xticks.append(xticks_jobs[i])
    # xticks_jobs.sort()
    ax.set_xticks(xticks)
    xtick_labels = [f"${str(int(x))}$" for x in xticks]
    ax.set_xticklabels(xtick_labels, ha='center', size=16)
    # new_xticks = configure_xticks(annotations, ax2, max_end_time, min_start_time)
    # new_xticks = new_xticks[1:-1]
    # ax.set_xticks(new_xticks)
    # xtick_labels = [str(int(x)) for x in new_xticks]
    #

    annotate_plot(annotations, ax, ax2, default_offset_y=1.75, offset_y=1.65)

    # setup plotting related styling
    run_num = str(run + 1)
    type = 'A' + run_num
    plt.suptitle(r"\bf{\textit{" + f"{type}" + r"  -  Measured Tail Latency of Memcached with Dynamic Load" + ' (QPS interval = ' + str(qps_interval) + 's)}' + "}",
                 x=0.5,
                 y=0.97,
                 fontsize=20)

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=18)

    # Combine the legend handles and labels from both plots
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2
    # plt.gcf().autofmt_xdate()
    # Create a legend with the combined handles and labels
    plt.legend(handles, labels, prop={'size': 14.5}, loc='upper right')
    plt.gcf().autofmt_xdate()

    ax.set_facecolor((0.92, 0.92, 0.92))
    add_annotated_text_plot(ax, max_end_time, min_start_time, INTERVALS_PLACEMENT, RELATIVE_OFFSET_XTICKS, run)
    plt.tight_layout()
    plt.savefig('A' + run_num + 'Q' + q_num +'.pdf')
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
        INTERVALS_PLACEMENT = [((0.045, -0.04), (0.663, -0.04)),
                               ((0.045, -0.04), (0.685, -0.04)),
                               ((0.045, -0.04), (0.664, -0.04))]

        RELATIVE_OFFSET_XTICKS = [0.67, 0.69, 0.67]
        qps_interval = 8
    else:
        raise ValueError('Invalid question number')

    FILE_NAME = f'{results_path}/memcached_'
    parsec_file_name = f'{results_path}/log_'

    for run in range(RUNS):
        parsec_data = get_parsec_data(parsec_file_name, run)
        memcached_data = get_memcached_data(FILE_NAME, run)
        max_time = parsec_data['memcached']['df']['time'].max()
        # add x seconds to max time, so it reaches 20 minutes
        max_time += (1200 - max_time)

        # compute step in terms of qps_interval
        step = 1200 // qps_interval
        xticks, xtick_labels = get_xticks(max_time, step=step)
        # each row in memcached_data is a 10-second interval so trim it to 20 minutes
        memcached_data = memcached_data.iloc[:step, :]
        create_memcached_plot(xticks, xtick_labels, memcached_data, parsec_data, run, args.q)
