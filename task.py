from _typeshed import Self
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

    

