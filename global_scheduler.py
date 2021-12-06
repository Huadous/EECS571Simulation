import re
from matplotlib import widgets
from dvfs import job_level_dvfs
import utils
from CGpair import CGpairs
from task import task, task_queue as tq
from scheduler import RMA
from utils import Lcm_of_array
import gantt_charts
import matplotlib.pyplot as plt
import numpy as np




class gs:
    num_of_clusters = 2
    def __init__(self) -> None:
        self.CGC = [CGpairs("Cluster " + str(i + 1)) for i in range(gs.num_of_clusters)]

    def load_task_queue(self, task_queue: tq, type):
        task_queue[0].show_task_info()

        if (type == utils.simulation_type['dvfs']):
            for tk in task_queue:
                flag = False
                print(">" * 40)
                print(tk.show_task_info())
                self.CGC.sort(key=CGP_sort)
                for CGpair in self.CGC:
                    CGpair.show_info_short()

                for CGpair in self.CGC:
                    CGpair.show_name()
                    if (not CGpair.switch):
                        CGpair.switch = True
                    CGpair.gpu.sort(key=lambda gpu: gpu.scheduler.utilization)
                    for gpu in CGpair.gpu:
                        gpu.show_name()
                        if (gpu.scheduler.utilization == 0):
                            gpu.scheduler.add_task(tk)
                            if (gpu.scheduler.Schedulablity_RMA()):
                                # gpu.scheduler.
                                # tk.show_task_info()
                                print("status1")
                                flag = True
                                break
                            else:
                                tk.change_to_normal()
                                if (gpu.scheduler.Schedulablity_RMA()):
                                    print("status2")
                                    flag = True
                                    break
                                else:
                                    print("status3")
                                    tk.change_to_save_energy()
                                    gpu.scheduler.remove_task(tk)
                        else:
                            gpu.scheduler.add_task(tk)
                            if (not gpu.scheduler.Schedulablity_RMA()):
                                tk.change_to_normal()
                                if (gpu.scheduler.Schedulablity_RMA()):
                                    print("status4")
                                    flag = True
                                    break
                                else:
                                    print("status5")
                                    tk.change_to_save_energy()
                                    gpu.scheduler.remove_task(tk)
                            else:
                                print("status6")
                                flag = True
                                break

                    if (flag):
                        break
                print("<" * 40)
                if (not flag):
                    for CGpair in self.CGC:
                        CGpair.show_name()
                        for gpu in CGpair.gpu:
                            gpu.scheduler.add_task(tk)

                            record = []

                            for i in range(len(gpu.scheduler.task_queue.task_queue) - 1, -1, -1):
                                task_i = gpu.scheduler.task_queue.task_queue[i]
                                record.append(task_i)
                                task_i.change_to_normal()
                                if (gpu.scheduler.Schedulablity_RMA()):
                                    flag = True
                                    break

                            if (not flag):
                                for task in record:
                                    task.change_to_save_energy()
                                gpu.scheduler.remove_task(tk)
                            else:
                                break
                    
                    if (not flag):
                        print("not schedulable: ")
                        print(tk.show_task_info())
        else:
            for tk in task_queue:
                tk.change_to_normal()
                flag = False
                print(">" * 40)
                print(tk.show_task_info())
                self.CGC.sort(key=CGP_sort)
                for CGpair in self.CGC:
                    CGpair.show_info_short()

                for CGpair in self.CGC:
                    CGpair.show_name()
                    if (not CGpair.switch):
                        CGpair.switch = True
                    CGpair.gpu.sort(key=lambda gpu: gpu.scheduler.utilization)
                    for gpu in CGpair.gpu:
                        gpu.show_name()
                        # if (gpu.scheduler.utilization == 0):
                        #     gpu.scheduler.add_task(tk)
                        #     if (gpu.scheduler.Schedulablity_RMA()):
                        #         print("status1")
                        #         flag = True
                        #         break
                        #     else:
                        #         print("status2")
                        #         tk.change_to_save_energy()
                        #         gpu.scheduler.remove_task(tk)
                        # else:
                        gpu.scheduler.add_task(tk)
                        if (gpu.scheduler.Schedulablity_RMA()):
                            print("status1")
                            flag = True
                            break
                        else:
                            print("status2")
                            gpu.scheduler.remove_task(tk)

                    if (flag):
                        break

                if (not flag):
                    print("not schedulable: ")
                    print(tk.show_task_info())




    def check_overhead(self, data):
        pass
                
    
    def check_u(self, type):
        fig = plt.figure(figsize=(20,10))
        if (type == utils.simulation_type['dvfs']):
            fig.suptitle("CPU-GPU Clusters Scheduling Gantt Charts: On)", fontsize=16)
        else:
            fig.suptitle("CPU-GPU Clusters Scheduling Gantt Charts(DVFS: Off)", fontsize=16)
        hand_list = []
        labl_list = []
        for i in range(gs.num_of_clusters):
            self.CGC[i].show_info()
            self.CGC[i].start_service(fig, hand_list, labl_list, gs.num_of_clusters, type)
        
        self.CGC.sort(key=lambda CGC: utils.find_num(CGC.name))
        for CGpair in self.CGC:
            CGpair.gpu.sort(key=lambda gpu: utils.find_num(gpu.name))
        
        return self.plot_of_u(type)

    
    def check_energy(self, type):
        energy = np.zeros((gs.num_of_clusters, CGpairs.num_of_gpu_default, len(utils.energy_type)))
        for i, CGpair in enumerate(self.CGC):
            for j, gpu in enumerate(CGpair.gpu):
                energy[i][j] = gpu.scheduler.job_queue.check_energy()
                if (np.sum(energy[i][j] == np.zeros(len(utils.energy_type))) == len(energy[i][j]) and CGpair.switch):
                    energy[i][j][utils.energy_type['idle']] = 85
        print(energy, np.sum(energy))
        return self.plot_of_e(energy, type)

    def plot_of_e(self, energy ,type1):
        fig1 = plt.figure(figsize=(20,8))
        if (type1 == utils.simulation_type['dvfs']):
            fig1.suptitle("Energy Consumption(DVFS: On)", fontsize=16)
        else:
            fig1.suptitle("Energy Consumption(DVFS: Off)", fontsize=16)
        colors = ['lightgreen', 'blue', 'dodgerblue', 'lightblue','purple', 'crimson']
        labels = ['total', 'normal execute','task-level dvfs', 'job-level dvfs','P overhead', 'idle']
        # energy_type = {'normal': 0, 'tld': 1, 'jld': 2, 'po': 3, 'idle': 4}
        record = np.zeros((gs.num_of_clusters, CGpairs.num_of_gpu_default, len(labels)))
        
        for i, CGpair in enumerate(self.CGC):
            x = np.arange(CGpairs.num_of_gpu_default) 
            width = 0.14
            ax = fig1.add_subplot(2, gs.num_of_clusters, utils.find_num(CGpair.name))
            y = np.zeros((CGpairs.num_of_gpu_default, len(labels)))
            y[:,1:] = energy[i]
            y[:, 0] = np.sum(y, axis = 1)


            record[i] = y

            for j in range(len(labels)):
                width_i = width * j
                ax.bar(x + width_i, y[:, j], width=width, label=labels[j], color=colors[j])
                for index, value in enumerate(y[:, j]):
                    plt.text(index + width_i, value + 0.01,
                        '{0:.1f}'.format(value), horizontalalignment='center', verticalalignment='bottom', fontsize=8)
            plt.legend(loc='best')
    
            ax.title.set_text('Cluster ' + str(utils.find_num(CGpair.name)))
            ax.set(ylim=(0, 305.0))
            ax.set_ylabel("Power(Watts)")
            plt.xticks(range(CGpair.num_of_gpu_default), ["GPU " + str(i + 1) for i in range(CGpairs.num_of_gpu_default)])
            # plt.yticks([i / 10 for i in range(11)],[str(i * 10) + " %" for i in range(11)])

        ax2 = fig1.add_subplot(2,1,2)
        total = np.sum(record, axis=(0,1))
        width = 1.0
        for j in range(len(labels)):
            width_i = width * j
            ax2.bar(width_i, total[j], width=0.4, label=labels[j], color=colors[j])
            plt.text(width_i, total[j] + 0.01,
                    '{0:.1f}'.format(total[j]), horizontalalignment='center', verticalalignment='bottom', fontsize=12)
        ax2.title.set_text('Overall Energy Consumption')
        ax2.set(ylim=(0, 1250.0))
        plt.xticks(range(len(labels)), [labels[i] for i in range(len(labels))])
        ax2.set_ylabel("Power(Watts)")
        return record, total


    def plot_of_u(self, type1):
        fig1 = plt.figure(figsize=(20,8))
        if (type1 == utils.simulation_type['dvfs']):
            fig1.suptitle("Utilization(DVFS: On)", fontsize=16)
        else:
            fig1.suptitle("Utilization(DVFS: Off)", fontsize=16)
        colors = ['lightgreen', 'red', 'blue', 'limegreen','purple','dodgerblue', 'lightblue']
        labels = ['total', 'miss ddl','normal execute', 'T overhead','P overhead','task-level dvfs', 'job-level dvfs']
        type = [0, 2, 5, 6, 1, 3, 4]
        record = np.zeros((gs.num_of_clusters, CGpairs.num_of_gpu_default, len(type)))
        
        for i, CGpair in enumerate(self.CGC):
            x = np.arange(CGpairs.num_of_gpu_default) 
            width = 0.14
            ax = fig1.add_subplot(2, gs.num_of_clusters, utils.find_num(CGpair.name))
            y = np.zeros((len(type), CGpairs.num_of_gpu_default))
            for j, gpu in enumerate(CGpair.gpu):
                if len(gpu.scheduler.job_queue.job_queue) == 0:
                    y[:,j] = np.zeros(len(type))
                    continue
                for job in gpu.scheduler.job_queue.job_queue:
                    if (job.status == type[1] - 1):
                        y[1][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                    elif (job.status == type[2] - 1):
                        y[2][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                    elif (job.status == type[3] - 1):
                        y[3][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                    elif (job.status == type[4] - 1):
                        y[4][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                    elif (job.status == type[5] - 1):
                        y[5][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                    elif (job.status == type[6] - 1):
                        y[6][j] += job.execute_time_intervals[1] - job.execute_time_intervals[0]
                y[:, j] = y[:, j] / gpu.scheduler.job_queue.lcm_time
            y[0] = np.sum(y, axis = 0)


            record[i] = y.T

            for j in range(len(type)):
                width_i = width * j
                ax.bar(x + width_i, y[j], width=width, label=labels[type[j]], color=colors[type[j]])
                for index, value in enumerate(y[j]):
                    plt.text(index + width_i, value + 0.01,
                        '{0:3.1f}'.format(value * 100.0) + "%", horizontalalignment='center', verticalalignment='bottom', fontsize=8)
            plt.legend(loc='best')
    
            ax.title.set_text('Cluster ' + str(utils.find_num(CGpair.name)))
            ax.set(ylim=(0, 1.08))

            plt.xticks(range(CGpair.num_of_gpu_default), ["GPU " + str(i + 1) for i in range(CGpairs.num_of_gpu_default)])
            plt.yticks([i / 10 for i in range(11)],[str(i * 10) + " %" for i in range(11)])

        ax2 = fig1.add_subplot(2,1,2)
        total = np.sum(record, axis=(0,1)) / 4
        width = 1.0
        for j in range(len(type)):
            width_i = width * j
            ax2.bar(width_i, total[j], width=0.4, label=labels[type[j]], color=colors[type[j]])
            plt.text(width_i, total[j] + 0.01,
                    '{0:3.1f}'.format(total[j] * 100.0) + "%", horizontalalignment='center', verticalalignment='bottom', fontsize=12)
        ax2.title.set_text('Overall Utilization')
        ax2.set(ylim=(0, 1.08))
        plt.xticks(range(len(type)), [labels[type[i]] for i in range(len(type))])
        plt.yticks([i / 10 for i in range(11)],[str(i * 10) + " %" for i in range(11)])

        return record, total

def CGP_sort(CGP:CGpairs):
    min_u = CGP.gpu[0].scheduler.utilization
    if (not CGP.switch):
        return 999999
    for i in range(len(CGP.gpu)):
        min_u = min(min_u, CGP.gpu[i].scheduler.utilization)
    return min_u