import copy
import random

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


# 机器均匀交叉
def mac_cross(job_num, Ma_1, Tm_1, Ma_2, Tm_2, cross):
    Mc1, Mc2, Tc1, Tc2 = [], [], [], []
    for i in range(job_num):
        Mc1.append([]), Mc2.append([]), Tc1.append([]), Tc2.append([])

        # 这里差一个完全随机

        for j in range(len(cross[i])):
            if cross[i][j] == 0:
                Mc1[i].append(Ma_1[i][j])
                Mc2[i].append(Ma_2[i][j])
                Tc1[i].append(Tm_1[i][j])
                Tc2[i].append(Tm_2[i][j])
            else:
                Mc1[i].append(Ma_2[i][j])
                Mc2[i].append(Ma_1[i][j])
                Tc1[i].append(Tm_2[i][j])
                Tc2[i].append(Tm_1[i][j])
    return Mc1, Mc2, Tc1, Tc2


def machine_cross(job_num, S_job, S_machine, S_time):
    for i in range(0, config.popsize, 2):
        if np.random.random() < config.cross_prob:
            job, machine, machine_time = S_job[i:i + 1], S_machine[i:i + 1], S_time[i:i + 1]
            Ma_1, Tm_1, across = to_MT(job_num, job, machine, machine_time)
            job1, machine1, machine_time1 = S_job[i + 1:i + 2], S_machine[i + 1:i + 2], S_time[i + 1:i + 2]
            Ma_2, Tm_2, across = to_MT(job_num, job1, machine1, machine_time1)
            Mc1, Mc2, Tc1, Tc2 = mac_cross(job_num, Ma_1, Tm_1, Ma_2, Tm_2, across)
            # 第一个机器编码
            machine_new1, time_new1 = back_MT(job_num, job, Mc1, Tc1)
            S_machine[i] = machine_new1[0]
            S_time[i] = time_new1[0]

            # 第二个机器编码
            machine_new2, time_new2 = back_MT(job_num, job1, Mc2, Tc2)
            S_machine[i + 1] = machine_new2[0]
            S_time[i + 1] = time_new2[0]


def pox(job_num, S_job, S_machine, S_time):
    for j in range(0, config.popsize, 2):
        if np.random.random() < config.cross_prob:
            job_1 = S_job[j:j+1]
            job_2 = S_job[j+1:j+2]

            p1 = copy.deepcopy(job_1)
            p2 = copy.deepcopy(job_2)
            p1 =  p1[0].tolist()
            p1 = list(map(int, p1))
            p2 = list(map(int,p2[0].tolist()))
            child_1, child_2 = [-1] * len(p1), [-1] * len(p2)
            # 建立工件集合
            job_set = [_ for _ in range(job_num)]
            j_set1 = np.random.choice(job_set, int(job_num / 2), replace=False)
            j_set2 = [0] * (job_num - len(j_set1))
            k = 0
            for i in range(job_num):
                if i not in j_set1:
                    j_set2[k] = i
                    k += 1
            j_set2 = np.array(j_set2)
            for i in range(len(j_set1)):
                index_j1_of_p1 = np.where(p1 == j_set1[i])[0]
                index_j1_of_p2 = np.where(p2 == j_set1[i])[0]

                for l in range(np.size(index_j1_of_p1)):
                    a1 = index_j1_of_p1[l]
                    a2 = index_j1_of_p2[l]
                    child_1[a1] = int(p1[a1])
                    child_2[a2] = int(p2[a2])
            k1, j_1 = 0, 0
            k2, j_2 = 0, 0
            j_set1 = j_set1.tolist()
            j_set2 = j_set2.tolist()
            while k1 < len(p1):
                if p1[k1] not in j_set2:
                    k1 += 1
                else:
                    if child_2[j_1] == -1:
                        child_2[j_1] = int(p1[k1])
                        j_1 += 1
                        k1 += 1
                    else:
                        j_1 += 1
            while k2 < len(p2):
                if p2[k2] not in j_set2:
                    k2 += 1
                else:
                    if child_1[j_2] == -1:
                        child_1[j_2] = int(p2[k2])
                        j_2 += 1
                        k2 += 1
                    else:
                        j_2 += 1
            child_1 = np.array(child_1).reshape(1, job_1.shape[1])
            child_2 = np.array(child_2).reshape(1, job_2.shape[1])

            ma1, mt1 = S_machine[j:j + 1], S_time[j:j + 1]
            ma11, mt11, wrc = to_MT(job_num, job_1, ma1, mt1)
            ma1_new, mt1_new = back_MT(job_num, child_1, ma11, mt11)
            ma2, mt2 = S_machine[j + 1:j + 2], S_time[j + 1:j + 2]
            ma22, mt22, wrc = to_MT(job_num, job_2, ma2, mt2)
            ma2_new, mt2_new = back_MT(job_num, child_2, ma22, mt22)
            S_job[j] = child_1[0]
            S_machine[j], S_time[j] = ma1_new[0], mt1_new[0]
            S_job[j + 1] = child_2[0]
            S_machine[j + 1], S_time[j + 1] = ma2_new[0], mt2_new[0]

# 工件工序交叉
# def pox(job_num, S_job, S_machine, S_time):
#     for j in range(0, config.popsize, 2):
#         if np.random.random() < config.cross_prob:
#             p1 = S_job[j:j + 1]
#             p2 = S_job[j + 1:j + 2]  # 两条父染色体
#             seq = random.sample(range(0, job_num), int(job_num / 2))
#             set1 = set(seq)  # 得到需要交叉的工件的集合
#             child1 = copy.deepcopy(p1)
#             child2 = copy.deepcopy(p2)
#             remain1 = [i for i in range(len(p1[0])) if p1[0, i] in set1]
#             remain2 = [i for i in range(len(p1[0])) if p2[0, i] in set1]
#             cursor1, cursor2 = 0, 0
#             for i in range(len(p1[0])):
#                 if p2[0, i] in set1:
#                     child1[0, remain1[cursor1]] = p2[0, i]
#                     cursor1 += 1
#                 if p1[0, i] in set1:
#                     child2[0, remain2[cursor2]] = p1[0, i]
#                     cursor2 += 1
#             ma1, mt1 = S_machine[j:j + 1], S_time[j:j + 1]
#             ma11, mt11, wrc = to_MT(job_num, p1, ma1, mt1)
#             ma1_new, mt1_new = back_MT(job_num, child1, ma11, mt11)
#             ma2, mt2 = S_machine[j + 1:j + 2], S_time[j + 1:j + 2]
#             ma22, mt22, wrc = to_MT(job_num, p2, ma2, mt2)
#             ma2_new, mt2_new = back_MT(job_num, child2, ma22, mt22)
#             S_job[j] = child1[0]
#             S_machine[j], S_time[j] = ma1_new[0], mt1_new[0]
#             S_job[j + 1] = child2[0]
#             S_machine[j + 1], S_time[j + 1] = ma2_new[0], mt2_new[0]
