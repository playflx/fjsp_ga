# 这是一个示例 Python 脚本。
import time

import numpy as np
from FJSP import FJSP
from ga.genetic import Ga
from utils import getFile
import config
import fileProcess
import warnings
warnings.filterwarnings("ignore")
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    t0 = time.time()
    log = open('log-rbf.txt', mode='a', encoding='utf-8')
    for i in range(1, 5):
        _, job_num, machine_num = getFile.read(i)
        obj_Process = fileProcess.FileProcess(job_num, machine_num)
        T_machine, T_machineTime, process_mac_num, jobs, tom = obj_Process.time_mac_job_pro(i)
        param_data = [T_machine, T_machineTime, process_mac_num, jobs, tom]

        gen = Ga([job_num, machine_num], config.generation, config.popsize, config.cross_prob, param_data,
                 config.mutation_prob)
        # 得到job,machine,machineTime
        a, b, c, d, e = gen.ga_total(i)
        job, machine, machine_time = np.array([a]), np.array([b]), np.array([c])
        # 创建fjsp对象，计算加工时间
        obj_fjsp = FJSP(job_num, machine_num)
        res, _, _, _, _ = obj_fjsp.calculate(job, machine, machine_time)
        print('MK0' + str(i) + '.fjs: ', res, file=log)
        print(res)
        print(d)
        print("flag:",e)
        # print(rbf_model,file=log)
        # print('该算例的工序集合：',job,file=log)
        # print('该算例的机器集合：',machine,file=log)
        # print('该算例的加工时间集合：', machine_time, file=log)
        obj_fjsp.draw(job, machine, machine_time, i)
    log.close()
    t1 = time.time()
    print(t1 - t0)
