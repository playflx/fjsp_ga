import random
import numpy as np
from matplotlib import pyplot as plt


class FJSP:

    def __init__(self, job_num, machine_num):
        self.job_num = job_num
        self.machine_num = machine_num

    def axis(self):
        index = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10',
                 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20']
        scale_ls, index_ls = [], []
        for i in range(self.machine_num):
            scale_ls.append(i + 1)
            index_ls.append(index[i])

        return index_ls, scale_ls  # 返回坐标轴信息，按照工件数返回

    # 计算完工时间以
    def calculate(self, job, machine, machine_time):
        job_time = np.zeros((1, self.job_num))
        tmac_time = np.zeros((1, self.machine_num))
        startTime = 0
        list_M, list_S, list_W = [], [], []
        for i in range(job.shape[1]):
            job_index, mac_index = int(job[0, i]), int(machine[0, i]) - 1
            if job_time[0, job_index] > 0:  # 不是工件第一道工序
                startTime = max(job_time[0, job_index], tmac_time[0, mac_index])
                tmac_time[0, mac_index] = startTime + machine_time[0, i]
                job_time[0, job_index] = startTime + machine_time[0, i]
            if job_time[0, job_index] == 0:  # 是工件第一道工序
                startTime = tmac_time[0, mac_index]
                tmac_time[0, mac_index] = startTime + machine_time[0, i]
                job_time[0, job_index] = startTime + machine_time[0, i]
            list_M.append(machine[0, i])
            list_S.append(startTime)
            list_W.append(machine_time[0, i])

        tax = np.argmax(tmac_time[0]) + 1  # 结束最晚机器
        C_finish = max(tmac_time[0])  # 最大完工时间

        return C_finish, list_M, list_S, list_W, tax

    # 绘制甘特图
    def draw(self, job, machine, machine_time, index):  # 画图
        C_finish, list_M, list_S, list_W, tax = self.calculate(job, machine, machine_time)
        figure, ax = plt.subplots()
        count = np.zeros((1, self.job_num))
        for i in range(job.shape[1]):  # 每一道工序画一个小框
            count[0, int(job[0, i])] += 1
            plt.bar(x=list_S[i], bottom=list_M[i], height=0.5, width=list_W[i], orientation="horizontal", color='white',
                    edgecolor='black')
            plt.text(list_S[i] + list_W[i] / 32, list_M[i], '%.0f' % (job[0, i] + 1), color='black', fontsize=10,
                     weight='bold')
        plt.plot([C_finish, C_finish], [0, tax], c='black', linestyle='-.', label='完工时间=%.1f' % C_finish)
        font1 = {'weight': 'bold', 'size': 22}
        plt.title("甘特图MK0{}".format(index), font1)
        plt.ylabel("机器", font1)

        scale_ls, index_ls = self.axis()
        plt.yticks(index_ls, scale_ls)
        plt.axis([0, C_finish * 1.1, 0, self.machine_num + 1])
        plt.tick_params(labelsize=22)
        labels = ax.get_xticklabels()
        [label.set_fontname('FangSong') for label in labels]
        plt.legend(prop={'family': ['STSong'], 'size': 16})
        plt.savefig('./images/ga' + str(index) + '.png', )
        plt.show()
