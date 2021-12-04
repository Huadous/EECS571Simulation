import matplotlib
import plotly.express as px
import pandas as pd
import numpy as np
from job import job, job_queue as jq
from task import task, task_queue as tq
import matplotlib.pyplot as plt

def gantt_chart_generate(job_q: jq, task_q: tq):
    """[Based on the taskqueue and can use the function provided by the scheduler to generate the gantt chart to
    show the scheduling status of each GPU]

    Args:
        taskqueue ([type]): [the queue of tasks and it contains the tasks]
    """
    # plt.style.use('_mpl-gallery')
    colors = ['red','royalblue', 'lime','orange','green']
    labels = ['miss ddl','normal execute', 'overhead','orange','green']
    fig = plt.figure()
    # ax = fig.add_subplot(111)
    # arrow = r'$\uparrow$'
    # the data is plotted from_x to to_x along y_axis
    output_data, num_of_status = job_q.transform_gantt_charts_data()

    for i, data in enumerate(output_data[3]):
        ax1 = plt.hlines(output_data[0][i], output_data[1][i], output_data[2][i], linewidth=3, colors=colors[data], label=labels[data])
        # ax = plt.scatter(output_data[1][i], output_data[0][i], s=100, c='green', marker="|")
        # ax = plt.scatter(output_data[2][i], output_data[0][i], s=100, facecolors='none', edgecolors='orange', marker='o')
        
    for i, data in enumerate(output_data[3]):
        if (output_data[5][i]):
            ax = plt.scatter(output_data[2][i], output_data[0][i], s=100, facecolors='none', edgecolors='orange', marker='o', label="complete job")


    for task in task_q.task_queue:
        ax = plt.scatter([i * task.period for i in range(int(np.floor(job_q.lcm_time / task.period)))], [task.name for i in range(int(np.floor(job_q.lcm_time / task.period)))], s=100, facecolors='none', edgecolors='r', marker='d', label="release job")
    plt.title('Rate Monotonic scheduling')
    # plt.grid(True)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper right")
    plt.xlabel("Real-Time clock")
    # plt.ylabel("HIGH------------------Priority--------------------->LOW")
    plt.xticks(np.arange(min(output_data[1]), max(output_data[2])+1, 1.0))
    plt.show()


if __name__ == '__main__':
    gantt_chart_generate()