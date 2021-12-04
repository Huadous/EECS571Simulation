import numpy as np

# hello world

class task:
    def __init__(self, name = "", rt = 0, p = 0, et = 0, ddl = 0, periodic = True) -> None:
        """[initialization for task]

        Args:
            name (string, optinal): [name of the task]. Defaults to "".
            rt (int, optional): [release time]. Defaults to 0.
            p (int, optional): [period]. Defaults to 0.
            et (int, optional): [execution time]. Defaults to 0.
            ddl (int, optional): [deadline]. Defaults to 0.
            periodic (bool, optional): [periodic]. Defaults to True.
        """
        self.name = name
        self.release_time = rt
        self.period = p
        self.execution_time = et
        self.deadline = ddl
        self.periodic = periodic
        self.priority = 0
        

    def redefine(self, name = "", rt = -1, p = -1, et = -1, ddl = -1, periodic = -1) -> None:
        """[redefine the details for the tasks]

        Args:
            name (string, optinal): [name of the task]. Defaults to "".
            rt (int, optional): [release time]. Defaults to -1.
            p (int, optional): [period]. Defaults to -1.
            et (int, optional): [execution time]. Defaults to -1.
            ddl (int, optional): [deadline]. Defaults to -1.
            periodic (int, optional): [periodic]. Defaults to -1.
        """
        if (name != ""):
            self.name = name
        if (rt != -1):
            self.release_time = rt
        if (p != -1):
            self.period = p
        if (et != -1):
            self.execution_time = et
        if (ddl != -1):
            self.deadline = ddl
        if (periodic != -1):
            self.periodic = periodic

    def show_task_info(self) -> str:
        """[show the task info]
        """
        return "'" + str(self.name) + "': {'release time': " + str(self.release_time) + ", 'period': " + str(self.period) + ", 'WCET': " + str(self.execution_time) + ", 'deadline': " + str(self.deadline) + ", 'priority': " + str(self.priority) + "}"

class task_queue:
    def __init__(self) -> None:
        """[initialize the task queue]
        """
        self.task_queue = []

    def append_task(self, i_task: task) -> None:
        """[append the task after the original task queue]

        Args:
            i_task (task): [the task]
        """
        self.task_queue.append(i_task)

    def load_task_queue(self, task_q: list) -> None:
        """[load an entire task queue directly]

        Args:
            task_q (list): [the task queue]
        """
        self.task_queue = task_q.copy()
    
    def size(self) -> int:
        """[return the size of the queue]

        Returns:
            int: [size]
        """
        return len(self.task_queue)

    def priority_sort_by_period(self) -> None:
        """[sort the task queue by period(RMA)]
        """
        self.task_queue.sort(key=lambda task: task.period)
        for i, task in enumerate(self.task_queue):
            task.priority = i

    def show_task_queue_info(self) -> None:
        """[show the task queue info]
        """
        print("task queue info:")
        for i in range(len(self.task_queue)):
            print("\t" + str(i + 1) + ". " + self.task_queue[i].show_task_info())
    
    def return_preiods(self) -> np.array:
        array_of_peridos = np.zeros(self.size())
        for i, task in enumerate(self.task_queue):
            array_of_peridos[i] = task.period
        return array_of_peridos

if __name__ == '__main__':
    task1 = task(name = "task1", p=2.0)
    task2 = task(name = "task2", p=3.0)
    task_q1 = task_queue()
    task_q1.append_task(task1)
    task_q1.append_task(task2)
    task_q1.show_task_queue_info()
    task_q1.priority_sort_by_period()
    task_q1.show_task_queue_info()
    

