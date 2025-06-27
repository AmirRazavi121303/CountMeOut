import pandas as pd 
import random

class MathProblem:
    def is_valid(self):
        # ...existing code or raise NotImplementedError...
        raise NotImplementedError
    def __str__(self): 
        # ...existing code or raise NotImplementedError...
        raise NotImplementedError

class ArithmeticProblem(MathProblem):
    def __init__(self, a, b, c, op1, op2):
        self.a = a
        self.b = b
        self.c = c
        self.op1 = op1
        self.op2 = op2
        self.problem_str = f"{a} {op1} {b} {op2} {c}"
        try: 
            self.correct_answer = eval(self.problem_str)
        except ZeroDivisionError:
            self.correct_answer = None
    def is_valid(self):
        return self.correct_answer is not None and self.correct_answer % 1 == 0
    def __str__(self): 
        return self.problem_str

class AlgebraicProblem(MathProblem):
    def __init__(self, a, b, op2, x):
        self.a = a
        self.b = b
        self.op2 = op2
        self.x = random.randint(-9, 9)
        self.problem_str = f"{a}x {op2} {b} = "
        try:
            self.correct_answer = eval(f"{a}*{self.x} {op2} {b}")
        except ZeroDivisionError:
            self.correct_answer = None
    def is_valid(self):
        return self.correct_answer is not None and self.correct_answer % 1 == 0
    def __str__(self):
        return self.problem_str

class StudentAttempt: 
    def __init__(self, problem: MathProblem, error_chance = 0.3):
        self.problem = problem
        self.correct = random.randint(1,100) / 100 > error_chance
        self.reason = "None" if self.correct else random.choice(["Sign misconception", "Random 2 multiplication", ])
        self.answer = None
        self.steps = None
        self.wrong_step = "None"
        self.generate_attempt()
        
    def generate_attempt(self):
        a, b, c = self.problem.a, self.problem.b, self.problem.c
        op1, op2 = self.problem.op1, self.problem.op2
        
        try:
            if self.correct is True:
                if op1 in ('*', '/'):  # check if op1 is * or /
                    step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                    middle = eval(f'{a} {op1} {b}')
                    step_2 = f"{middle} {op2} {c} = {eval(self.problem.problem_arithmetic)}"
                elif op1 not in ('*', '/') and op2 in ('*', '/'):  # check op2 for * or /
                    step_1 = f"{b} {op2} {c} = {eval(f'{b} {op2} {c}')}"
                    middle = eval(f'{b} {op2} {c}')
                    step_2 = f"{a} {op1} {middle} = {eval(self.problem.problem_arithmetic)}"
                elif op1 in ('+', '-'): 
                    step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                    middle = eval(f'{a} {op1} {b}')
                    step_2 = f"{middle} {op2} {c} = {eval(self.problem.problem_arithmetic)}"
                self.answer = eval(self.problem.problem_arithmetic)
            else: # to add more errors you have to edit under this block
                if self.reason == "Sign misconception":
                    step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}') * -1}"
                    middle = eval(f'{a} {op1} {b}') * -1
                    step_2 = f"{middle} {op2} {c} = {eval(f'{middle}{op2}{c}')}"
                    self.answer = eval(f'{middle}{op2}{c}')
                    self.wrong_step = "Step 1"
                elif self.reason == "Random 2 multiplication":
                    step_1 = f"{a} {op1} {b} = {eval(f'{a} {op1} {b}')}"
                    middle = eval(f'{a} {op1} {b}') 
                    self.answer = middle * 2
                    step_2 = f"{middle} {op2} {c} = {self.answer}"
                    self.wrong_step = "Step 2"
            self.steps = f"Step 1: {step_1}, Step 2: {step_2}"
        except:
            self.answer = None
            self.steps = "Error in computation"
            self.wrong_step = "Error"


def generate_dataset(n_problems, problem_type="arithmetic"):
    data = []
    count = 0
    while count < n_problems:
        a, b, c = random.randint(-9,9), random.randint(-9,9), random.randint(-9,9) 
        ops = ['+', '-', '*', '/']
        op1, op2 = random.choice(ops[0:3]), random.choice(ops)
        if problem_type == "arithmetic":
            problem = ArithmeticProblem(a, b, c, op1, op2)
        elif problem_type == "algebraic":
            problem = AlgebraicProblem(a, b, op2)
        else:
            continue
        if not problem.is_valid():
            continue
        attempt = StudentAttempt(problem)
        data.append({
            "Problem": str(problem),
            "Answer": attempt.answer,
            "Correct?": attempt.correct,
            "Reason": attempt.reason,
            "Student Steps": attempt.steps,
            "Wrong Step": attempt.wrong_step
        })
        count += 1
    return pd.DataFrame(data)

df = generate_dataset(10, problem_type="arithmetic")
print(df)
