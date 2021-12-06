import utils
from gpu import gpu




class CGpairs:
    num_of_gpu_default = 2
    def __init__(self, name) -> None:
        self.name = name
        self.switch = False
        self.gpu = [gpu("GPU " + str(i + 1)) for i in range(CGpairs.num_of_gpu_default)]

    def start_service(self, fig, hand_list, labl_list, cluster_num, type):
        for gpu in  self.gpu:
            gpu.scheduler.RMA_schedule()
            gpu.scheduler.show_gantt_chart(fig, hand_list, labl_list, cluster_num, utils.find_num(self.name), CGpairs.num_of_gpu_default, utils.find_num(gpu.name), type)

    def show_name(self):
        print(self.name)

    def show_info_short(self):
        self.show_name()
        print("switch: " + str(self.switch))
        for i in range(len(self.gpu)):
            self.gpu[i].show_info_short()

    def show_info(self):
        self.show_name()
        print("switch: " + str(self.switch))
        for i in range(len(self.gpu)):
            self.gpu[i].show_info()



