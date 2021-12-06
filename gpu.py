import numpy as np
from scheduler import RMA
from task import task, task_queue as tq



class gpu:
    def __init__(self, name) -> None:
        self.name = name
        self.scheduler = RMA()
    
    def add_task(self, tk: tq):
        self.show_name()
        self.scheduler.add_task(tk)
        return self.scheduler.Schedulablity_RMA()

    # def deploy_task_queue(self):
    #     self.show_name()
    #     self.scheduler.RMA_schedule()
    
    def check_utilization(self):
        self.show_name()
        return self.scheduler.utilization

    def show_name(self):
        print(self.name)

    def show_info(self):
        self.show_name()
        self.scheduler.show_info()
    
    def show_info_short(self):
        print(self.name, self.scheduler.utilization)

    
