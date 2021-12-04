from task import task
from task import task_queue as tq
from job import job
from job import job_queue as jq
import utils
import numpy as np
import math
import gantt_charts


class RMA:
    """[summary]
    """
    def __init__(self, task_queue: tq) -> None:
        self.task_queue = task_queue
        self.lcm_time = utils.Lcm_of_array(self.task_queue.return_preiods(), 0)
        self.num_of_task = task_queue.size()
        self.utilization_queue = np.zeros(self.num_of_task)
        self.utilization = 0
        self.schedulablity = np.zeros(self.num_of_task)
        self.job_queue = jq(self.lcm_time)

    def update_utilization(self):
        for i, task in enumerate(self.task_queue.task_queue):
            # print(task.execution_time/ task.period)
            self.utilization_queue[i] = task.execution_time/ task.period
        self.utilization = np.sum(self.utilization_queue)
        # print(self.utilization_queue)
        # print(np.sum(self.utilization_queue))
        

    def Schedulablity_RMA(self) -> bool:
        """
        Calculates the utilization factor of the tasks to be scheduled
        and then checks for the schedulablity and then returns true is
        schedulable else false.
        """
        self.task_queue.priority_sort_by_period()
        self.update_utilization()

        if self.utilization <= 1:
            if self.RMA_boundary_check():
                return True
            else:
                if self.RTA():
                    return True

        return False

    def RMA_boundary_check(self) -> bool:
        """[check whether the tasks are RMA schadulable by RMA boundary]

        Returns:
            bool: [True or False]
        """
        print("1step")
        RMA_boundary = self.num_of_task * (2 ** (1 / self.num_of_task) - 1)
        print(self.utilization, RMA_boundary)
        if self.utilization <= RMA_boundary:
            return True

        return False

    def RTA(self) -> bool:
        """[summary]

        Returns:
            bool: [description]
        """
        print("2step")
        for i in range(self.num_of_task):
            a1 = a0 = 0
            for j in range(i + 1):
                a1 += self.task_queue.task_queue[j].execution_time
            while(a1 != a0):
                a0 = a1
                a1 = self.task_queue.task_queue[i].execution_time
                for j in range(i):
                    a1 += math.ceil(a0/self.task_queue.task_queue[j].period) * self.task_queue.task_queue[j].execution_time

                # print(a0, a1)
            if (a1 > self.task_queue.task_queue[i].deadline):
                self.schedulablity[i] = 0
                # print(a1)
                # print("->0 ")
            else:
                self.schedulablity[i] = 1
                # print(a1)
                # print("->1 ")
        
        if (np.sum(self.schedulablity) == self.num_of_task):
            return True
        return False 

    def RMA_schedule(self):
        # for task in self.task_queue.task_queue:
        #     self.job_queue.append_task(task)
        # self.job_queue.check_overhead(utils.Overhead_Generator)
        self.job_queue.load_taskq(self.task_queue)


class scheduler:
    """[Scheduler, implementation of Rate Monotonic Scheduling here for the GPU to ]
    """
    def __init__(self, task_queue: tq, RMA=True) -> None:
        self.task_queue = task_queue


if __name__ == '__main__':
    # task1 = task(name = "task1", p=2.0, et=0.5, ddl=2.0)
    # task2 = task(name = "task2", p=3.0, et=0.5, ddl=3.0)
    # task3 = task(name = "task3", p=6.0, et=3.0, ddl=6.0)
    task1 = task(name = "task1", p=3.0, et=1.0, ddl=3.0)
    task2 = task(name = "task2", p=4.0, et=1.0, ddl=4.0)
    task3 = task(name = "task3", p=6.0, et=2.1, ddl=6.0)
    # task1 = task(name = "task1", p=3.0, et=0.5, ddl=3.0)
    # task2 = task(name = "task2", p=4.0, et=1.0, ddl=4.0)
    # task3 = task(name = "task3", p=6.0, et=2.0, ddl=6.0)
    # print(task1)
    task_q1 = tq()
    task_q1.append_task(task1)
    task_q1.append_task(task2)
    task_q1.append_task(task3)
    task_q1.show_task_queue_info()
    task_q1.priority_sort_by_period()
    task_q1.show_task_queue_info()
    rma = RMA(task_q1)
    print(rma.Schedulablity_RMA())
    print(rma.schedulablity)
    print(rma.lcm_time)
    rma.RMA_schedule()
    gantt_charts.gantt_chart_generate(rma.job_queue, task_q1)
