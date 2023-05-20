from utils import *

# -----------GLOBALS-------------


RUNS = 3
FILE_NAME = "results/memcached_output_"
parsec_file_name = "results/log_"

INTERVALS_PLACEMENT = [((0.045, -0.04), (0.807, -0.04)),
                       ((0.045, -0.04), (0.84, -0.04)),
                       ((0.045, -0.04), (0.7, -0.04))]

RELATIVE_OFFSET_XTICKS = [0.803, 0.84, 0.7]

def create_memcached_plot(xticks, xtick_labels, data, parsec_data, run):
    fig, ax = plt.subplots(figsize=(20, 12))
    plt.grid(axis='y', color='white', linewidth=2.0, zorder=0)
    plt.grid(axis='x', color='white', linewidth=2.0, zorder=0)
    # label_str = label_mapping(label)
    labels = [r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', r'\bf{QPS}']

    # Sample input data
    annotations, max_end_time, min_start_time = create_parsec_annotations(parsec_data, JOB_COLORS)
    # add line to connect markers
    ax.scatter(xticks, data['p95'], color='darkorange', marker='x', s=100, zorder=9)
    ax.plot(xticks, data['p95'], color='darkorange', linewidth=3.5, label=labels[0], zorder=9)
    ax.set_xlabel(r"\bf{Time} $(s)$", size=15)
    ax.set_ylabel(r'$\bf{95}^{th}$ \bf{Percentile Latency (ms)}', rotation=0, size=15)

    ax.yaxis.set_label_coords(0.0, 1.01)
    ax.xaxis.set_label_coords(0.5, -0.11)
    ax.set_ylim([0, 2])

    ax2 = ax.twinx()
    ax2.scatter(xticks, data['QPS'], color='darkblue', marker='o', s=50, zorder=9, alpha=0.6)
    ax2.plot(xticks, data['QPS'], color='darkblue', linewidth=2, label=labels[1], zorder=9, alpha=0.6)
    ax2.set_ylabel(r'\bf{QPS}', rotation=0, size=15)
    ax2.set_ylim([0, 130000])
    yticks, yticks_labels = get_yticks(130000)
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticks_labels)
    ax2.yaxis.set_label_coords(1.0, 1.03)

    # formatting xticks
    xticks_jobs = list(annotations.keys())
    xticks_jobs.sort()
    xticks_jobs.append(1200)
    ax.set_xticks(xticks_jobs)
    xtick_labels = [f"${str(int(x))}s$" for x in xticks_jobs]
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
    plt.suptitle(r"\bf{\textit{" + f"{type}" + r"  -  Measured Tail Latency of Memcached with Dynamic Load}}",
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
    ax.set_facecolor((0.92, 0.92, 0.92))
    add_annotated_text_plot(ax, max_end_time, min_start_time, INTERVALS_PLACEMENT, RELATIVE_OFFSET_XTICKS, run)
    plt.tight_layout()
    plt.savefig('A' + run_num + 'Q3.pdf')
    plt.close()


if __name__ == "__main__":
    for run in range(RUNS):
        parsec_data = get_parsec_data(parsec_file_name, run)
        memcached_data = get_memcached_data(FILE_NAME, run)
        max_time = parsec_data['memcached']['df']['time'].max()
        # add x seconds to max time, so it reaches 20 minutes
        max_time += (20 * 60 - max_time)
        xticks, xtick_labels = get_xticks(max_time, step=120)
        # each row in memcached_data is a 10-second interval so trim it to 20 minutes
        memcached_data = memcached_data.iloc[:120, :]
        create_memcached_plot(xticks, xtick_labels, memcached_data, parsec_data, run)
