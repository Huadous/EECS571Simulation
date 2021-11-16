from task import task
from task import task_queue as tq
import utils
import numpy as np
import math

class job:
    """[summary]
    """
    def __init__(self, base_task: task) -> None:
        """[initialize the job]

        Job is one implementation for a task. A periodic task can be executed many times and each time of this tasks execution is called a job.

        Args:
            base_task (task): [the task that the job generated from]
        """
        self.name = base_task.name
        self.execute_time_intervals = np.array([])

    def get_name(self) -> str:
        """[get the name of the job]

        The name of the job is the same of the name of the base_task.

        Returns:
            str: [the name of the job]
        """
        return self.name

    def get_execute_time_intervals(self) -> np.array:
        """[get the specific intervals of the execute time]

        The job actually can be preempted by other higher priority tasks, which means job may not finish its job within one continuous time interval.
        Thus, we need to use array to contain the info. E.g. [[0.0, 1.0], [3.0, 4.0]], this means the job first starts at 0.0 and ends at 1.0 and may
        be preempted by other job. But it resumes at 3.0 and finishes its job at 4.0.

        Returns:
            np.array: [the specific intervals of the execute time]
        """
        return self.execute_time_intervals

    def set_name(self, name: str) -> None:
        """[set the name of the job]

        Args:
            name (str): [the name of the job]
        """
        self.name = name

    def set_execute_time_intervals(self, execute_time_intervals: np.array) -> None:
        """[set the specific intervals of the execute time]

        Args:
            execute_time_intervals (np.array): [the specific intervals of the execute time]
        """
        self.execute_time_intervals = np.copy(execute_time_intervals)

    def show_job_info(self) -> str:
        """[show the task info]
        """
        return "'" + str(self.name) + "': {'execute time intervals': " + str(self.execute_time_intervals) + "}"


class job_queue:
    def __init__(self) -> None:
        """[initialize the job queue]
        """
        self.job_queue = []
        self.task_job_joint_map = {}

    def append_job(self, i_job: job) -> None:
        """[append the job after the original job queue]

        Args:
            i_job (job): [the job]
        """
        self.job_queue.append(i_job)

    def load_job_queue(self, job_q: list) -> None:
        """[load an entire job queue directly]

        Args:
            job_q (list): [the job queue]
        """
        self.job_queue = job_q.copy()

    def sort(self) -> None:
        """[sort the job queue by period(RMA)]
        """
        self.job_queue.sort(key=lambda job: job.execute_time_intervals[0][0])

    def show_job_queue_info(self) -> None:
        """[show the job queue info]
        """
        print("job queue info:")
        for i in range(len(self.job_queue)):
            print("\t" + str(i + 1) + ". " + self.job_queue[i].show_job_info())



class RMA:
    """[summary]
    """
    def __init__(self, task_queue: tq) -> None:
        self.task_queue = task_queue
        self.num_of_task = task_queue.size()
        self.job_queue = job_queue()
        self.utilization_queue = np.zeros(self.num_of_task)
        self.utilization = 0
        self.schedulablity = np.zeros(self.num_of_task)

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
        lcm_time = utils.Lcm_of_array(self.task_queue.return_preiods())
        


class scheduler:
    """[Scheduler, implementation of Rate Monotonic Scheduling here for the GPU to ]
    """
    def __init__(self, task_queue: tq, RMA=True) -> None:
        self.task_queue = task_queue


if __name__ == '__main__':
    task1 = task(name = "task1", p=2.0, et=0.5, ddl=2.0)
    task2 = task(name = "task2", p=3.0, et=0.5, ddl=3.0)
    task3 = task(name = "task2", p=6.0, et=3.0, ddl=6.0)
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