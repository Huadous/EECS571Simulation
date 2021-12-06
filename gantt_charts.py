import matplotlib
from numpy.core.fromnumeric import size
import plotly.express as px
import pandas as pd
import numpy as np
from job import job, job_queue as jq
from task import task, task_queue as tq
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# fig.suptitle('CPU-GPU Clusters Gantt Charts',size=20, x = 0.0, y = 1.0)

def gantt_chart_generate(fig, hand_list, labl_list, job_q: jq, task_q: tq, cluster_num, cluster_id, gpu_num, gpu_id, type):
    """[Based on the taskqueue and can use the function provided by the scheduler to generate the gantt chart to
    show the scheduling status of each GPU]

    Args:
        taskqueue ([type]): [the queue of tasks and it contains the tasks]
    """
    colors = ['red', 'blue', 'limegreen','purple','dodgerblue', 'lightblue']
    labels = ['-miss ddl','-normal execute', '-Transformation Overhead','-Preemption Overhead','-task-level dvfs', '-job-level dvfs']
    job_status = {'mis': 0, 'exec': 1, 'T_oh': 2,
              'P_oh': 3, 'tl_dvfs': 4, 'jl_dvfs': 5}

    linewidth = [15,15,15,15]
    ax = fig.add_subplot(cluster_num , gpu_num, cluster_num * (cluster_id - 1) + gpu_id)
    
    ax.title.set_text('Cluster ' + str(cluster_id) + ", GPU " + str(gpu_id))

    output_data, num_of_status = job_q.transform_gantt_charts_data(type)

    for i, data in enumerate(output_data[3]):
        ax = plt.hlines(output_data[0][i], output_data[1][i], output_data[2][i], linewidth=7, colors=colors[data], label=labels[data], )

    for i, data in enumerate(output_data[3]):
        if (output_data[5][i]):
            # ax = plt.scatter(output_data[2][i], output_data[0][i], s=100, facecolors='none', edgecolors='orange', marker='|', label="complete job", zorder=3)
            ax = plt.scatter(output_data[2][i], output_data[0][i], s=150, c='red', marker='|', label="complete job", zorder=3)


    for task in task_q.task_queue:
        ax = plt.scatter([i * task.period for i in range(int(np.floor(job_q.lcm_time * 1.2 / task.period)))], [task.name for i in range(int(np.floor(job_q.lcm_time * 1.2 / task.period)))], s=100, facecolors='none', edgecolors='r', marker='d', label="release job", zorder=3)

    if (cluster_id == cluster_num and gpu_id == gpu_num):
        add_legend(fig, hand_list, labl_list)

    # plt.yticks(range(len(task_q.task_queue) + 2), ['1'] + [r'$\text{{Task}}_{{{}}}$'.format(int(task.name[-1])) for task in task_q.task_queue] + ['1a'], rotation=45)  # Set text labels and properties.
    plt.xlim(0 - job_q.lcm_time * 0.04, job_q.lcm_time * 1.04)
    plt.xlabel("Real-Time clock")
    if (len(task_q.task_queue) == 1):
        plt.vlines(x = job_q.time_line + [job_q.lcm_time], ymin=-1, ymax=1, linewidth=0.6, colors = ['black'] * len(job_q.time_line + [job_q.lcm_time]), linestyles='dashdot', zorder=-1)
    else:
        plt.vlines(x = job_q.time_line + [job_q.lcm_time], ymin=0, ymax=len(task_q.task_queue) - 1, linewidth=0.6, colors = ['black'] * len(job_q.time_line + [job_q.lcm_time]), linestyles='dashdot', zorder=-1)
    plt.hlines(y = range(len(task_q.task_queue)), xmin=0, xmax=job_q.lcm_time, linewidth=0.6 , colors = ['black'] * len(task_q.task_queue), linestyles='dotted', zorder=-1)
    # plt.xticks(np.arange(min(output_data[1]), max(output_data[2])+1, 1.0))
    plt.show(block=False)
    handles, labels = plt.gca().get_legend_handles_labels()
    # print(type(handles))
    hand_list += handles
    labl_list += labels


def add_legend(fig, hand_list, labl_list):


    # lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    # lines, labels = [sum(lol, []) for lol in zip(*list(set_container))]
    # # fig.legend(lines, labels)
    

    # lines, labels = fig.axes[-1].get_legend_handles_labels()]
    handls = []
    labels = []

    for h,l in zip(hand_list,labl_list):
       if l not in labels:
            labels.append(l)
            handls.append(h)
    
    index = np.argsort(labels).tolist()
    # print(index)

    labels = [labels[i] for i in index]
    handls = [handls[i] for i in index]

    print(len(handls), len(labels))
    fig.legend(handls, labels, loc="lower center",
            ncol=4, fancybox=True, shadow=True)

    # fig.legend(by_label.values(), by_label.keys(), loc="lower right", bbox_to_anchor=(1., -.3),
    #         ncol=5, fancybox=True, shadow=True)

if __name__ == '__main__':
    pass