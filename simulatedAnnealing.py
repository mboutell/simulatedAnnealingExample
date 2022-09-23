# Matt Boutell
# Attempt to solve the partition problem, approximately, using simulated 
# annealing.


from symbol import pass_stmt
import numpy as np
import random

numbers = [14175, 15055, 16616, 17495, 18072, 19390, 19731, 22161, 23320, 23717, 26343, 28725, 29127, 32257, 40020, 41867, 43155, 46298, 56734, 57176, 58308, 61848, 65825, 66042, 68634, 69189, 72936, 74287, 74537, 81942, 82027, 82623, 82802, 82988, 90467, 97042, 97507, 99564]
target = 1000000

def annealing(numbers, target):
    # Binary vector: 1 = corresponding number is in partition
    s = get_initial_solution(numbers, target) 
    t = 1
    epsilon = 0.01
    learning_rate = 0.9
    while t > epsilon:
        if partition_sum(s, numbers) == target:
            break
        s_nbr = find_neighbor(s)
        

        t *= learning_rate
    
    print("found best solution with sum", partition_sum(s, numbers))
    print(s)

def get_initial_solution(numbers, target):
    solution = [0 for number in numbers]
    # How many? Use the expected size of each one:
    expected_size_of_one = sum(numbers)/len(numbers)
    num_in_partition = target / expected_size_of_one
    # Set that many places to one
    while sum(solution) < num_in_partition:
        random_index = random.randint(len(solution))
        solution[random_index] = 1
    return solution

def find_neighbor(s):
    neighbor = s.copy()
    random_index = random.randint(len(neighbor))
    neighbor[random_index] = 1 - neighbor[random_index]
    return neighbor

def partition_sum(s, numbers):
    # TODO: Just a dot product, so use numpy.
    total = 0
    for k in range(len(numbers)):
        total += s*numbers
    return total

annealing()