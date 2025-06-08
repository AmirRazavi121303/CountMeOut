import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Step 1: Load your data
df = pd.read_csv("/Users/amir/Downloads/CodeAmir/CountMeOut/countmeout_data.csv")

print(df)

# Step 2: Combine steps as one input
X = df["Unnamed: 1"]
y = df["Unnamed: 2"]  # binary target

# Step 3: Convert text to vectors
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Step 4: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2)

# Step 5: Train a simple classifier
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

"""example = vectorizer.transform("Step 1: 2 + 3 = 5. Step 2: 5 * 2 = 12")
print(clf.predict(example))"""
