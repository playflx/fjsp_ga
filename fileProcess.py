import numpy as np
from utils import getFile


class FileProcess:
    def __init__(self, job_num, machine_num):
        self.job_num = job_num
        self.machine_num = machine_num

        # 将每个工件的每道工序的可选机器和加工时间取出来

    def translate(self, line):
        machine, machine_time, process_select_num, process_index = [], [], [], []
        process_num = line[0]  # 每个工件的工序数
        line = line[1:len(line) + 1]
        index = 0
        # 得到每个工序可选机器数的数字的索引和每道工序可选机器数
        for i in range(process_num):
            sig = line[index]
            process_select_num.append(sig)
            process_index.append(index)
            index = index + 1 + 2 * sig
        # 删除可选工序数的位置
        for j in range(process_num):
            del line[process_index[j] - j]
        # 将机器数和加工时间分别加入两个数组中
        for k in range(0, len(line) - 1, 2):
            machine.append(line[k])
            machine_time.append(line[k + 1])
        return machine, machine_time, process_select_num

        # 获取10个工件中最大工序数

    def width_max(self, parameters):
        width = []
        for i in range(self.job_num):
            mac, _, sdx = self.translate(parameters[i])
            singed = len(mac)
            width.append(singed)
        width = max(width)
        return width

        # 将加工机器和加工时间对应放到两列表中

    def cau(self, parameters):
        width = self.width_max(parameters)
        C_machine, C_machineTime = np.zeros((self.job_num, width)), np.zeros((self.job_num, width))
        process_mac_num = []
        for i in range(self.job_num):
            mac, macTime, sdx = self.translate(parameters[i])
            process_mac_num.append(sdx)  # 添加每个工件的每道工序可选机器数
            sig = len(mac)
            C_machine[i, 0:sig] = mac
            C_machineTime[i, 0:sig] = macTime
        return C_machine, C_machineTime, process_mac_num

        # 得到加工时间，加工机器，工件工序集合，工序数，

    def time_mac_job_pro(self, index):
        parameters, _, _ = getFile.read(index)
        machine, machineTime, process_mac_num = self.cau(parameters)
        jobs, tom = [], []
        for i in range(self.job_num):
            tim = []
            for j in range(1, len(process_mac_num[i]) + 1):
                jobs.append(i)
                tim.append(sum(process_mac_num[i][0:j]))
            tom.append(tim)
        return machine, machineTime, process_mac_num, jobs, tom
