import argparse
import numpy as np
import time
from sudoku_pair_solver import *
import random

random.seed(random.randint(1, 1e6))

start_time = time.time()
ap = argparse.ArgumentParser()
ap.add_argument('-k', '--kdim', required=True, help='Value of k')
ap.add_argument('-o', '--output_file', required=True, help='Name of the csv file to dump the results')
args = vars(ap.parse_args())

kdim = int(args['kdim'])
file_name = args['output_file']

def random_generate():
    pos_x = random.randint(1, kdim**2)
    pos_y = random.randint(1, kdim**2)
    return pos_x, pos_y


i_x_1, i_y_1 = random_generate()
i_x_2, i_y_2 = random_generate()

while i_x_2 == i_x_1 and i_y_1 == i_y_2:
    i_x_2, i_y_2 = random_generate()


num_1 = random.randint(1, kdim**2)
num_2 = random.randint(1, kdim**2)

grid_1 = np.zeros((kdim**2, kdim**2)).tolist()
grid_2 = np.zeros((kdim**2, kdim**2)).tolist()


solver = Solver(kdim, grid_1, grid_2, file_name)
solver.get_clauses()

grid_1[i_x_1-1][i_y_1-1] = num_1
grid_2[i_x_2-1][i_y_2-1] = num_2

solver.solve()
solver.set_grid()

solver.add_solution_clauses()
solver.get_fixed_clauses()
solver.print_grid()
print()


done = False
count = 0
for _ in range(kdim**4):
    count += 1
    pos_x_1, pos_y_1 = random_generate()
    pos_x_2, pos_y_2 = random_generate()
    prev_1, prev_2 = None, None

    while solver.grid_1[pos_x_1-1][pos_y_1-1] == 0:
        pos_x_1, pos_y_1 = random_generate()
    
    prev_1 = solver.grid_1[pos_x_1-1][pos_y_1-1]
    solver.grid_1[pos_x_1-1][pos_y_1-1] = 0

    while solver.grid_2[pos_x_2-1][pos_y_2-1] == 0:
        pos_x_2, pos_y_2 = random_generate()
    
    prev_2 = solver.grid_2[pos_x_2-1][pos_y_2-1]
    solver.grid_2[pos_x_2-1][pos_y_2-1] = 0

    print(f'Zeros made: {count}')

    solver.get_clauses_updated(pos_x_1, pos_y_1, prev_1, pos_x_2, pos_y_2, prev_2)

    x = solver.solve()
    
    if x:
        print()
        solver.grid_1[pos_x_1-1][pos_y_1-1] = prev_1
        solver.grid_2[pos_x_2-1][pos_y_2-1] = prev_2
        solver.print_grid()
        print(f'Number of zeros : {count-1}')
        done = True
    
    if done:
        break        

solver.print_grid_to_csv()
end_time = time.time()
print(f'Time taken: {end_time-start_time}')