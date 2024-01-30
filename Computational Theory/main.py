import sys
import numpy as np

def ler_automato(arquivo):
    with open(arquivo, 'r') as file:
        states = file.readline().strip().split(',')
        alpha = file.readline().strip().split(',')
        start = file.readline().strip().split(',')
        finish = file.readline().strip().split(',')
        transitions = []
        for line in file:
            transitions.append(line.strip().split(','))
    return states, alpha, start, finish, transitions

def eliminar_estado(transitions, state):
    incoming = [t for t in transitions if t[2] == state]
    outgoing = [t for t in transitions if t[0] == state]
    for inc in incoming:
        for out in outgoing:
            if inc[0] != out[2]:
                new_path = inc[1] + out[1]
                transitions.append([inc[0], new_path, out[2]])
    return [t for t in transitions if state not in t]

def converter_para_er(states, start, finish, transitions):
    for state in states:
        if state not in start and state not in finish:
            transitions = eliminar_estado(transitions, state)
    er_transitions = [t for t in transitions if t[0] in start and t[2] in finish]
    return '+'.join(['(' + t[1] + ')' for t in er_transitions])

def main(arquivo_entrada):
    states, alpha, start, finish, transitions = ler_automato(arquivo_entrada)
    er = converter_para_er(states, start, finish, transitions)
    print(er)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 programa.py <arquivo_entrada>")
    else:
        main(sys.argv[1])