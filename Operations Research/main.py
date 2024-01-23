# -*- coding: utf-8 -*-

import sys
import numpy as np

np.set_printoptions(precision=7)
np.seterr(divide='ignore')

# Tableau Creation Functions

def str2int_arr(str_arr):
    int_arr = np.array(())
    for i in str_arr:
        int_arr = np.append(int_arr, int(i))
    return int_arr

def file2matrix(path):
    file = open(path, 'r')
    lines = file.readlines()
    line_counter = 0

    for line in lines:
        if line_counter >= 2:
            values = str2int_arr(line.split())
            matrix = np.vstack((matrix, values))
        elif line_counter == 1:
            values = str2int_arr(line.split())
            values = np.append(values, 0)
            matrix = np.empty(0)
            matrix = np.append(matrix, values)
        else:
            restrictions, variables = lines[0].split()
            restrictions = int(restrictions)
            variables = int(variables)
        line_counter += 1
    
    return matrix, restrictions, variables

def matrix2tableau(matrix, restrictions):
    matrix[0] *= -1
    b = np.matrix(matrix[:,-1])
    b = np.transpose(b)

    wo_b = np.delete(matrix,-1,1)
    
    id = np.eye(restrictions)
    id = np.vstack([np.zeros((1,restrictions)),id])
    
    tableau = np.hstack([wo_b,id,b])
    tableau[0,-1] = 0
    
    return tableau

# Auxiliary Functions

def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

def non_positive(column):
    if column[0] != 0:
        if np.all(column <= 0):
            return True
    return False

# Pivoting Functions

def get_pivot_position(tableau, col):
    b_over_A = tableau[1:,-1] / tableau[1:,col]
    b_over_A[b_over_A <= 0] = np.inf
    row = np.argmin(b_over_A) + 1
    return row, col

def pivot_step(tableau, pivot_position):
    pivot_row, pivot_col = pivot_position
    index = 0
    tableau[pivot_row] /= tableau[pivot_row,pivot_col]
    for row in tableau:
        if index != pivot_row:
            if tableau[index,pivot_col] != 0:
                coef = tableau[index,pivot_col]
                row -= coef * tableau[pivot_row]
        index += 1
    return tableau

def pivot(tableau, opt):
    pivot_position = get_pivot_position(tableau, opt)
    tableau = pivot_step(tableau, pivot_position)
    return tableau

# Possible States

def infeasible(tableau):
    for row in tableau[1:]:
        A_row = row[0,:-1]
        b_row = row[0,-1]
        cond1 = np.all(A_row >= 0) and b_row < 0
        cond2 = np.all(A_row <= 0) and b_row > 0
        if cond1 or cond2:
            return True
    return False

def unbounded(tableau):
    columns = np.array(tableau).T
    for column in columns[:-1]:
        if non_positive(column):
            return unb_sol(tableau)
    return np.empty(0)

def optimal(tableau):
    columns = np.array(tableau).T
    index = 0
    for column in columns:
        if column[0] < 0:
            return index
        index += 1
    return -1

# Optimal output

def opt_opt(tableau):
    return tableau[0,-1]

def opt_sol(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)
    sol_len = tableau.shape[1] - tableau.shape[0]
    return solutions[:sol_len]

def opt_cert(tableau):
    index = tableau.shape[1] - tableau.shape[0]
    return tableau[0,index:-1]

# Infeasible Output

def inf_cert(tableau):
    return -tableau[1:,-1]

# Unbounded Output

def unb_sol(tableau):
    col = tableau.shape[1] - tableau.shape[0]
    sol = tableau[0,:col].tolist()
    row = 1
    pos = 0
    for i in sol[0]:
        if i == 0:
            sol[0][pos] = tableau[row,-1]
            row += 1
        else:
            sol[0][pos] = 0
        pos += 1
    return sol

def unb_cert(tableau):
    return unbounded(tableau)

# Print Answers

def answer(string, tableau):
    if string == "inf":
        print('inviavel')
        cert = inf_cert(tableau)
        print(np.reshape(cert, cert.shape[0]))
    elif string == "unb":
        print('ilimitada')
        print(unbounded(tableau))
    elif string == "opt":
        print("otima")
        print(opt_opt(tableau))
        print(opt_sol(tableau))
        print(opt_cert(tableau))
    else:
        print('ERROR')

# Simplex Algorithm

def simplex_algorithm(tableau):
    iter = 0
    while iter < 40:
        if infeasible(tableau):
            answer("inf", tableau)
            break
        if len(unbounded(tableau)) > 0:
            answer("unb", tableau)
            break 
        opt = optimal(tableau)
        if opt == -1:
            answer("opt", tableau)
            break 
        else:
            tableau = pivot(tableau, opt)
        iter += 1

# Main Function

def main():
    matrix, restrictions, variables = file2matrix(str(sys.argv[1]))
    tableau = matrix2tableau(matrix, restrictions)
    simplex_algorithm(tableau)

main()