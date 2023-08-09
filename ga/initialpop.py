import copy
import random
import time

import numpy as np

import config


# 回溯算法,函数参数还要把job_index加进去,为每个工序选择加工机器
# global last_machine_path, last_machineTime_path
def backtracking(jobs, path_machine, path_time, job_index_2, last_machine_path, last_machineTime_path, param_data):
    T_machine, T_machine_time, process_num, work, tim = param_data[0], param_data[1], param_data[2], param_data[3], \
        param_data[4]
    if len(jobs) == 0:
        ma = copy.deepcopy(path_machine)
        mt = copy.deepcopy(path_time)
        last_machine_path.append(ma)
        last_machineTime_path.append(mt)
        return

    job = int(jobs[0])
    n_machine_number = process_num[job][job_index_2[job]]  # 该工序可选机器数
    machine_number_total = tim[job][job_index_2[job]]  # 该工序累计可选机器数
    high = machine_number_total
    low = high - n_machine_number
    _time = T_machine_time[job][low:high]
    _machine = T_machine[job][low:high]  # 加工时间和机器集列表
    job_index_2[job] += 1
    for i in range(len(_machine)):
        job_index_3 = copy.deepcopy(job_index_2)
        path_machine.append(_machine[i])
        path_time.append(_time[i])
        backtracking(jobs[1:], path_machine, path_time, job_index_3, last_machine_path, last_machineTime_path,param_data)
        del (path_machine[-1])
        del (path_time[-1])
    job_index_2[job] -= 1


def initial(job_num, machine_num, param_data):
    T_machine, T_machine_time, process_num, work, tim = param_data[0], param_data[1], param_data[2], param_data[3], \
        param_data[4]
    machine = []
    machineTime = []  # 最终的机器和加工时间集合
    machine_time = [0] * machine_num  # 记录当前每个机器上的最大完工时间
    # 得到新的工序集合
    initial_a = random.sample(range(4 * len(work)), len(work))
    index_jobs = np.array(initial_a).argsort()
    jobs = []
    for i in range(len(work)):
        jobs.append(work[index_jobs[i]])

    length = len(jobs)  # 新的工序集合长度
    rest = length % config.step  # 计算几个step完剩余的
    rest_number = length - rest  # step剩余的开始的place
    job_index = [0] * job_num  # 记录while循环内当前工件加工到第几到工序
    it = 0

    while it < rest_number:

        path_machine = []
        path_time = []  # 记录每次循环中路径的列表

        process = 1  # step1.计算当前step路径数
        job_index_1 = copy.deepcopy(job_index)  # 复制job_index 记录,记录工件到第几道工序了,为了得到四步工序的总路径数的记载变量,先得到之前已经加工过的工序记载量
        for job in jobs[it:it + config.step]:  # 该jobs里面包含了四个工序（顶点）(固定步数工序config.step）
            job = int(job)
            process *= process_num[job][job_index_1[job]]  # 得到当前四步的总路径数
            job_index_1[job] += 1  # 对应的
        # step2。创建每次step路径机器和加工时间列表
        last_machine_path = []
        last_machineTime_path = []
        job_index_2 = copy.deepcopy(job_index)

        job_1 = jobs[it:it + config.step]

        backtracking(job_1, path_machine, path_time, job_index_2, last_machine_path, last_machineTime_path,param_data)

        maxTime = float('inf')
        index = 0
        for i in range(process):
            machine_time_ = copy.deepcopy(machine_time)
            for k in range(len(last_machine_path[i])):
                machine_time_[int(last_machine_path[i][k]) - 1] += int(last_machineTime_path[i][k])
            if max(machine_time_) < maxTime:
                maxTime = max(machine_time_)
                index = i

        for i in range(len(last_machine_path[index])):
            machine.append(last_machine_path[index][i])
            machineTime.append(last_machineTime_path[index][i])
            machine_time[int(last_machine_path[index][i]) - 1] += last_machineTime_path[index][
                i]  # 最后计算目前选择的最佳路径的所选的机器集合情况下，每台机器的最大完工时间
        # 结束之后 jobs[0:4]中的每个工序job_index都要+1
        for job in jobs[it:it + config.step]:
            job_index[int(job)] += 1

        # it 开始step
        it += config.step

    # while循环结束后，jobs剩余小于step数量的工序，选择其可选加工机器
    last_machine_path_rest = []
    last_machineTime_path_rest = []
    path_machine = []
    path_time = []

    process_1 = 1  # 剩余工序组成的路径数
    job_index_4 = copy.deepcopy(job_index)  # 记录工件到第几道工序了,为了得到四步工序的总路径数的记载变量,先得到之前已经加工过的工序记载量
    for job in jobs[rest_number:]:  # 该jobs里面包含了四个工序（顶点）(固定步数工序config.step）
        job = int(job)
        process_1 *= process_num[job][job_index_4[job]]  # 得到当前四步的总路径数
        job_index_4[job] += 1  # 对应的

    job_index_3 = copy.deepcopy(job_index)
    backtracking(jobs[rest_number:], path_machine, path_time, job_index_3, last_machine_path_rest,
                 last_machineTime_path_rest,param_data)
    maxTime = float('inf')
    index = 0
    for i in range(process_1):
        machine_time_ = copy.deepcopy(machine_time)
        for k in range(len(last_machine_path_rest[i])):
            machine_time_[int(last_machine_path_rest[i][k]) - 1] += int(last_machineTime_path_rest[i][k])
        if max(machine_time_) < maxTime:
            maxTime = max(machine_time_)
            index = i

    for i in range(len(last_machine_path_rest[index])):
        machine.append(last_machine_path_rest[index][i])
        machineTime.append(last_machineTime_path_rest[index][i])
        machine_time[int(last_machine_path_rest[index][i]) - 1] += last_machineTime_path_rest[index][
            i]  # 最后计算目前选择的最佳路径的所选的机器集合情况下，每台机器的最大完工时间

    return jobs, machine, machineTime
