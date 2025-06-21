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
student_steps = []

def generate_random_answers(problems, wrong_answers, reason, correct, student_steps): 
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
        else: #ill figure this out later lol
            step_1 = "caca"
            step_2 = "coco"
        student_steps.append(f"Step 1: {step_1}, Step 2: {step_2}")
    return answers


problems = generate_random_problem(tries, n) 
answers = generate_random_answers(problems, wrong_answers, reason, correct, student_steps)
df = pd.DataFrame(list(zip(problems, answers, correct, reason, student_steps)), columns=["Problem", "Answer", "Correct?", "Reason", "Student Steps"]) 

#df.to_csv('output.csv')

print(df)

"""if len(wrong_answers) > 0 :
    print("\nThe following problems are wrong:") 
    for index, item in enumerate(wrong_answers):
        print(f"{index}: {item}")
else:
    print(f"\nNo wrong answers within these problems")
print('')"""