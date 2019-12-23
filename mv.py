import numpy as np


def mv(data):
    """Majority Voting method for worker model.

    labeltask: Labels of each task assigned by workers
    ntask: The number of tasks
    """
    labeltask = data[3].squeeze()
    ntask = data[6].squeeze()

    results = np.zeros(ntask)
    
    for idx, task in enumerate(labeltask):
        num_class_one = 0
        num_class_two = 0
        
        for label in task[0]:
            if label == 1:
                num_class_one += 1
            else:
                num_class_two += 1
                
        if num_class_one >= num_class_two:
            results[idx] = 1
        else:
            results[idx] = 2
            
    return results
