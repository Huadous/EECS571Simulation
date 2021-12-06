from math import gamma, sqrt
import enenrgy_consumption_utils as ecu
import numpy as np


vgc_limitation = [0.85, 1.05]
fgc_limitation = [0.85 , ecu.g1(vgc_limitation[1])]
fgm_limitation = [0.5, 1.1]

dvfs_type = {'normal': 0, 'tl': 1, 'jl': 2}

class task_level_dvfs:
    optimal_alpha = -1
    def __init__(self, D) -> None:
        self.GPU_settings = [1,1,1]
        self.D = D
        self.execution_time = 0
        self.execution_time_default = ecu.run_time(1, 1, self.D)
        self.P = 0
        self.Ej = 0
        self.P_default = ecu.average_power_consumption(1,1,1)
        # self.Ej_default = self.P_default / 1000 * self.execution_time_default / 3600000
        # if (task_level_dvfs.optimal_alpha == -1):
        self.find_optimal_setting()
        self.optimalalpha = task_level_dvfs.optimal_alpha
    
    def show_tld(self):
        return "{'GPUsettings': " + str(self.GPU_settings) + ", 'exec_normal': " + str(self.execution_time_default) + ", 'exec_save': " + str(self.execution_time) + ", 'P': " + str(self.P) + ", 'Ej': " + str(self.Ej) + "}"
    
    def find_optimal_setting(self):
        Vgc = np.linspace(vgc_limitation[0], vgc_limitation[1], 1000)
        opt_index = np.argmin(ecu.power_consumption(Vgc, ecu.g1(Vgc), fgm_limitation[0], self.D))
        vgc_opt = Vgc[opt_index]
        fgc_opt = ecu.g1(vgc_opt)
        Fgm = np.linspace(fgm_limitation[0], fgm_limitation[1], 1000)
        opt_index = np.argmin(ecu.power_consumption(vgc_opt, fgc_opt, Fgm, self.D))
        fgm_opt = Fgm[opt_index]
        self.GPU_settings = [vgc_opt, fgc_opt, fgm_opt]
        task_level_dvfs.optimal_alpha = ecu.run_time(fgc_opt, fgm_opt, self.D) / ecu.run_time(1, 1, self.D)
        self.execution_time = ecu.run_time(fgc_opt, fgm_opt, self.D)
        self.P = ecu.average_power_consumption(vgc_opt, fgc_opt, fgm_opt)
        # self.Ej = self.P / 1000 * self.execution_time / 3600000
        # print(self.GPU_settings, task_level_dvfs.optimal_alpha, ecu.run_time(fgc_opt, fgm_opt, self.D), ecu.run_time(1, 1, self.D), ecu.power_consumption(vgc_opt, fgc_opt, fgm_opt, self.D) / ecu.power_consumption(1, 1, 1, self.D))
        

class job_level_dvfs:
    def __init__(self, tld: task_level_dvfs) -> None:
        self.GPU_settings = tld.GPU_settings
        self.D = 0
        self.optimalalpha = tld.optimal_alpha
        self.type = dvfs_type['normal']
        self.execution_time = 0
        self.P = 0
        # self.Ej = 0
        self.P_save = tld.P
        self.P_default = tld.P_default

    # def change_from_alpha(self, time_interval):
    #     self.optimalalpha =  time_interval / ecu.run_time(1, 1, self.D)
        
    #     self.find_optimal_setting_based_on_time(time_interval)
    #     self.execution_time_default = ecu.run_time(1,1,self.D)
        
    #     self.type = dvfs_type['jl']
    
    def update(self, time_interval):
        if (self.type == dvfs_type['normal']):
            self.D = ecu.run_time_reverse(time_interval)
            self.P = self.P_default
        else:
            self.D = ecu.run_time_reverse_new(self.GPU_settings[1], self.GPU_settings[2], time_interval)
            self.P = self.P_save
        self.execution_time = time_interval
        # self.Ej = self.P / 1000 * self.execution_time / 3600000

    
    def find_optimal_setting_based_on_time(self, time_interval):
        execution_time_save = ecu.run_time(self.GPU_settings[1], self.GPU_settings[2], self.D)
        if (time_interval > execution_time_save):
            self.execution_time = execution_time_save
            self.P = self.P_save
            # self.Ej = self.P / 1000 * self.execution_time / 3600000
            return dvfs_type['tl']
        Vgc = np.linspace(vgc_limitation[0], vgc_limitation[1], 1000)
        Fgm = ecu.vgc_to_fgm_based_on_t(Vgc, time_interval, self.D)
        index_del = (Fgm > fgm_limitation[1]) + (Fgm < fgm_limitation[0])
        # print(Vgc)
        # print(ecu.g1(Vgc))
        # print(index_del)
        # print(Fgm)
        # print(Fgm.shape)
        Fgm = np.delete(Fgm, index_del, 0)
        Vgc = np.delete(Vgc, index_del, 0)
        # print(Fgm.shape)
        Fgm[Fgm > fgm_limitation[1]] = fgm_limitation[1]
        opt_index = np.argmin(ecu.power_consumption(Vgc, ecu.g1(Vgc), Fgm, self.D))
        vgc_opt = Vgc[opt_index]
        fgc_opt = ecu.g1(vgc_opt)
        fgm_opt = Fgm[opt_index]
        self.GPU_settings = [vgc_opt, fgc_opt, fgm_opt]
        self.execution_time = ecu.run_time(fgc_opt, fgm_opt, self.D)
        self.P = ecu.average_power_consumption(vgc_opt, fgc_opt, fgm_opt)
        return dvfs_type['jl']
        # self.Ej = self.P / 1000 * self.execution_time / 3600000
        # print(self.GPU_settings, self.optimalalpha, ecu.run_time(fgc_opt, fgm_opt, self.D), ecu.run_time(1, 1, self.D), ecu.power_consumption(vgc_opt, fgc_opt, fgm_opt, self.D) / ecu.power_consumption(1, 1, 1, self.D))


if __name__ == '__main__':
    # print("hello world")
    # print(power_consumption(1,1,1))
    test = task_level_dvfs(120)
    # test.find_optimal_setting()

    test1 = task_level_dvfs(130)
    # res1 = test.find_optimal_setting()

    test2 = job_level_dvfs(140)
    test2.change_from_alpha(ecu.run_time(1, 1, 140))
