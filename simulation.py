from matplotlib.colors import Normalize
from numpy.core.fromnumeric import size
from task import task, task_queue as tq
from global_scheduler import gs
import matplotlib.pyplot as plt
import numpy as np
import utils


task_set_benchmark = [
    task(name="Task 1", p=3000.0, et=1000.0, ddl=3000.0),
    task(name="Task 2", p=4000.0, et=1000.0, ddl=4000.0),
    task(name="Task 3", p=6000.0, et=2000.0, ddl=6000.0),
    # task(name="Task 4", p=3000.0, et=500.0, ddl=3000.0),
    # task(name="Task 5", p=4000.0, et=1200.0, ddl=4000.0),
    # task(name="Task 6", p=6000.0, et=2100.0, ddl=6000.0),
    # task(name="Task 7", p=3000.0, et=800.0, ddl=3000.0),
    # task(name="Task 8", p=4000.0, et=200.0, ddl=4000.0),
    # task(name="Task 9", p=6000.0, et=2400.0, ddl=6000.0),
    # task(name="Task 10", p=4000.0, et=1200.0, ddl=4000.0),
    # task(name="Task 11", p=6000.0, et=210.0, ddl=6000.0),
    # task(name="Task 12", p=3000.0, et=800.0, ddl=3000.0),
    # task(name="Task 13", p=4000.0, et=200.0, ddl=4000.0),
    # task(name="Task 14", p=6000.0, et=1200.0, ddl=6000.0)
]

task_set = tq()
for task_i in task_set_benchmark:
    task_set.append_task(task_i)

task_set.show_task_queue_info()
test_gs = gs()
test_gs.load_task_queue(task_set_benchmark, utils.simulation_type['dvfs'])
u_d_on, u_o_on = test_gs.check_u(utils.simulation_type['dvfs'])
e_d_on, e_o_on = test_gs.check_energy(utils.simulation_type['dvfs'])

test_gs = gs()
test_gs.load_task_queue(task_set_benchmark, utils.simulation_type['normal'])
u_d_off, u_o_off = test_gs.check_u(utils.simulation_type['normal'])
e_d_off, e_o_off = test_gs.check_energy(utils.simulation_type['normal'])

