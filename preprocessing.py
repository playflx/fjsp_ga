import random

import numpy as np


# Candidate solution preprocessing
class CandidateSolution:

    def __init__(self, job_num, machine_num, parm_data):
        self.job_num = job_num
        self.machine_num = machine_num
        self.T_machine, self.T_machineTime, self.process_mac_num, self.work, self.tom = parm_data[0], parm_data[1], \
            parm_data[2], parm_data[3], parm_data[4]

    # 全局选择候选解
    def GS_creat_jobs(self):
        initial_a = random.sample(range(4 * len(self.work)), len(self.work))
        index_jobs = np.array(initial_a).argsort()
        jobs = []
        for i in range(len(self.work)):
            jobs.append(self.work[index_jobs[i]])
        jobs = np.array(jobs).reshape(1, len(self.work))

        n_machine = np.zeros((1, jobs.shape[1]))
        n_machinetime = np.zeros((1, jobs.shape[1]))
        index = [0] * self.job_num
        machine = [0] * self.machine_num  # 记录每个机器上的时间
        for idx, job in enumerate(jobs[0]):
            job = int(job)
            index_machine = self.process_mac_num[job][index[job]]  # 得到该工件加工到第几个工序可以使用的机器数
            index_tom = self.tom[job][index[job]]  # 该工件累计工序数
            high = index_tom
            low = index_tom - index_machine
            _time = self.T_machineTime[job, low:high]
            _machine = self.T_machine[job, low:high]
            index[job] += 1
            ma, ma_ind, mt = 0, 0, float('inf')
            _time = _time.tolist()
            _machine = _machine.tolist()
            for ind, mach in enumerate(_machine):
                if _time[ind] + machine[int(mach) - 1] < mt:
                    mt = _time[ind] + machine[int(mach) - 1]
                    ma = int(mach)
                    ma_ind = ind
            machine[ma - 1] += _time[ma_ind]
            n_machine[0, idx] = ma
            n_machinetime[0, idx] = _time[ma_ind]

        return jobs, n_machine, n_machinetime, initial_a

    # 局部选择候选解
    def LS_creat_jobs(self):
        initial_a = random.sample(range(4 * len(self.work)), len(self.work))
        index_jobs = np.array(initial_a).argsort()
        jobs = []
        for i in range(len(self.work)):
            jobs.append(self.work[index_jobs[i]])
        jobs = np.array(jobs).reshape(1, len(self.work))

        n_machine = np.zeros((1, jobs.shape[1]))
        n_machinetime = np.zeros((1, jobs.shape[1]))
        index = [0] * self.job_num

        for i in range(self.job_num):
            num = jobs[0].tolist().count(i)  # 找出该工件在工序集合中的工序数
            machine = [0] * self.machine_num
            job = i
            for j in range(0, num):
                num_index = np.where(i == jobs[0])  # 该工件所有工序的索引
                index_machine = self.process_mac_num[job][index[job]]  # 得到该工件加工到第几个工序可以使用的机器数
                index_tom = self.tom[job][index[job]]  # 该工件累计工序数
                high = index_tom
                low = index_tom - index_machine
                _time = self.T_machineTime[job, low:high]
                _machine = self.T_machine[job, low:high]
                index[job] += 1
                ma, ma_ind, mt = 0, 0, float('inf')
                _time = _time.tolist()
                _machine = _machine.tolist()
                for ind, mach in enumerate(_machine):
                    if _time[ind] + machine[int(mach) - 1] < mt:
                        mt = _time[ind] + machine[int(mach) - 1]
                        ma = int(mach)
                        ma_ind = ind
                machine[ma - 1] += _time[ma_ind]
                n_machine[0, num_index[0][j]] = ma
                n_machinetime[0, num_index[0][j]] = _time[ma_ind]
        return jobs, n_machine, n_machinetime, initial_a

    # 随机选择候选解
    def RS_creat_jobs(self):
        initial_a = random.sample(range(4 * len(self.work)), len(self.work))
        index_jobs = np.array(initial_a).argsort()
        jobs = []
        for i in range(len(self.work)):
            jobs.append(self.work[index_jobs[i]])
        jobs = np.array(jobs).reshape(1, len(self.work))

        n_machine = np.zeros((1, jobs.shape[1]))
        n_machinetime = np.zeros((1, jobs.shape[1]))
        index = [0] * self.job_num
        machine = [0] * self.machine_num
        for idx, job in enumerate(jobs[0]):
            job = int(job)
            index_machine = self.process_mac_num[job][index[job]]  # 得到该工件加工到第几个工序可以使用的机器数
            index_tom = self.tom[job][index[job]]  # 该工件累计工序数
            high = index_tom
            low = index_tom - index_machine
            _time = self.T_machineTime[job, low:high]
            _machine = self.T_machine[job, low:high]
            index[job] += 1
            index_time = np.random.randint(0, len(_time), 1)
            n_machine[0, idx] = _machine[index_time[0]]
            n_machinetime[0, idx] = _time[index_time[0]]

        return jobs, n_machine, n_machinetime, initial_a
