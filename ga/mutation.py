import numpy as np

import config


# 把加工时间编码和加工机器编码转化为对应列表
def to_MT(job_num, job, machine, machine_time):
    ma_, maT_, cross_ = [], [], []
    # 添加工件个数的空列表

    for i in range(job_num):
        ma_.append([]), maT_.append([]), cross_.append([])
    for i in range(job.shape[1]):
        sig = int(job[0, i])
        ma_[sig].append(machine[0, i])
        maT_[sig].append(machine_time[0, i])  # 记录每个工件的加工机器和时间
        index = np.random.randint(0, 2, 1)[0]
        cross_[sig].append(index)  # 随机生成一个0或1的列表，用于后续的机器的均匀交叉
    return ma_, maT_, cross_


# 列表返回根据新的工序，返回新的加工机器编码和加工时间编码
def back_MT(job_num, job, machine, machineTime):
    memory = np.zeros((1, job_num), dtype=int)
    m1, t1 = np.zeros((1, job.shape[1])), np.zeros((1, job.shape[1]))
    for i in range(job.shape[1]):
        sig = int(job[0, i])
        m1[0, i] = machine[sig][memory[0, sig]]
        t1[0, i] = machineTime[sig][memory[0, sig]]
        memory[0, sig] += 1
    return m1, t1


# # 随机选择每个个体的每个工件的一个可变异位置
# def mutation(job_num, S_job, S_machine, S_time, parm_data):
#     T_machine, T_machineTime, process_mac_num, work, tom = parm_data[0], parm_data[1], \
#         parm_data[2], parm_data[3], parm_data[4]
#
#     for i in range(0, config.popsize):
#         if np.random.random() < config.mutation_prob:
#             job = S_job[i].reshape(1, len(S_job[i]))
#             ma = S_machine[i].reshape(1, len(S_machine[i]))
#             mt = S_time[i].reshape(1, len(S_time[i]))
#             Ma, Mt, wcr = to_MT(job_num, job, ma, mt)
#             for j in range(job_num):
#                 r = np.random.randint(0, len(Ma[j]))  # 随机选择变异位置
#                 index_machine = process_mac_num[j][r]  # 得到该工件加工到第几个工序可以使用的机器数
#                 index_tom = tom[j][r]  # 该工件累计工序数
#                 high = index_tom
#                 low = index_tom - index_machine
#                 _time = T_machineTime[j, low:high]
#                 _machine = T_machine[j, low:high]
#                 Mt[j][r] = min(_time)
#                 ind = np.argwhere(_time == Mt[j][r])
#                 Ma[j][r] = _machine[ind[0, 0]]
#             ma_new, mt_new = back_MT(job_num, job, Ma, Mt)
#             S_machine[i] = ma_new[0]
#             S_time[i] = mt_new[0]


# 随机选择一个个体任意工件的多个可变异位置
def mutation(job_num, S_job, S_machine, S_time, parm_data):
    T_machine, T_machineTime, process_mac_num, work, tom = parm_data[0], parm_data[1], \
        parm_data[2], parm_data[3], parm_data[4]

    for i in range(0, config.popsize):
        if np.random.random() < config.mutation_prob:
            job = S_job[i].reshape(1, len(S_job[i]))
            ma = S_machine[i].reshape(1, len(S_machine[i]))
            mt = S_time[i].reshape(1, len(S_time[i]))
            Ma, Mt, wcr = to_MT(job_num, job, ma, mt)
            # r = np.random.randint(0, job_num)  # 随机选择变异工件
            # 然后随机选择变异的工序位置数
            # n = np.random.randint(0, len(Ma[r]))  # 随机选择工件工序变异数量
            for j in range(job_num):
                n = np.random.randint(0, len(Ma[j]))  # 随机选择工件工序变异数量
                for k in range(n):
                    pos = np.random.randint(0, len(Ma[j]))  # 随机选择变异位置
                    index_machine = process_mac_num[j][pos]  # 得到该工件加工到第几个工序可以使用的机器数
                    index_tom = tom[j][pos]  # 该工件累计工序数
                    high = index_tom
                    low = index_tom - index_machine
                    _time = T_machineTime[j, low:high]
                    _machine = T_machine[j, low:high]
                    Mt[j][pos] = min(_time)
                    ind = np.argwhere(_time == Mt[j][pos])
                    Ma[j][pos] = _machine[ind[0, 0]]
            ma_new, mt_new = back_MT(job_num, job, Ma, Mt)
            S_machine[i] = ma_new[0]
            S_time[i] = mt_new[0]
