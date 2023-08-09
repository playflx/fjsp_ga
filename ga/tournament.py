import random
import numpy as np

import config


def tournament(work, work_job, work_machine, work_time, answer):
    # 锦标赛选择策略
    S_job, S_machine, S_time = np.zeros((config.popsize, len(work))), np.zeros(
        (config.popsize, len(work))), np.zeros((config.popsize, len(work)))
    S_answer = [0] * int(config.popsize)
    S_index = [0] * int(config.popsize)
    index = 0
    for i in range(int(config.popsize)):
        select_index = random.sample(range(len(answer)), config.tournament_size)
        fit = float('inf')
        for j in select_index:
            if answer[j] < fit:
                fit = answer[j]
                index = j
        S_job[i] = work_job[index]
        S_machine[i] = work_machine[index]
        S_time[i] = work_time[index]
        S_answer[i] = answer[index]
        S_index[i] = index
    return S_job, S_machine, S_time, S_answer, S_index
