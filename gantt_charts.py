import plotly.express as px
import pandas as pd
import numpy as np
from job import job, job_queue as jq
import matplotlib.pyplot as plt

def gantt_chart_generate(job_q: jq):
    """[Based on the taskqueue and can use the function provided by the scheduler to generate the gantt chart to
    show the scheduling status of each GPU]

    Args:
        taskqueue ([type]): [the queue of tasks and it contains the tasks]
    """
    colors = ['red','green','blue','orange','yellow']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # the data is plotted from_x to to_x along y_axis
    output_data, num_of_status = job_q.transform_gantt_charts_data()
    for i, data in enumerate(output_data[3]):
        ax = plt.hlines(output_data[0][i], output_data[1][i], output_data[2][i], linewidth=20, colors=colors[data])
    plt.title('Rate Monotonic scheduling')
    plt.grid(True)
    plt.xlabel("Real-Time clock")
    # plt.ylabel("HIGH------------------Priority--------------------->LOW")
    plt.xticks(np.arange(min(output_data[1]), max(output_data[2])+1, 1.0))
    plt.show()


if __name__ == '__main__':
    gantt_chart_generate()