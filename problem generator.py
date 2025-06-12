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

wrong_answers = []

def generate_random_answers(problems, wrong_answers): #generates answers to the problems, reminder: make it so it gives an answer based on a certain probability
    answers = []
    wrong_answers = []
    odds = 0.3 #this is the odds of the machine printing the wrong answer to a problem
    for item in problems:
        right_or_wrong = random.sample(list(range(1,100)), 1)[0]  # moved inside the loop
        if (right_or_wrong / 100) > odds: #if odds are in our favour, give right answer
            answers.append(eval(item))
        else:  #else give wrong answer
            answers.append("poop") #for now wrong answers can just be identified by "poop", i will fix this
            #wrong_answers.append(answers.pop())
    return answers

#reminder: make it such that the function signals somehow when an answer is wrong

problems = generate_random_problem(tries, n) #this is how i store the problems generated 
answers = generate_random_answers(problems, wrong_answers)
columns = [f"Problem {i+1}" for i in range(len(problems))] #creates the name for every column
df = pd.DataFrame(list(zip(problems, answers)), columns=["Problem", "Answer"]) #creates the dataframe with each newly generated set of problems

print(df)
