from utils import fileName


def read(index):
    file_name = fileName.file_name + str(index) + '.fjs'
    f = open(file_name)
    lines = f.readlines()
    parameters, count = [], 0
    job_num, machine_num = 0, 0
    for line in lines:
        tread = line.strip('\n')
        if len(tread) == 0: break
        if count > 0:
            jmt = []
            j = 0
            while j < len(tread):
                if tread[j] != ' ' and tread[j] != '\t':
                    if j + 1 == len(tread):
                        jmt.append(int(tread[j]))
                    if j + 1 < len(tread) and (tread[j + 1] == ' ' or tread[j + 1] == '\t'):
                        jmt.append(int(tread[j]))
                    if j + 1 < len(tread) and tread[j + 1] != ' ' and tread[j + 1] != '\t':
                        num = tread[j] + tread[j + 1]
                        jmt.append(int(num))
                        j += 1
                j += 1
            parameters.append(jmt)
        # 文件第一行，取机器数和工件数
        else:
            jm_num = []
            j = 0
            while j < len(tread):
                if len(jm_num) >= 2:
                    break
                if tread[j] != ' ' and tread[j] != '\t':
                    if j + 1 < len(tread) and (tread[j + 1] == ' ' or tread[j + 1] == '\t'):
                        jm_num.append(int(tread[j]))
                    if j + 1 < len(tread) and tread[j + 1] != ' ' and tread[j + 1] != '\t':
                        num = tread[j] + tread[j + 1]
                        jm_num.append(int(num))
                        j += 1

                j += 1
            job_num = jm_num[0]
            machine_num = jm_num[1]
        count += 1
    return parameters, job_num, machine_num
