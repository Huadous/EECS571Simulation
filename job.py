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
        self.status = 1

    def change_statue(self, status) -> None:
        self.status = status

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
        return "'" + str(self.name) + "': {'execute time intervals': " + str(self.execute_time_intervals) + ", 'status':" + str(self.status) + "}"


class job_queue:
    def __init__(self, lcm_time) -> None:
        """[initialize the job queue]
        """
        self.job_queue = []
        # self.periods = np.array([])
        self.lcm_time = lcm_time
        self.task_job_joint_map = {}
        self.num_of_task = 0

    def append_task(self, i_task: task) -> None:
        self.num_of_task += 1
        cur_t = 0
        index = 0
        while(cur_t < self.lcm_time):
            left_execution_time = i_task.execution_time
            # job_status = 1
            while(left_execution_time > 0):
                while(index < len(self.job_queue) and self.job_queue[index].execute_time_intervals[0] <= cur_t ):
                    index += 1
                print(index)
                while (index != 0 and index < len(self.job_queue) and self.job_queue[index - 1].execute_time_intervals[1] == self.job_queue[index].execute_time_intervals[0]):
                    index += 1
                print(index)
                execution_time_interval = np.zeros(2)
                job_tmp = job(i_task)
                if (index - 1 >= 0 and index < len(self.job_queue)):
                    print("option 1")
                    start_time = max(cur_t, self.job_queue[index - 1].execute_time_intervals[1])
                    time_interval = (self.job_queue[index].execute_time_intervals[0] - start_time)
                    if (left_execution_time > time_interval):
                        execution_time_interval[0] = start_time
                        if (start_time >= cur_t + i_task.deadline):
                            job_tmp.change_statue(0)
                            execution_time_interval[1] = self.job_queue[index].execute_time_intervals[0]
                        elif (cur_t + i_task.deadline < self.job_queue[index].execute_time_intervals[0]):
                            job_tmp.change_statue(0)
                            execution_time_interval[1] = cur_t + i_task.deadline
                        else:
                            execution_time_interval[1] = self.job_queue[index].execute_time_intervals[0]
                    else:
                        execution_time_interval[0] = start_time
                        if (start_time >= cur_t + i_task.deadline):
                            job_tmp.change_statue(0)
                            execution_time_interval[1] = start_time + left_execution_time
                        elif (cur_t + i_task.deadline < start_time + left_execution_time):
                            job_tmp.change_statue(0)
                            execution_time_interval[1] = cur_t + i_task.deadline
                        else:
                            execution_time_interval[1] = start_time + left_execution_time
                    left_execution_time -= time_interval
                elif (len(self.job_queue) == 0):
                    print("option 2")
                    execution_time_interval[0] = start_time = 0
                    if (start_time >= cur_t + i_task.deadline):
                        job_tmp.change_statue(0)
                        execution_time_interval[1] = left_execution_time
                    elif (cur_t + i_task.deadline < left_execution_time):
                        job_tmp.change_statue(0)
                        execution_time_interval[1] = cur_t + i_task.deadline
                    else:
                        execution_time_interval[1] = left_execution_time
                    left_execution_time = 0
                else:
                    print("option 3")
                    start_time = max(cur_t, self.job_queue[-1].execute_time_intervals[1])
                    execution_time_interval[0] = start_time
                    if (start_time >= cur_t + i_task.deadline):
                        job_tmp.change_statue(0)
                        execution_time_interval[1] = start_time + left_execution_time
                    elif (cur_t + i_task.deadline < start_time + left_execution_time):
                        job_tmp.change_statue(0)
                        execution_time_interval[1] = cur_t + i_task.deadline
                    else:
                        execution_time_interval[1] = start_time + left_execution_time
                    left_execution_time = 0
                    # if (left_execution_time > time_interval):
                    #     execution_time_interval = np.array([0, self.job_queue[index].execute_time_intervals[-1]])
                    # else:
                    #     execution_time_interval = np.array([self.job_queue[index - 1].execute_time_intervals[-1], self.job_queue[index - 1].execute_time_intervals[-1] + left_execution_time])
                
                job_tmp.set_execute_time_intervals(execution_time_interval)
                self.job_queue.insert(index, job_tmp)
                print("cur_t" + str(cur_t))
                print("lefttime" + str(left_execution_time))
                
                for job_implementation in self.job_queue:
                    print(job_implementation.show_job_info())
                
            cur_t += i_task.period
            
    def transform_gantt_charts_data(self) -> list:
        output = [[], [], [], []]
        num_of_status = 0
        for job_implementation in self.job_queue:
            if (job_implementation.status not in output[3]):
                num_of_status += 1
            output[0].append(job_implementation.name)
            output[1].append(job_implementation.execute_time_intervals[0])
            output[2].append(job_implementation.execute_time_intervals[1])
            output[3].append(job_implementation.status)
            
        print(output, num_of_status)
        
        return output, num_of_status

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