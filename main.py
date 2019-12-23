from bp import bp
from em import em
from matplotlib import pyplot as plt
from mv import mv
import numpy as np
import os
from scipy import io
import time


def main():
    tol = 0.00001
    max_iter = 100
    alpha = 2
    beta = 1

    """SYN dataset"""
    tag_syn = os.path.join("data", "SYN_data", "SYN_r")
    num_trials = 10

    plot_mv = []
    plot_bp = []
    plot_em = []

    for value in range(1, 20, 2):  # r=1,3,5,6,7,9,11,13,15,17,19, means number of tasks assigned to each worker
        avg_error_mv = 0
        avg_error_bp = 0
        avg_error_em = 0

        time_mv = 0
        time_bp = 0
        time_em = 0
        for i in range(num_trials):  # trial=1~10
            data = io.loadmat(tag_syn+"{}_{}.mat".format(value, i+1))["data"][0][0]
            true_labels = io.loadmat(tag_syn+"{}_{}_true.mat".format(value, i+1))["true_labels"][0]

            """MV"""
            start = time.time()
            est_mv = mv(data)
            error_mv = np.average(est_mv != true_labels)
            avg_error_mv += error_mv
            end = time.time()
            time_mv += end-start
            """"""

            """BP"""
            start = time.time()
            est_bp = bp(data, max_iter, tol, alpha, beta)
            error_bp = np.average(est_bp != true_labels)
            avg_error_bp += error_bp
            end = time.time()
            time_bp += end-start
            """"""

            """EM"""
            start = time.time()
            est_em = em(data, max_iter, tol, alpha, beta)
            error_em = np.average(est_em != true_labels)
            avg_error_em += error_em
            end = time.time()
            time_em += end-start
            """"""

        avg_error_mv = avg_error_mv/num_trials
        print("In SYN dataset using MV, when r={}, error rate is {}, time is {} secs".
              format(value, avg_error_mv, time_mv))
        avg_error_bp = avg_error_bp/num_trials
        print("In SYN dataset using BP, when r={}, error rate is {}, time is {} secs".
              format(value, avg_error_bp, time_bp))
        avg_error_em = avg_error_em/num_trials
        print("In SYN dataset using EM, when r={}, error rate is {}, time is {} secs".
              format(value, avg_error_em, time_em))

        plot_mv.append(avg_error_mv)
        plot_bp.append(avg_error_bp)
        plot_em.append(avg_error_em)

    plt.figure(figsize=(10, 8))
    plt.title("SYN dataset")
    plt.xlabel("r", )
    plt.ylabel("error")
    plt.xlim(0, 20)
    plt.ylim(0, 1)
    plt.plot([i for i in range(1, 20, 2)], plot_mv, label="MV")
    plt.plot([i for i in range(1, 20, 2)], plot_bp, label="BP")
    plt.plot([i for i in range(1, 20, 2)], plot_em, label="EM")
    plt.legend(loc="upper left")
    plt.show()
    """"""

    """SIM dataset"""
    tag_sim = os.path.join("data", "SIM_data", "SIM_l")
    num_trials = 10

    plot_mv = []
    plot_bp = []
    plot_em = []

    for value in [1, 5, 10, 15, 20, 25]:  # l=1,5,10,15,20,25, means number of workers assigned to each task
        avg_error_mv = 0
        avg_error_bp = 0
        avg_error_em = 0

        time_mv = 0
        time_bp = 0
        time_em = 0
        for i in range(num_trials):  # trial=1~10
            data = io.loadmat(tag_sim+"{}_{}.mat".format(value, i+1))["data"][0][0]
            true_labels = io.loadmat(tag_sim+"{}_{}_true.mat".format(value, i+1))["true_labels"][0]

            """MV"""
            start = time.time()
            est_mv = mv(data)
            error_mv = np.average(est_mv != true_labels)
            avg_error_mv += error_mv
            end = time.time()
            time_mv += end-start
            """"""

            """BP"""
            start = time.time()
            est_bp = bp(data, max_iter, tol, alpha, beta)
            error_bp = np.average(est_bp != true_labels)
            avg_error_bp += error_bp
            end = time.time()
            time_bp += end-start
            """"""

            """EM"""
            start = time.time()
            est_em = em(data, max_iter, tol, alpha, beta)
            error_em = np.average(est_em != true_labels)
            avg_error_em += error_em
            end = time.time()
            time_em += end-start
            """"""

        avg_error_mv = avg_error_mv/num_trials
        print("In SIM dataset using MV, when l={}, error rate is {}, time is {} secs".
              format(value, avg_error_mv, time_mv))
        avg_error_bp = avg_error_bp/num_trials
        print("In SIM dataset using BP, when l={}, error rate is {}, time is {} secs".
              format(value, avg_error_bp, time_bp))
        avg_error_em = avg_error_em/num_trials
        print("In SIM dataset using EM, when l={}, error rate is {}, time is {} secs".
              format(value, avg_error_em, time_em))

        plot_mv.append(avg_error_mv)
        plot_bp.append(avg_error_bp)
        plot_em.append(avg_error_em)

    plt.figure(figsize=(10, 8))
    plt.title("SIM dataset")
    plt.xlabel("l")
    plt.ylabel("error")
    plt.xlim(0, 30)
    plt.ylim(0, 1)
    plt.plot([1, 5, 10, 15, 20, 25], plot_mv, label="MV")
    plt.plot([1, 5, 10, 15, 20, 25], plot_bp, label="BP")
    plt.plot([1, 5, 10, 15, 20, 25], plot_em, label="EM")
    plt.legend(loc="upper left")
    plt.show()
    """"""

    """TEMP dataset"""
    data = io.loadmat("data/other_data/TEMP_data.mat")["data"][0][0]
    true_labels = io.loadmat("data/other_data/TEMP_data_true.mat")["true_labels"][0]

    """MV"""
    start = time.time()
    est_mv = mv(data)
    error_mv = np.average(est_mv != true_labels)
    end = time.time()
    time_mv = end-start
    """"""

    """BP"""
    start = time.time()
    est_bp = bp(data, max_iter, tol, alpha, beta)
    error_bp = np.average(est_bp != true_labels)
    end = time.time()
    time_bp = end-start
    """"""

    """EM"""
    start = time.time()
    est_em = em(data, max_iter, tol, alpha, beta)
    error_em = np.average(est_em != true_labels)
    end = time.time()
    time_em = end-start
    """"""

    print("In TEMP dataset using MV, error rate is {}, time is {} secs".format(error_mv, time_mv))
    print("In TEMP dataset using BP, error rate is {}, time is {} secs".format(error_bp, time_bp))
    print("In TEMP dataset using EM, error rate is {}, time is {} secs".format(error_em, time_em))
    """"""


if __name__ == "__main__":
    main()
