from task import task
from task import task_queue as tq
import utils
import numpy as np

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


class RMA:
    """[summary]
    """
    def __init__(self, task_queue: tq) -> None:
        self.task_queue = task_queue
        self.job_queue = []
        self.task_job_joint_map = {}
        self.utilization_queue = np.array([])
        self.utilization = 0
        self.num_of_task = len(task_queue)

    def update_utilization(self):
        for i in self.task_queue:
            np.hstack((self.utilization_queue, i.execution_time/ i.period))
        self.utilization = np.sum(self.utilization_queue)
        

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
        RMA_boundary = self.num_of_task * (2 ** (1 / self.num_of_task) - 1)
        if self.utilization <= RMA_boundary:
            return True

        return False

    def RTA(self) -> bool:
        """[summary]

        Returns:
            bool: [description]
        """
        pass


class scheduler:
    """[Scheduler, implementation of Rate Monotonic Scheduling here for the GPU to ]
    """
    def __init__(self, task_queue: tq, RMA=True) -> None:
        self.task_queue = task_queue


