
import random

tries = int(input("How many problems do you want? "))

problems = ""
n = tries - (tries-1)

def generate_random_problem(tries, problems, n):
    while tries > 0: 
        a, b, c = random.randint(1,9), random.randint(1,9), random.randint(1,9)
        ops = ['+', '-', '*', '/']
        op1, op2 = random.choice(ops[0:3]), random.choice(ops) #just cuz i dont ever want the first operator to be a division 
        problems += f"Problem {n}: {a} {op1} {b} {op2} {c} \n" 
        tries -= 1;
        n += 1
    return problems

print(generate_random_problem(tries, problems, n))
