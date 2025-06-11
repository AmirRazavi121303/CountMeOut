import pandas as pd 
import random

tries = 5 #int(input("How many problems do you want? "))

n = tries - (tries-1)

def generate_random_problem(tries, n):
    problems = [] #stores problems
    while tries > 0: 
        a, b, c = random.randint(1,9), random.randint(1,9), random.randint(1,9) 
        ops = ['+', '-', '*', '/']
        op1, op2 = random.choice(ops[0:3]), random.choice(ops) #just cuz i dont ever want the first operator to be a division 
        problems.append(f"{a} {op1} {b} {op2} {c} ")
        if eval(problems[-1]) % 1 == 0:
            tries -= 1
            n += 1
        else:
            problems.pop()
            generate_random_problem(tries, n)
    return problems

def generate_answers(problems): #generates answers to the problems, reminder: make it so it gives an answer based on a certain probability
    answers = []
    for item in problems:
        answers.append(eval(item))
    return answers


problems = generate_random_problem(tries, n) #this is how i store the problems generated 
answers = generate_answers(problems)
columns = [f"Problem {i+1}" for i in range(len(problems))] #creates the name for every column
df = pd.DataFrame(answers, problems, columns=["Problem"]) #creates the dataframe with each newly generated set of problems

print(df)