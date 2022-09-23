# Matt Boutell
# Attempt to solve the partition problem, approximately, using simulated 
# annealing.


from operator import truediv
import numpy as np
import random

numbers = [14175, 15055, 16616, 17495, 18072, 19390, 19731, 22161, 23320, 23717, 26343, 28725, 29127, 32257, 40020, 41867, 43155, 46298, 56734, 57176, 58308, 61848, 65825, 66042, 68634, 69189, 72936, 74287, 74537, 81942, 82027, 82623, 82802, 82988, 90467, 97042, 97507, 99564]
numbers = np.array(numbers)
target = 1000000

def annealing(numbers, target):
    problem = Partition(numbers, target)
    s = problem.get_initial_solution()
    t = 1
    epsilon = 0.00000001
    learning_rate = 0.99
    while t > epsilon:
        if problem.is_exact(s):
            break
        s_nbr = problem.find_neighbor(s)
        e = problem.scaled_distance_from_target(s)
        e_nbr = problem.scaled_distance_from_target(s_nbr)
        # We are minimiizing the distance from the target.
        # If delta_e > 0, e(delta_e) > 1, so we always accept.
        # We want to accept the neighbor if it is smaller.
        # To make delta_e > 0 when s_neighbor < s, we take e - e_nbr
        if problem.isMin:
            delta_e = e - e_nbr
        else:
            delta_e = e_nbr - e 
        rand = random.random()
        if rand < np.exp(delta_e / t):
            s = s_nbr
            print("new best has sum", problem.partition_sum(s))
        t *= learning_rate
    
    print("found best solution with sum", problem.partition_sum(s), "difference = ", problem.distance_from_target(s))
    print(s)

class Partition():
    def __init__(self, numbers, target):
        self.numbers = numbers
        self.target = target
        self.isMin = True

    def get_initial_solution(self):
        # Encoding uses a binary vector: 1 = corresponding number in the list is in partition
        # Eg, [1, 0, 1, 0, ...] includes the numbers in position 0 and 2 plus others.
        solution = np.zeros(len(self.numbers))
        # How many? Use the expected size of each one:
        expected_size_of_one = numbers.mean()
        num_in_partition = target / expected_size_of_one
        # Set that many places to one
        while sum(solution) < num_in_partition:
            random_index = random.randint(0, len(solution) - 1)
            solution[random_index] = 1
        return solution

    def find_neighbor(self, s):
        neighbor = s.copy()
        random_index = random.randint(0, len(neighbor) - 1)
        neighbor[random_index] = 1 - neighbor[random_index]
        return neighbor

    def scaled_distance_from_target(self, s):
        distance = self.distance_from_target(s)
        return 10*(distance / self.target - 1)

    def distance_from_target(self, s):
        total = self.partition_sum(s)
        return np.abs(total - self.target)
        
    def partition_sum(self, s):
        return np.dot(s, self.numbers)

    def is_exact(self, s):
        return self.partition_sum(s) == target

annealing(numbers, target)