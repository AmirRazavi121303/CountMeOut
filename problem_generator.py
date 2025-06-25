import pandas as pd 
import random

tries = 10 #int(input("How many problems do you want? "))

n = tries - (tries-1)

def generate_random_problem(tries, n):
    problems = [] #stores problems
    while tries > 0: 
        a, b, c = random.randint(-9,9), random.randint(-9,9), random.randint(-9,9) 
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

reason = []
correct = []
student_steps = []
wrong_step = []

def generate_random_answers(problems, reason, correct, student_steps, wrong_step): 
    answers = []
    odds = 0.3
    for item in problems:
        right_or_wrong = random.randint(1, 100)
        if (right_or_wrong / 100) > odds: 
            answers.append(eval(item))
            reason.append("None")
            correct.append(True)
            wrong_step.append("None")
        else:  
            right_or_wrong = random.randint(1, 100) 
            if (right_or_wrong / 100) > odds:
                answers.append((eval(item)) * (-1))
                reason.append("Sign misconception")
            else:
                answers.append((eval(item)) * 2) #if answer is 0 this wont work fix plz
                reason.append("Random 2 multiplication")
            correct.append(False)
    
    #this part adds student steps to the problem. 
    #for example if the problem is 3 * 5 - 9 the steps would be: step 1: 3*5, step 2: 15-9
    for i, prob in enumerate(problems):
        a, op1, b, op2, c = prob.split()
        if correct[i]:
            if op1 in ('*', '/'):  # check if op1 is * or /
                step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                middle = eval(f'{a} {op1} {b}')
                step_2 = f"{middle} {op2} {c} = {answers[i]}"
            elif op1 not in ('*', '/') and op2 in ('*', '/'):  # check op2 for * or /
                step_1 = f"{b} {op2} {c} = {eval(f'{b} {op2} {c}')}"
                middle = eval(f'{b} {op2} {c}')
                step_2 = f"{a} {op1} {middle} = {answers[i]}"
            elif op1 in ('+', '-'): 
                step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                middle = eval(f'{a} {op1} {b}')
                step_2 = f"{middle} {op2} {c} = {answers[i]}"
        else: 
            if reason[i] == ("Sign misconception"):
                step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b} * {-1}')}"
                middle = eval(f'{a} {op1} {b}') * -1
                step_2 = f"{middle} {op2} {c} = {answers[i]}"
                wrong_step.insert(i ,"Step 1")
            elif reason[i] == ("Random 2 multiplication"):
                step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                middle = eval(f'{a} {op1} {b}') 
                answers[i]
                step_2 = f"{middle} {op2} {c} = {answers[i]}"
                wrong_step.insert(i, "Step 2")
        student_steps.append(f"Step 1: {step_1}, Step 2: {step_2}")
    return answers


problems = generate_random_problem(tries, n) 
answers = generate_random_answers(problems, reason, correct, student_steps, wrong_step)
df = pd.DataFrame(list(zip(problems, answers, correct, reason, student_steps, wrong_step)), columns=["Problem", "Answer", "Correct?", "Reason", "Student Steps", "Wrong Step"]) 

#df.to_csv('output.csv')

print(df)
