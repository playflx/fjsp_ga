import copy
import random
from itertools import chain

import numpy as np
from lxml.html.builder import CODE


# pox交叉算子
class pox:
    def __init__(self, job_num):
        self.job_num = job_num  # 工件数

    def pox_improve(self, f1, f2):

        p1 = copy.deepcopy(f1)
        p2 = copy.deepcopy(f2)
        p1 = p1.tolist()
        p2 = p2.tolist()
        child_1, child_2 = [-1] * len(f1), [-1] * len(f2)
        # 建立工件集合
        job_set = [_ for _ in range(self.job_num)]
        num = np.random.randint(1, self.job_num)  # 选取要pox的集合数
        j_set1 = np.random.choice(job_set, int(self.job_num/2), replace=False)
        j_set2 = [0] * (self.job_num - len(j_set1))
        k = 0
        for i in range(self.job_num):
            if i not in j_set1:
                j_set2[k] = i
                k += 1
        j_set2 = np.array(j_set2)
        asd = j_set2[0]
        index_c2_of_p1_set = []
        index_c1_of_p2_set = []
        for i in range(len(j_set1)):
            index_j1_of_p1 = np.where(p1 == j_set1[i])[0]
            index_j1_of_p2 = np.where(p2 == j_set1[i])[0]

            for j in range(np.size(index_j1_of_p1)):
                a1 = index_j1_of_p1[j]
                a2 = index_j1_of_p2[j]
                child_1[a1] = p1[a1]
                child_2[a2] = p2[a2]
        k1, j_1 = 0, 0
        k2, j_2 = 0, 0
        j_set1 = j_set1.tolist()
        j_set2 = j_set2.tolist()
        while k1 < len(p1):
            if p1[k1] not in j_set2:
                k1 += 1
            else:
                if child_2[j_1] == -1:
                    child_2[j_1] = p1[k1]
                    j_1 +=1
                    k1 += 1
                else:
                    j_1 += 1
        while k2 < len(p2):
            if p2[k2] not in j_set2:
                k2 += 1
            else:
                if child_1[j_2] == -1:
                    child_1[j_2] = p2[k2]
                    j_2 += 1
                    k2 += 1
                else:
                    j_2 += 1
        child_1 = np.array(child_1).reshape(1, f1.shape[1])
        child_2 = np.array(child_2).reshape(1, f2.shape[1])
        return child_1,child_2


#
jobs = [_ for _ in range(10)]
random.shuffle(jobs)
job1 = copy.deepcopy(jobs)
random.shuffle(jobs)
job2 = copy.deepcopy(jobs)
obj_pox = pox(10)
child1,child2 = obj_pox.pox_improve(job1, job2)
print(job1)
print(job2)
print(child1)
print(child2)