def compare_analysis(u_o_on, u_o_off, e_o_on, e_o_off):
    # make data
    # x = [1, 2, 3, 4]
    # colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
    fig2 = plt.figure(figsize=(20,10))
    fig2.suptitle("DVFS: ON vs OFF", fontsize=16)
    # plot
    
    index_1 =  (u_o_on > 0.0)
    index_2 =  (u_o_off > 0.0)
    index_3 =  (e_o_on > 0.0)
    index_4 =  (e_o_off > 0.0)

    u_colors = ['blue', 'dodgerblue', 'lightblue', 'red', 'limegreen','purple']
    u_labels = ['NL','TLD', 'JLD', 'MISS', 'T OH','P OH']
    
    ax1 = fig2.add_subplot(2,4,1)
    # ax1.xaxis.set_label_position('top')
    ax1.set_title('Utilization(DVFS: ON)', y = 1.1)
    ax1.pie([u_o_on[i] for i in range(1, len(u_o_on)) if index_1[i]], labels=[u_labels[i] for i in range(len(u_o_on) - 1) if index_1[i + 1]],colors=u_colors, autopct='%1.0f%%', pctdistance=1.1, startangle=90, labeldistance=1.16, normalize=False, rotatelabels=True)
    plt.xlabel("Utilization: " + '{0:3.1f}'.format(u_o_on[0] * 100.0) + "%")
    # plt.legend(u_labels, loc="best")
    ax2 = fig2.add_subplot(2,4,2)
    ax2.set_title('Utilization(DVFS: OFF)', y = 1.1)
    ax2.pie([u_o_off[i] for i in range(1, len(u_o_off)) if index_2[i]], labels=[u_labels[i] for i in range(len(u_o_off) - 1) if index_2[i + 1]],colors=u_colors, autopct='%1.0f%%', pctdistance=1.1, startangle=90, labeldistance=1.16, normalize=False, rotatelabels=True)
    plt.xlabel("Utilization: " + '{0:3.1f}'.format(u_o_off[0] * 100.0) + "%")
    # plt.legend(u_labels, loc="best")

    e_colors = ['blue', 'dodgerblue', 'lightblue','purple', 'crimson']
    e_labels = ['NL','TLD', 'JLD','P OH', 'IDLE']

    ax3 = fig2.add_subplot(2,4,3)
    ax3.set_title('Power(DVFS: ON)', y = 1.1)
    ax3.pie([e_o_on[i] for i in range(1, len(e_o_on)) if index_3[i]], labels=[e_labels[i] for i in range(len(e_o_on) - 1) if index_3[i + 1]],colors=e_colors, autopct='%1.0f%%', pctdistance=1.1, startangle=90, labeldistance=1.16, normalize=True, rotatelabels=True)
    plt.xlabel("Power: " + '{0:.1f}'.format(e_o_on[0]) + " Watts")
    # plt.legend(e_labels, loc="best")
    ax4 = fig2.add_subplot(2,4,4)
    ax4.set_title('Power(DVFS: OFF)', y = 1.1)
    ax4.pie([e_o_off[i] for i in range(1, len(e_o_off)) if index_4[i]], labels=[e_labels[i] for i in range(len(e_o_off) - 1) if index_4[i + 1]],colors=e_colors, autopct='%1.0f%%', pctdistance=1.1, startangle=90, labeldistance=1.16, normalize=True, rotatelabels=True)
    plt.xlabel("Power: " + '{0:.1f}'.format(e_o_off[0]) + " Watts")
    # plt.legend(e_labels, loc="best")

    u_colors_new = ['lightgreen', 'blue', 'dodgerblue', 'lightblue', 'red', 'limegreen','purple']
    u_labels_new = ['Total', 'Normal','Task-level\nDVFS', 'Job-level\nDVFS', 'Miss\n DDL', 'Transformation\n Overhead','Preemption\n Overhead']

    ax5 = fig2.add_subplot(2, 2, 3)
    x = range(len(u_colors_new))
    for j in range(len(u_colors_new)):
        value = u_o_on[j] - u_o_off[j]
        ax5.bar(x[j], value, width=0.8, label=u_labels_new[j], color=u_colors_new[j])
        y_pos = 0.01
        anchor = 'bottom'
        sign = '+'
        if (value < 0):
            y_pos = -y_pos
            anchor = 'top'
            sign = '-'
        plt.text(x[j], value + y_pos,
                sign + '{0:3.1f}'.format(value * 100.0) + "%", horizontalalignment='center', verticalalignment=anchor, fontsize=10)
        plt.legend(['Total', 'Normal','Task-level DVFS', 'Job-level DVFS', 'Miss DDL', 'T Overhead','P Overhead'], loc="lower center",bbox_to_anchor=(0.5, 1.05), 
            ncol=4)
    plt.hlines(y = 0, xmin=-1, xmax= len(u_colors_new) + 1, linewidth=0.6 , colors = 'black', linestyles='dotted', zorder=-1)
    plt.xlim(-0.6, len(u_colors_new) - 0.4)
    plt.xticks(range(len(u_colors_new)), [u_labels_new[i] for i in range(len(u_colors_new))], fontsize=8)
    plt.ylim(-1.08, 1.08)
    plt.yticks([i / 10 for i in range(-10, 11)], [str(i * 10) + " %" for i in range(-10, 0)] + [str(i * 10) + " %" for i in range(11)])
    
    e_colors_new = ['lightgreen', 'blue', 'dodgerblue', 'lightblue','purple', 'crimson']
    e_labels_new = ['Total', 'Normal','Task-level\nDVFS', 'Job-level\nDVFS','Preemption\n Overhead', 'Idle']
    
    ax6 = fig2.add_subplot(2, 2, 4)

    x = range(len(e_colors_new))
    for j in range(len(e_colors_new)):
        value = e_o_on[j] - e_o_off[j]
        ax6.bar(x[j], value, width=0.8, label=e_labels_new[j], color=e_colors_new[j])
        y_pos = 0.01
        anchor = 'bottom'
        sign = '+'
        if (value < 0):
            y_pos = -y_pos
            anchor = 'top'
            sign = '-'
        if(j == 0):
            plt.text(x[j], value + y_pos,
                sign + '{0:.1f}'.format(value) + '({0:3.1f}%)'.format(np.abs(e_o_on[j] - e_o_off[j]) / e_o_off[j] * 100), horizontalalignment='center', verticalalignment=anchor, fontsize=10)
        else:
            plt.text(x[j], value + y_pos,
                sign + '{0:.1f}'.format(value), horizontalalignment='center', verticalalignment=anchor, fontsize=10)
        plt.legend(['Total', 'Normal','Task-level DVFS', 'Job-level DVFS','P Overhead', 'Idle'], loc="lower center",bbox_to_anchor=(0.5, 1.05), 
            ncol=4)
    plt.hlines(y = 0, xmin=-1, xmax= len(u_colors_new) + 1, linewidth=0.6 , colors = 'black', linestyles='dotted', zorder=-1)
    plt.xlim(-0.6, len(e_colors_new) - 0.4)
    plt.xticks(range(len(e_colors_new)), [e_labels_new[i] for i in range(len(e_colors_new))], fontsize=10)
    ax6.set(ylim=(-1250, 1250.0))
    ax6.set_ylabel("Power(Watts)")
    
    # patches, texts = ax.pie(sizes, colors=colors, shadow=True, startangle=90)
    # plt.legend(patches, labels, loc="best")
    # plt.axis('equal')

    # fig, ax = plt.subplots()
    # ax.pie(x, colors=colors, radius=3, center=(4, 4),
    #     wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
    #     ylim=(0, 8), yticks=np.arange(1, 8))
    # plt.axes.xaxis.set_visible(False)
    # plt.axes.yaxis.set_visible(False)

compare_analysis(u_o_on, u_o_off, e_o_on, e_o_off)

plt.show()
# task_q1 = tq()
# task_q1.append_task(task1)
# task_q1.append_task(task2)
# task_q1.append_task(task3)
# task_q1.show_task_queue_info()
# task_q1.priority_sort_by_period()
# task_q1.show_task_queue_info()
# rma = RMA(task_q1)
# print(rma.Schedulablity_RMA())
# print(rma.schedulablity)
# print(rma.lcm_time)
# rma.RMA_schedule()
# gantt_charts.gantt_chart_generate(rma.job_queue, task_q1)
