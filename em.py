import numpy as np


def em(data, max_iter, tol, alpha, beta):
    """Expectation Maximization method for worker model.

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
    
    p = np.ones(nwork)*0.6  # reliability of workers initialized by 0.6
    
    s = np.zeros(ntask)  # labels of tasks to be estimated
    
    prev_prob1 = np.ones(ntask)  # probability of labels
    prev_prob2 = np.ones(ntask)
    
    for i in range(max_iter):
        diff = 0  # the difference between probabilities

        """estimate label"""
        for label in range(ntask):
            prob1 = 1
            prob2 = 1
            for worker in neibtask[label][0]:
                # update probabilities of label
                if adj[label][worker-1] == 1:
                    prob1 *= p[worker-1]
                    prob2 *= (1-p[worker-1])
                else:
                    prob1 *= (1-p[worker-1])
                    prob2 *= p[worker-1]

            # estimate label of task, maximizing probability
            if prob1 >= prob2:
                s[label] = 1
            else:
                s[label] = 2

            norm = prob1 + prob2  # probability normalization
            prob1 /= norm
            prob2 /= norm

            diff += (abs(prev_prob1[label]-prob1)+abs(prev_prob2[label]-prob2))/2
            prev_prob1[label] = prob1
            prev_prob2[label] = prob2
        """"""
        
        """update reliability"""
        for worker in range(nwork):
            temp = 0  # sum of probabilities
            r_u = len(neibwork[worker][0])  # the number of tasks assigned to worker

            if r_u == 0:  # exception for workers not take any tasks
                continue

            for task in neibwork[worker][0]:
                if adj[task-1][worker] == 1:
                    temp += prev_prob1[task-1]
                else:
                    temp += prev_prob2[task-1]

            # update reliability of workers
            p[worker] = (temp+alpha-1)/(r_u+alpha+beta-2)
        """"""
        
        diff /= ntask
        if diff <= tol:
            # stop if converged
            break
        
    return s
