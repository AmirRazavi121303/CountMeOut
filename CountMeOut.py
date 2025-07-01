import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from scipy.sparse import hstack
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np

# Step 1: Load your data
df = pd.read_csv("/Users/amir/Downloads/CodeAmir/CountMeOut/output_6.csv")

print(df)

#make 800k * 5 matrix with each operator and operand as seperate columns, + answers, + binary student steps

#example matrix for 3 * 2 - 5 = 14, step 1 right, step 2 wrong
#  [3, 2, 2, 3, 5]
#  [0, 1, 0, 1, 0]

def enumerate_operators_and_operands(series, max_len=10):
    vocab = {
        "+" : 0,
        "-" : 1,
        "*" : 2,
        "/" : 3,
    }
    values = []
    items = []
    for expr in series:
        tokens = expr.strip().split()
        row = []
        nums = []
        for token in tokens:
            if token in vocab:
                row.append(vocab[token])
                nums.append(0)
            else:
                try:
                    row.append(int(token))
                    nums.append(1)
                except ValueError:
                    pass  # skip tokens that are neither operator nor integer
        
        # Pad or truncate to max_len
        if len(row) < max_len:
            pad_len = max_len - len(row)
            row.extend([-1] * pad_len)   # pad value -1 (can be changed)
            nums.extend([-1] * pad_len)
        else:
            row = row[:max_len]
            nums = nums[:max_len]
        
        values.append(row)
        items.append(nums)
    return np.array(values), np.array(items)
# Usage:
vec_problems, vec_items = enumerate_operators_and_operands(df["Problem"], max_len=10)
vec_steps, vec_steps_items = enumerate_operators_and_operands(df["Student Steps"], max_len=10)

df["Reason_filled"] = df["Reason"].fillna("No Error")

reason_to_code = {reason: idx for idx, reason in enumerate(df["Reason_filled"].unique())}

X_problem = np.hstack([vec_problems, vec_items, df["Answer"].to_numpy().reshape(-1,1), vec_steps, vec_steps_items, df["Wrong Step"].to_numpy().reshape(-1,1)]) 

y = df["Reason_filled"].map(reason_to_code).astype(int)

X_train_prob, X_test_prob, y_train, y_test = train_test_split(
    X_problem, y, test_size=0.2, random_state=42, shuffle=True
)

"""y_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)

y_train_vec = y_vectorizer.fit_transform(y_train)
y_test_vec = y_vectorizer.transform(y_test)

prob_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000, token_pattern=r"(?u)\b[\w\*\+\-/=]+\b")
steps_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
ans_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)

X_train_prob = prob_vectorizer.fit_transform(X_train_prob)
X_train_steps = steps_vectorizer.fit_transform(X_train_steps)
X_train_ans = ans_vectorizer.fit_transform(X_train_ans)

X_test_prob = prob_vectorizer.transform(X_test_prob)
X_test_steps = steps_vectorizer.transform(X_test_steps)
X_test_ans = ans_vectorizer.transform(X_test_ans)

X_train_combined = hstack([X_train_prob, X_train_steps])
X_test_combined = hstack([X_test_prob, X_test_steps])

reg_model = LogisticRegression(max_iter=1000, class_weight={0: 1.2, 1:1.0}) # output: the probability of a data point falling into a certain class given the variables 
reg_model.fit(X_train_prob, y_train)
y_pred_log = reg_model.predict(X_test_prob)
print("🪵 Logistic Regression Report:")
print(classification_report(y_test, y_pred_log))"""

rf_model = RandomForestClassifier(n_estimators=50, n_jobs=1, random_state=42)
rf_model.fit(X_train_prob, y_train)
y_pred_rf = rf_model.predict(X_test_prob)
print("🌳 Random Forest Report:")
print(classification_report(y_test, y_pred_rf))
print("Good Job!")
