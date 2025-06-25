import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from scipy.sparse import hstack

# Step 1: Load your data
df = pd.read_csv("/Users/amir/Downloads/CodeAmir/CountMeOut/output_6.csv")

print(df)

X_problem = df["Problem"] + "|" + df["Student Steps"] + "|" + df["Answer"].astype(str)
#X_steps = df["Student Steps"] 
y = df["Correct?"].astype(int)  # binary target

X_train_prob, X_test_prob, y_train, y_test = train_test_split(X_problem, y, test_size=0.2, random_state=42, shuffle=True)

prob_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000, token_pattern=r"(?u)\b[\w\*\+\-/=]+\b")
#steps_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
#ans_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000, stop_words="english")

X_train_prob = prob_vectorizer.fit_transform(X_train_prob)
#X_train_steps = steps_vectorizer.fit_transform(X_train_steps)
#X_train_ans = ans_vectorizer.fit_transform(X_train_ans)

X_test_prob = prob_vectorizer.transform(X_test_prob)
#X_test_steps = steps_vectorizer.transform(X_test_steps)
#X_test_ans = ans_vectorizer.transform(X_test_ans)

X_train_combined = hstack([X_train_prob])
X_test_combined = hstack([X_test_prob])

reg_model = LogisticRegression(max_iter=1000, class_weight={0: 1.2, 1:1.0}) # output: the probability of a data point falling into a certain class given the variables 
reg_model.fit(X_train_combined, y_train)
y_pred_log = reg_model.predict(X_test_combined)
print("🪵 Logistic Regression Report:")
print(classification_report(y_test, y_pred_log))

"""rf_model = RandomForestClassifier(n_estimators=50, n_jobs=1, random_state=42, class_weight={0: 1.4, 1:1.0})
rf_model.fit(X_train_combined, y_train)
y_pred_rf = rf_model.predict(X_test_combined)
print("🌳 Random Forest Report:")
print(classification_report(y_test, y_pred_rf))"""
