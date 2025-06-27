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
df = pd.read_csv("/Users/amir/Downloads/CodeAmir/CountMeOut/output_5.csv")

print(df)

#make 800k * 5 matrix with each operator and operand as seperate columns, + answers, + binary student steps

#example matrix for 3 * 2 - 5 = 14, step 1 right, step 2 wrong
#  [3, 2, 2, 3, 5]
#  [0, 1, 0, 1, 0]

def enumerate_operators_and_operands(df):
    vocab = {
        "+" : 0,
        "-" : 1,
        "*" : 2,
        "/" : 3,
    }
    values = []
    items = []
    for problem in df["Problem"]:
        tokens = problem.strip().split()
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
        values.append(row)
        items.append(nums)
    return values, items

def ensure(X, target_shape):
    if X.shape[1] == 0:
        return csr_matrix((X.shape[0], 1))

vec_problems, vec_items = enumerate_operators_and_operands(df)
print(vec_problems[0:3], vec_items[0:3])

X_problem = np.hstack([vec_problems, vec_items])
X_ans = ensure(df["Answer"], (df["Answer"].shape[0], 1))
X_steps = df["Wrong Step"] 
y = df["Correct?"].astype(int) # binary target, add binary target for which step was wrong

X_train_prob, X_test_prob, X_train_ans, X_test_ans, X_train_steps, X_test_steps, y_train, y_test = train_test_split(
    X_problem, X_ans, X_steps, y, test_size=0.2, random_state=42, shuffle=True
)

print(X_train_prob.shape)
print(X_train_ans.shape)
print(X_train_steps.shape)

"""prob_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000, token_pattern=r"(?u)\b[\w\*\+\-/=]+\b")
steps_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
ans_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)

X_train_prob = prob_vectorizer.fit_transform(X_train_prob)
X_train_steps = steps_vectorizer.fit_transform(X_train_steps)
X_train_ans = ans_vectorizer.fit_transform(X_train_ans)

X_test_prob = prob_vectorizer.transform(X_test_prob)
X_test_steps = steps_vectorizer.transform(X_test_steps)
X_test_ans = ans_vectorizer.transform(X_test_ans)"""

X_train_combined = hstack([X_train_prob, X_train_ans, X_train_steps])
X_test_combined = hstack([X_test_prob, X_test_ans, X_test_steps])

reg_model = LogisticRegression(max_iter=1000, class_weight={0: 1.2, 1:1.0}) # output: the probability of a data point falling into a certain class given the variables 
reg_model.fit(X_train_combined, y_train)
y_pred_log = reg_model.predict(X_test_combined)
print("🪵 Logistic Regression Report:")
print(classification_report(y_test, y_pred_log))

rf_model = RandomForestClassifier(n_estimators=50, n_jobs=1, random_state=42, class_weight={0: 1.4, 1:1.0})
rf_model.fit(X_train_combined, y_train)
y_pred_rf = rf_model.predict(X_test_combined)
print("🌳 Random Forest Report:")
print(classification_report(y_test, y_pred_rf))
