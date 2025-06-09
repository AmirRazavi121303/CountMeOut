import pandas as pd 
import random

tries = 5 #int(input("How many problems do you want? "))

n = tries - (tries-1)

def generate_random_problem(tries, n):
    problems = []
    while tries > 0: 
        a, b, c = random.randint(1,9), random.randint(1,9), random.randint(1,9)
        ops = ['+', '-', '*', '/']
        op1, op2 = random.choice(ops[0:3]), random.choice(ops) #just cuz i dont ever want the first operator to be a division 
        problems.append(f"Problem {n}: {a} {op1} {b} {op2} {c} ")
        tries -= 1;
        n += 1
    return problems

problems = generate_random_problem(tries, n)
columns = [f"Problem {i+1}" for i in range(len(problems))]
df = pd.DataFrame(problems, columns=["Problem"])

print(df)