import copy
import random

import numpy as np

import config
import preprocessing
from FJSP import FJSP
from pylab import mpl

from ga.crossover import pox, machine_cross
from ga.initialpop import initial
from ga.mutation import mutation
from ga.tournament import tournament
from rbf.RBF import RBFNet, Model_Selection, rbf_predict
from rbf.index_bootstraps import index_bootstrap

mpl.rcParams['font.sans-serif'] = ['SimHei']


class Ga:
    def __init__(self, param_fjsp, generation, Popsicle, cross_prob, param_data, mutation_prob):
        self.job_num = param_fjsp[0]  # 工件数
        self.machine_num = param_fjsp[1]  # 机器数
        self.generation = generation  # 迭代次数
        self.Popsicle = Popsicle  # 粒子个数
        self.cross_prob = cross_prob  # 交叉概率
        self.mutation_prob = mutation_prob  # 变异概率
        self.param_data = param_data
        self.work = param_data[3]

    # 遗传算法
    def ga_total(self, index):
        flag = True
        global obj_fjsp
        cs = preprocessing.CandidateSolution(self.job_num, self.machine_num, self.param_data)
        best_index = 0
        work = self.work  # 初始工序集合
        obj_fjsp = FJSP(self.job_num, self.machine_num)
        # 适应度值
        answer, result = [], []
        work_job, work_machine, work_time = np.zeros((self.Popsicle, len(work))), np.zeros(
            (self.Popsicle, len(work))), np.zeros((self.Popsicle, len(work)))
        center_locals, weight_locals, bias_locals, spread_locals, = [], [], [], []
        for gen in range(self.generation):
            if gen < 1:
                for i in range(self.Popsicle):
                    job, machine, machineTime = initial(self.job_num, self.machine_num, self.param_data)
                    job = np.array(job).reshape(1, len(work))
                    machine = np.array(machine).reshape(1, len(work))
                    machineTime = np.array(machineTime).reshape(1, len(work))
                    C_finish, _, _, _, _ = obj_fjsp.calculate(job, machine, machineTime)
                    answer.append(C_finish)
                    work_job[i], work_machine[i], work_time[i] = job[0], machine[0], machineTime[0]

                print('第{}个种群初始的最小最大完工时间:'.format(index), (min(answer)))

            # if gen > int(self.generation/2):
            if gen > 1:
                # if gen > 0:
                p_job, p_machine, p_time = np.zeros((self.Popsicle, len(work))), np.zeros(
                    (self.Popsicle, len(work))), np.zeros((self.Popsicle, len(work)))
                p_answer = []
                # 引入候选解预处理
                for i in range(self.Popsicle):
                    if i < int(self.Popsicle * 0.6):
                        job, machine, machine_time, initial_a = cs.GS_creat_jobs()
                        C_finish, _, _, _, _ = obj_fjsp.calculate(job, machine, machine_time)
                        p_answer.append(C_finish)
                        p_job[i], p_machine[i], p_time[i] = job[0], machine[0], machine_time[0]

                    elif i < int(self.Popsicle * 0.9):
                        job, machine, machine_time, initial_a = cs.LS_creat_jobs()
                        C_finish, _, _, _, _ = obj_fjsp.calculate(job, machine, machine_time)
                        p_answer.append(C_finish)
                        p_job[i], p_machine[i], p_time[i] = job[0], machine[0], machine_time[0]

                    else:
                        job, machine, machine_time, initial_a = cs.RS_creat_jobs()
                        C_finish, _, _, _, _ = obj_fjsp.calculate(job, machine, machine_time)
                        p_answer.append(C_finish)
                        p_job[i], p_machine[i], p_time[i] = job[0], machine[0], machine_time[0]
                for i in range(self.Popsicle):
                    if answer[i] > p_answer[i]:
                        work_job[i] = p_job[i]
                        work_machine[i] = p_machine[i]
                        work_time[i] = p_time[i]
                        answer[i] = p_answer[i]

            # # # construct rbf model
            # train_x = np.random.rand(self.Popsicle, work_job.shape[1] * 2)
            # for i in range(work_job.shape[0]):
            #     train_x[i][0:len(work_job[i])] = work_job[i]
            #     train_x[i][len(work_job[i]):2 * len(work_job[i])] = work_machine[i]
            # center_locals, weight_locals, bias_locals, spread_locals, = [], [], [], []
            # train_y = np.array(answer).reshape(-1, 1)
            # for i in range(self.Popsicle):
            #     data_index = index_bootstrap(self.Popsicle, config.boot_prob)
            #     RBF = RBFNet(k=config.k)
            #     local_c, local_w, local_b, local_s = RBF.local_update(train_x[data_index], train_y[data_index])
            #     center_locals.append(local_c)
            #     weight_locals.append(local_w)
            #     bias_locals.append(local_b)
            #     spread_locals.append(local_s)
            # 锦标赛选择策略
            S_job, S_machine, S_time, S_answer, S_index = tournament(work, work_job, work_machine, work_time, answer)

            # 工件pox交叉
            pox(self.job_num, S_job, S_machine, S_time)

            # 机器均匀交叉操作
            machine_cross(self.job_num, S_job, S_machine, S_time)

            # 机器变异操作
            mutation(self.job_num, S_job, S_machine, S_time, self.param_data)

            # train_x = np.random.rand(S_job.shape[0], work_job.shape[1] * 2)
            # for i in range(S_job.shape[0]):
            #     train_x[i][0:len(S_job[i])] = S_job[i]
            #     train_x[i][len(S_job[i]):2 * len(S_job[i])] = S_machine[i]
            #     # train_x[i][2 * len(S_job[i]):] = S_time[i]
            #
            # be_ind = answer.index(min(answer))
            # best_pop = np.hstack((work_job[be_ind], work_machine[be_ind])).reshape(1, work_job.shape[1] * 2)
            # model_index = Model_Selection(center_locals, weight_locals, bias_locals, spread_locals, best_pop,
            #                               num_set=config.model_num)
            # tmp = np.zeros((S_job.shape[0], 1))
            #
            # _ = random.choice(model_index)
            # tmp[:, 0] = rbf_predict(center_locals[_], weight_locals[_], bias_locals[_], spread_locals[_],
            #                         train_x).flatten()
            # if abs(min(tmp[:, 0]) - min(answer)) <= config.threshold:
            #
            #     for j, tempm in enumerate(tmp[:, 0]):
            #         if tempm < answer[j]:
            #             work_job[j] = S_job[j]
            #             work_machine[j] = S_machine[j]
            #             work_time[j] = S_time[j]
            #             answer[j] = tempm
            # else:
            # 对选择、交叉和变异后得到的个体进行评估和比较
            if gen > 0:
                train_x = np.random.rand(S_job.shape[0], work_job.shape[1] * 3)
                for i in range(S_job.shape[0]):
                    train_x[i][0:len(S_job[i])] = S_job[i]
                    train_x[i][len(S_job[i]):2 * len(S_job[i])] = S_machine[i]
                    train_x[i][2 * len(S_job[i]):] = S_time[i]

                be_ind = answer.index(min(answer))
                best_pop = np.random.rand(1, work_job.shape[1] * 3)
                for l in range(3):
                    best_pop[0][0:len(S_job[l])] = S_job[be_ind]
                    best_pop[0][len(S_job[l]):2 * len(S_job[l])] = S_machine[be_ind]
                    best_pop[0][2 * len(S_job[l]):] = S_time[be_ind]
                # best_pop = np.hstack((work_job[be_ind], work_machine[be_ind]),work_time[be_ind]).reshape(1, work_job.shape[1] * 3)
                model_index = Model_Selection(center_locals, weight_locals, bias_locals, spread_locals, best_pop,
                                              num_set=config.model_num)
                tmp = np.zeros((S_job.shape[0], 1))

                _ = random.choice(model_index)
                tmp[:, 0] = rbf_predict(center_locals[_], weight_locals[_], bias_locals[_], spread_locals[_],
                                        train_x).flatten()
                # 随机性
                indi = random.randint(0, config.popsize - 1)
                if abs(tmp[:, 0][indi] - answer[indi]) <= config.threshold:
                    flag = False
                if not flag:
                    for j, temp in enumerate(tmp[:, 0]):
                        if temp < answer[j]:
                            work_job[j] = S_job[j]
                            work_machine[j] = S_machine[j]
                            work_time[j] = S_time[j]
                            answer[j] = temp
            if flag:
                for k, pos in enumerate(S_index):
                    C_finish, _, _, _, _ = obj_fjsp.calculate(S_job[k].reshape(1, S_job.shape[1]),
                                                              S_machine[k].reshape(1, S_job.shape[1]),
                                                              S_time[k].reshape(1, S_job.shape[1]))
                    if C_finish < S_answer[k]:
                        work_job[k] = S_job[k]
                        work_machine[k] = S_machine[k]
                        work_time[k] = S_time[k]
                        answer[k] = C_finish

                # construct rbf model
                train_x = np.random.rand(self.Popsicle, work_job.shape[1] * 3)
                for i in range(work_job.shape[0]):
                    train_x[i][0:len(work_job[i])] = work_job[i]
                    train_x[i][len(work_job[i]):2 * len(work_job[i])] = work_machine[i]
                    train_x[i][2 * len(S_job[i]):] = work_time[i]
                train_y = np.array(answer).reshape(-1, 1)
                for i in range(self.Popsicle):
                    data_index = index_bootstrap(self.Popsicle, config.boot_prob)
                    RBF = RBFNet(k=config.k)
                    local_c, local_w, local_b, local_s = RBF.local_update(train_x[data_index],
                                                                          train_y[data_index])
                    center_locals.append(local_c)
                    weight_locals.append(local_w)
                    bias_locals.append(local_b)
                    spread_locals.append(local_s)

            best_index = answer.index(min(answer))
            result.append(answer[best_index])

        return work_job[best_index], work_machine[best_index], work_time[best_index], answer,flag
