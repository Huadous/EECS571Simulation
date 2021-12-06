from re import S
from enenrgy_consumption_utils import power_consumption
from task import task as tk, task_queue
import utils
import numpy as np
import math
from dvfs import job_level_dvfs as jld
import dvfs

job_status = {'mis': 0, 'exec': 1, 'T_oh': 2,
              'P_oh': 3, 'tl_dvfs': 4, 'jl_dvfs': 5}


class job:
    """[summary]
    """

    def __init__(self, base_task: tk) -> None:
        """[initialize the job]

        Job is one implementation for a task. A periodic task can be executed many times and each time of this tasks execution is called a job.

        Args:
            base_task (task): [the task that the job generated from]
        """
        self.name = base_task.name
        self.execute_time_intervals = np.array([])
        self.status = job_status["exec"]
        self.priority = -1
        self.start = False
        self.end = False
        # self.dvfs = jld(base_task.D)
        self.dvfs = jld(base_task.dvfs)

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
        return "'" + str(self.name) + "': {'execute time intervals': " + str(self.execute_time_intervals) + ", 'status':" + str(self.status) + ", 'start':" + str(self.start) + ", 'end':" + str(self.end) + "}"


class job_queue:
    def __init__(self, lcm_time) -> None:
        """[initialize the job queue]
        """
        self.job_queue = []
        self.assign_manager = []
        # self.periods = np.array([])
        self.lcm_time = lcm_time
        self.task_job_joint_map = {}
        self.num_of_task = 0
        self.time_line = []

    def load_taskq(self, i_task_q: task_queue) -> None:
        flag = 1
        self.num_of_task = len(i_task_q.task_queue)
        # init the task assignment manager with the task queue
        for task in i_task_q.task_queue:
            self.assign_manager.append(
                {"task": task, "left_time": []})

        # generate the time line which events will happen
        self.time_line = utils.combine_list(
            [[i * task.period for i in range(int(self.lcm_time / task.period) + 1)] for task in i_task_q.task_queue])
        # print(self.time_line, int(self.lcm_time / task.period))

        # handle each time interval
        for i in range(1, len(self.time_line)):
            cur_time = self.time_line[i - 1]
            end_time = self.time_line[i]

            # check each task, whether needs to release new job
            for i in range(self.num_of_task):
                if (cur_time % i_task_q.task_queue[i].period == 0):
                    self.assign_manager[i]['left_time'].append(
                        [i_task_q.task_queue[i].execution_time, cur_time + i_task_q.task_queue[i].period])

            #
            for i in range(self.num_of_task):
                while (end_time - cur_time > 0 and len(self.assign_manager[i]['left_time']) > 0):
                    # print(end_time, cur_time)
                    # print(str(end_time - cur_time > 0),str(len(self.assign_manager[i]['left_time']) > 0),str(end_time - cur_time > 0 and len(self.assign_manager[i]['left_time']) > 0))
                    # if (len(self.assign_manager['left_time']) > 0):
                    for index, interval in enumerate(self.assign_manager[i]['left_time']):
                        job_tmp = job(self.assign_manager[i]['task'])
                        job_tmp.priority = self.assign_manager[i]['task'].priority
                        execution_time_interval = np.zeros(2)

                        if (self.assign_manager[i]['task'].execution_time == self.assign_manager[i]['task'].dvfs.execution_time):
                            job_tmp.status = job_status['tl_dvfs']
                            job_tmp.dvfs.type = dvfs.dvfs_type['tl']

                        # handle overhead
                        # if (flag == 1):
                        #     flag = 0
                        # else:
                        #     print(str(len(self.job_queue) > 0), str(self.job_queue[-1].priority > job_tmp.priority), str(self.job_queue[-1].end == False))

                        if (len(self.job_queue) > 0 and self.job_queue[-1].priority > job_tmp.priority and self.job_queue[-1].end == False):
                            # Transformation Overhead
                            T_overhead = utils.T_Overhead_Generator()
                            if (interval[0] <= T_overhead):
                                T_overhead = interval[0]
                            interval[0] -= T_overhead
                            # print("o->>>" + str(cur_overhead))
                            # if (end_time - cur_time <= T_overhead):
                            #     break
                            job_T_overhead = job(
                                tk(name=self.job_queue[-1].name))
                            job_T_overhead.priority = self.job_queue[-1].priority
                            job_T_overhead.set_execute_time_intervals(
                                np.array([cur_time, cur_time + T_overhead]))
                            job_T_overhead.change_statue(job_status['T_oh'])
                            self.job_queue.append(job_T_overhead)
                            cur_time += T_overhead

                            if (interval[0] > 0):
                                # Preemption Overhead
                                P_overhead = utils.P_Overhead_Generator()
                                # print("o->>>" + str(cur_overhead))
                                # if (end_time - cur_time <= P_overhead):
                                #     break
                                job_P_overhead = job(
                                    self.assign_manager[i]['task'])
                                job_P_overhead.priority = self.job_queue[-1].priority
                                job_P_overhead.set_execute_time_intervals(
                                    np.array([cur_time, cur_time + P_overhead]))
                                job_P_overhead.change_statue(job_status['P_oh'])
                                self.job_queue.append(job_P_overhead)
                                cur_time += P_overhead


                        left_time = end_time - cur_time

                        # handle miss ddl
                        if (cur_time >= interval[1]):
                            job_tmp.change_statue(job_status['mis'])

                        # mark job start
                        if (self.assign_manager[i]['task'].execution_time == interval[0]):
                            job_tmp.start = True

                        # task execution
                        if (interval[0] <= left_time):

                            execution_time_interval[0] = cur_time
                            execution_time_interval[1] = cur_time + interval[0]

                            job_tmp.end = True
                            cur_time += interval[0]
                            # print(self.assign_manager[i]['left_time'], index)
                            del self.assign_manager[i]['left_time'][index]

                        else:

                            execution_time_interval[0] = cur_time
                            execution_time_interval[1] = cur_time + left_time

                            cur_time += left_time
                            interval[0] -= left_time

                        if (len(self.job_queue) > 0 and job_tmp.name == self.job_queue[-1].name and execution_time_interval[0] == self.job_queue[-1].execute_time_intervals[1] and job_tmp.status == self.job_queue[-1].status):
                            self.job_queue[-1].execute_time_intervals[1] = execution_time_interval[1]
                            self.job_queue[-1].dvfs.update(self.job_queue[-1].execute_time_intervals[1] - self.job_queue[-1].execute_time_intervals[0])
                        else:
                            job_tmp.set_execute_time_intervals(
                                execution_time_interval)
                            job_tmp.dvfs.update(execution_time_interval[1] - execution_time_interval[0])
                            self.job_queue.append(job_tmp)

                        # print("-" * 40)
                        # for job_implementation in self.job_queue:
                        #     print(job_implementation.show_job_info())
                        # print("-" * 40)
                        # print("cur_time: " + str(cur_time))
                        # print("end_time: " + str(end_time))
                        # print("left_time: " + str(end_time - cur_time))
                        if (end_time - cur_time <= 0):
                            break

                if (end_time - cur_time <= 0):
                    break

    # def append_task(self, i_task: task) -> None:
    #     self.num_of_task += 1
    #     cur_t = 0
    #     index = 0
    #     while(cur_t < self.lcm_time):
    #         left_execution_time = i_task.execution_time
    #         job_seq = 1
    #         job_init_flag = True
    #         # job_status = 1
    #         while(left_execution_time > 0):
    #             while(index < len(self.job_queue) and self.job_queue[index].execute_time_intervals[0] <= cur_t):
    #                 index += 1
    #             print(index)
    #             while (index != 0 and index < len(self.job_queue) and self.job_queue[index - 1].execute_time_intervals[1] == self.job_queue[index].execute_time_intervals[0]):
    #                 index += 1
    #             print(index)
    #             execution_time_interval = np.zeros(2)
    #             job_tmp = job(i_task)
    #             if (index - 1 >= 0 and index < len(self.job_queue)):
    #                 print("option 1")
    #                 start_time = max(
    #                     cur_t, self.job_queue[index - 1].execute_time_intervals[1])
    #                 time_interval = (
    #                     self.job_queue[index].execute_time_intervals[0] - start_time)
    #                 if (left_execution_time > time_interval):
    #                     execution_time_interval[0] = start_time
    #                     if (start_time >= cur_t + i_task.deadline):
    #                         job_tmp.change_statue(job_status['mis'])
    #                         execution_time_interval[1] = self.job_queue[index].execute_time_intervals[0]
    #                     elif (cur_t + i_task.deadline < self.job_queue[index].execute_time_intervals[0]):
    #                         job_tmp.change_statue(job_status['mis'])
    #                         execution_time_interval[1] = cur_t + \
    #                             i_task.deadline
    #                     else:
    #                         execution_time_interval[1] = self.job_queue[index].execute_time_intervals[0]
    #                 else:
    #                     execution_time_interval[0] = start_time
    #                     if (start_time >= cur_t + i_task.deadline):
    #                         job_tmp.change_statue(job_status['mis'])
    #                         execution_time_interval[1] = start_time + \
    #                             left_execution_time
    #                     elif (cur_t + i_task.deadline < start_time + left_execution_time):
    #                         job_tmp.change_statue(job_status['mis'])
    #                         execution_time_interval[1] = cur_t + \
    #                             i_task.deadline
    #                     else:
    #                         execution_time_interval[1] = start_time + \
    #                             left_execution_time
    #                 left_execution_time -= time_interval
    #             elif (len(self.job_queue) == 0):
    #                 print("option 2")
    #                 execution_time_interval[0] = start_time = 0
    #                 if (start_time >= cur_t + i_task.deadline):
    #                     job_tmp.change_statue(job_status['mis'])
    #                     execution_time_interval[1] = left_execution_time
    #                 elif (cur_t + i_task.deadline < left_execution_time):
    #                     job_tmp.change_statue(job_status['mis'])
    #                     execution_time_interval[1] = cur_t + i_task.deadline
    #                 else:
    #                     execution_time_interval[1] = left_execution_time
    #                 left_execution_time = 0
    #             else:
    #                 print("option 3")
    #                 start_time = max(
    #                     cur_t, self.job_queue[-1].execute_time_intervals[1])
    #                 execution_time_interval[0] = start_time
    #                 if (start_time >= cur_t + i_task.deadline):
    #                     job_tmp.change_statue(job_status['mis'])
    #                     execution_time_interval[1] = start_time + \
    #                         left_execution_time
    #                 elif (cur_t + i_task.deadline < start_time + left_execution_time):
    #                     job_tmp.change_statue(job_status['mis'])
    #                     execution_time_interval[1] = cur_t + i_task.deadline
    #                 else:
    #                     execution_time_interval[1] = start_time + \
    #                         left_execution_time
    #                 left_execution_time = 0

    #             job_tmp.set_execute_time_intervals(execution_time_interval)
    #             if (job_init_flag):
    #                 job_tmp.start = True
    #                 job_init_flag = False
    #             if (left_execution_time <= 0):
    #                 job_seq = -1
    #                 job_tmp.end = True
    #             job_tmp.seq = job_seq
    #             job_tmp.priority = i_task.priority
    #             self.job_queue.insert(index, job_tmp)
    #             print("cur_t" + str(cur_t))
    #             print("lefttime" + str(left_execution_time))

    #             for job_implementation in self.job_queue:
    #                 print(job_implementation.show_job_info())

    #         cur_t += i_task.period

    # def check_overhead(self, func):
    #     overload_base = 0
    #     index = 1
    #     for i in range(1, len(self.job_queue)):
    #         if (self.job_queue[index].priority < self.job_queue[index-1].priority and self.job_queue[index-1].end == False):
    #             cur_overhead = func()
    #             print("o->>>" + str(cur_overhead))
    #             job_tmp = job(task(name=self.job_queue[index].name))
    #             job_tmp.set_execute_time_intervals(np.array(
    #                 [self.job_queue[index].execute_time_intervals[0] + overload_base, self.job_queue[index].execute_time_intervals[0] + overload_base + cur_overhead]))
    #             job_tmp.change_statue(job_status['oh'])
    #             self.job_queue.insert(index, job_tmp)
    #             index += 1
    #             overload_base += cur_overhead
    #         self.job_queue[index].execute_time_intervals += overload_base
    #         index += 1

    #     for job_implementation in self.job_queue:
    #         print(job_implementation.show_job_info())

    def check_energy(self):
        accumulated_time = 0
        watts_record = np.zeros(len(utils.energy_type))
        if (len(self.job_queue) == 0):
            return watts_record

        for i, job in enumerate(self.job_queue):
            if (self.job_queue[i].status == job_status['exec'] or self.job_queue[i].status == job_status['mis'] or self.job_queue[i].status == job_status['jl_dvfs'] or self.job_queue[i].status == job_status['tl_dvfs']):
                time_interval = (self.job_queue[i].execute_time_intervals[1] - self.job_queue[i].execute_time_intervals[0])
                accumulated_time += time_interval
                power_consumption = time_interval * self.job_queue[i].dvfs.P
                if (self.job_queue[i].status == job_status['exec'] or self.job_queue[i].status == job_status['mis']):
                    watts_record[utils.energy_type['normal']] += power_consumption
                elif (self.job_queue[i].status == job_status['jl_dvfs']):
                    watts_record[utils.energy_type['jld']] += power_consumption
                elif (self.job_queue[i].status == job_status['tl_dvfs']):
                    watts_record[utils.energy_type['tld']] += power_consumption
            elif (self.job_queue[i].status == job_status['T_oh']):
                time_interval = (self.job_queue[i].execute_time_intervals[1] - self.job_queue[i].execute_time_intervals[0])
                accumulated_time += time_interval
                power_consumption = time_interval * self.job_queue[i - 1].dvfs.P
                watts_record[utils.energy_type['normal']] += power_consumption
            elif (self.job_queue[i].status == job_status['P_oh']): 
                time_interval = (self.job_queue[i].execute_time_intervals[1] - self.job_queue[i].execute_time_intervals[0])
                accumulated_time += time_interval
                power_consumption = time_interval * 200
                watts_record[utils.energy_type['po']] += power_consumption

        watts_record[utils.energy_type['idle']] = (self.lcm_time - accumulated_time) * 85
        return watts_record / self.lcm_time

    def run_time_check(self):
        for i, job in enumerate(self.job_queue):
            if (i  < len(self.job_queue) - 1 and self.job_queue[i].status == job_status['exec'] and self.job_queue[i].dvfs.type != dvfs.dvfs_type["tl"] and self.job_queue[i].execute_time_intervals[1] < self.job_queue[i + 1].execute_time_intervals[0]):
                
                
                job.dvfs.find_optimal_setting_based_on_time(self.job_queue[i + 1].execute_time_intervals[0] - self.job_queue[i].execute_time_intervals[0])
                self.job_queue[i].execute_time_intervals[1] = self.job_queue[i].execute_time_intervals[0] + self.job_queue[i].dvfs.execution_time
                job.change_statue(job_status['jl_dvfs'])
            elif (i  == len(self.job_queue) - 1 and self.job_queue[i].status == job_status['exec'] and self.job_queue[i].dvfs.type != dvfs.dvfs_type["tl"] and self.job_queue[i].execute_time_intervals[1] < self.lcm_time):
                job.dvfs.find_optimal_setting_based_on_time(self.lcm_time - self.job_queue[i].execute_time_intervals[0])
                self.job_queue[i].execute_time_intervals[1] = self.job_queue[i].execute_time_intervals[0] + self.job_queue[i].dvfs.execution_time
                job.change_statue(job_status['jl_dvfs'])


                
    def transform_gantt_charts_data(self, type) -> list:
        if (type == utils.simulation_type['dvfs']):
            self.run_time_check()
        # self.check_energy()
        output = [[], [], [], [], [], []]
        num_of_status = 0
        for job_implementation in self.job_queue:
            if (job_implementation.status not in output[3]):
                num_of_status += 1
            output[0].append(job_implementation.name)
            output[1].append(job_implementation.execute_time_intervals[0])
            output[2].append(job_implementation.execute_time_intervals[1])
            output[3].append(job_implementation.status)
            output[4].append(job_implementation.start)
            output[5].append(job_implementation.end)

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
