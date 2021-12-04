from math import gamma, sqrt
from job import job, job_queue as jq
import enenrgy_consumption_manager as ecm
import numpy as np


vgc_limitation = [0.85, 1.05]
fgc_limitation = [0.85 , ecm.g1(vgc_limitation[1])]
fgm_limitation = [0.5, 1.2]

dvfs_type = {'init': 0, 'tl': 1, 'jl': 2}

class task_level_dvfs:
    optimal_alpha = -1
    def __init__(self) -> None:
        self.GPU_settings = [1,1,1]
        if (task_level_dvfs.optimal_alpha == -1):
            self.find_optimal_setting()
        self.optimalalpha = task_level_dvfs.optimal_alpha
    
    def find_optimal_setting(self):
        Vgc = np.linspace(vgc_limitation[0], vgc_limitation[1], 1000)
        opt_index = np.argmin(ecm.power_consumption(Vgc, ecm.g1(Vgc), fgm_limitation[0]))
        vgc_opt = Vgc[opt_index]
        fgc_opt = ecm.g1(vgc_opt)
        Fgm = np.linspace(fgm_limitation[0], fgm_limitation[1], 1000)
        opt_index = np.argmin(ecm.power_consumption(vgc_opt, fgc_opt, Fgm))
        fgm_opt = Fgm[opt_index]
        self.GPU_settings = [vgc_opt, fgc_opt, fgm_opt]
        task_level_dvfs.optimal_alpha = ecm.run_time(fgc_opt, fgm_opt) / ecm.run_time(1, 1)
        print(self.GPU_settings, task_level_dvfs.optimal_alpha, ecm.run_time(fgc_opt, fgm_opt), ecm.run_time(1, 1), ecm.power_consumption(vgc_opt, fgc_opt, fgm_opt) / ecm.power_consumption(1, 1, 1))

class job_level_dvfs:
    def __init__(self) -> None:
        self.GPU_settings = [1,1,1]
        self.optimalalpha = 1
        self.type = dvfs_type['init']

    def init_from_alpha(self, alpha):
        self.optimalalpha = alpha
        self.find_optimal_setting_based_on_time()
        self.type = dvfs_type['jl']
    
    def init_from_task_level_dvfs(self, tldvfs: task_level_dvfs):
        self.optimalalpha = tldvfs.optimalalpha
        self.GPU_settings = tldvfs.GPU_settings
        self.type = dvfs_type['tl']
    
    def find_optimal_setting_based_on_time(self):
        Vgc = np.linspace(vgc_limitation[0], vgc_limitation[1], 1000)
        Fgm = ecm.vgc_to_fgm_based_on_t(Vgc, self.optimalalpha)
        Fgm[Fgm < fgm_limitation[0]] = fgm_limitation[0]
        Fgm[Fgm > fgm_limitation[1]] = fgm_limitation[1]
        opt_index = np.argmin(ecm.power_consumption(Vgc, ecm.g1(Vgc), Fgm))
        vgc_opt = Vgc[opt_index]
        fgc_opt = ecm.g1(vgc_opt)
        fgm_opt = Fgm[opt_index]
        self.GPU_settings = [vgc_opt, fgc_opt, fgm_opt]
        print(self.GPU_settings, self.optimalalpha, ecm.run_time(fgc_opt, fgm_opt), ecm.run_time(1, 1), ecm.power_consumption(vgc_opt, fgc_opt, fgm_opt) / ecm.power_consumption(1, 1, 1))


if __name__ == '__main__':
    # print("hello world")
    # print(power_consumption(1,1,1))
    test = task_level_dvfs()
    # test.find_optimal_setting()

    test1 = task_level_dvfs()
    # res1 = test.find_optimal_setting()

    test2 = job_level_dvfs()
    test2.init_from_alpha(1.000)
