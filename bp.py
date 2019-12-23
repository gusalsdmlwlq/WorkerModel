import math
import numpy as np


def bp(data, max_iter, tol, alpha, beta):
    """Belief Propagation method for worker model.

    adj: Answer matrix between workers and tasks.
    ntask: The number of tasks.
    nwork: The number of workers.
    neibtask: Index of workers assigned to each task.
    neibwork: Index of tasks assigned to each worker.
    """
    adj = data[0]
    ntask = data[6].squeeze()
    nwork = data[7].squeeze()
    neibtask = data[13].squeeze()
    neibwork = data[14].squeeze()

    r_u = data[10].squeeze()  # number of task assigned to each worker

    s = np.zeros(ntask)  # labels of tasks to be estimated

    """
    m_iu_1: Message matrix from tasks to workers when s is 1
    m_iu_2: Message matrix from tasks to workers when s is 2
    m_ui_1: Message matrix from workers to tasks when s is 1
    m_ui_2: Message matrix from workers to tasks when s is 2
    """
    m_iu_1 = np.ones((ntask+1, nwork+1))/2
    m_iu_2 = np.ones((ntask+1, nwork+1))/2
    m_ui_1 = np.ones((nwork+1, ntask+1))/2
    m_ui_2 = np.ones((nwork+1, ntask+1))/2

    s_configs = []  # all configurations for calculating factors
    for i in range(2**(r_u-1)):
        s_configs.append(i)

    def factor_sum(s_nu, worker_idx, target_task_idx, target_task_label):
        """Calculate sum of (factor * message i->u)."""
        result = 0
        for config in s_configs:
            """
            c_u: The number of correct answers of worker u.
            temp: The product of factor and message.
            """
            c_u = 0
            temp = 1
            for j in range(len(s_nu)-1):
                # calculate every configurations of neighbor tasks assigned to worker u excluding target task i
                if config & 1 << j:  # s_j=2
                    temp *= m_iu_2[s_nu[s_nu != target_task_idx][-(j+1)]][worker_idx]  # m_ju(s_j=2)
                    if adj[s_nu[s_nu != target_task_idx][-(j+1)]-1][worker_idx-1] == 2:
                        c_u += 1
                else:  # s_j=1
                    temp *= m_iu_1[s_nu[s_nu != target_task_idx][-(j+1)]][worker_idx]  # m_ju(s_j=1)
                    if adj[s_nu[s_nu != target_task_idx][-(j+1)]-1][worker_idx-1] == 1:
                        c_u += 1
            if adj[target_task_idx-1][worker_idx-1] == target_task_label:
                # target task and worker u's answer are same
                c_u += 1
            temp *= math.gamma(alpha+beta)*math.gamma(alpha+c_u)*math.gamma(beta+len(s_nu)-c_u)\
                / (math.gamma(alpha)*math.gamma(beta)*math.gamma(alpha+beta+len(s_nu)))
            result += temp

        return result

    prev_b_1 = np.ones(ntask)/2  # previous beliefs
    prev_b_2 = np.ones(ntask)/2

    for i in range(max_iter):
        diff = 0  # the difference between beliefs

        """update task->worker"""
        for cur_task in range(1, ntask+1):  # each task i
            for worker in neibtask[cur_task-1][0]:  # worker u
                # update messages from tasks to workers when s is both 1 and 2
                m_1 = 1
                m_2 = 1
                m_i = neibtask[cur_task-1][0]
                for worker_ in m_i[m_i != worker]:  # another worker v
                    m_1 *= m_ui_1[worker_][cur_task]
                    m_2 *= m_ui_2[worker_][cur_task]
                m_norm = m_1 + m_2  # message normalization
                m_iu_1[cur_task][worker] = m_1/m_norm
                m_iu_2[cur_task][worker] = m_2/m_norm
        """"""

        """update worker->task"""
        for cur_worker in range(1, nwork+1):  # each worker u
            for task in neibwork[cur_worker-1][0]:  # task i
                # update messages from workers to tasks when s is both 1 and 2
                s_nu = neibwork[cur_worker-1][0]  # neighbor tasks assigned to worker u
                factor_sum_1 = factor_sum(s_nu, cur_worker, task, 1)
                factor_sum_2 = factor_sum(s_nu, cur_worker, task, 2)
                factor_norm = factor_sum_1 + factor_sum_2  # message normalization
                m_ui_1[cur_worker][task] = factor_sum_1/factor_norm
                m_ui_2[cur_worker][task] = factor_sum_2/factor_norm
        """"""

        """aggregate belief"""
        for cur_task in range(1, ntask+1):  # each task i
            b_1 = 1
            b_2 = 1
            for worker in neibtask[cur_task-1][0]:  # worker: u
                # update beliefs of task i
                b_1 *= m_ui_1[worker][cur_task]
                b_2 *= m_ui_2[worker][cur_task]

            # estimate s, label of task i, maximizing belief
            if b_1 >= b_2:
                s[cur_task-1] = 1
            else:
                s[cur_task-1] = 2

            b_norm = b_1 + b_2  # belief normalization
            b_1 /= b_norm
            b_2 /= b_norm

            diff += (abs(b_1-prev_b_1[cur_task-1])+abs(b_2-prev_b_2[cur_task-1]))/2
            prev_b_1[cur_task-1] = b_1
            prev_b_2[cur_task-1] = b_2
        """"""

        diff /= ntask
        if diff <= tol:
            # stop if converged
            break
        
    return s
