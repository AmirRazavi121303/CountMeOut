import pandas as pd 
import random

tries = 10 #int(input("How many problems do you want? "))

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
            # just continue, do not call generate_random_problem again
    return problems

wrong_answers = []
reason = []
correct = []

def generate_random_answers(problems, wrong_answers, reason, correct): 
    answers = []
    odds = 0.3
    for item in problems:
        right_or_wrong = random.randint(1, 100)
        if (right_or_wrong / 100) > odds: 
            answers.append(eval(item))
            reason.append("None")
            correct.append(True)
        else:  
            wrong_answers.append(item)
            right_or_wrong = random.randint(1, 100) 
            if (right_or_wrong / 100) > odds:
                answers.append((eval(item)) * (-1))
                reason.append("Sign misconception")
            else:
                answers.append((eval(item)) * 2)
                reason.append("Random 2 multiplication")
            correct.append(False)
    return answers

problems = generate_random_problem(tries, n) 
answers = generate_random_answers(problems, wrong_answers, reason, correct)
df = pd.DataFrame(list(zip(problems, answers, correct, reason)), columns=["Problem", "Answer", "Correct?", "Reason"]) 

#df.to_csv('output.csv')

print(df)

"""if len(wrong_answers) > 0 :
    print("\nThe following problems are wrong:") 
    for index, item in enumerate(wrong_answers):
        print(f"{index}: {item}")
else:
    print(f"\nNo wrong answers within these problems")
print('')"""