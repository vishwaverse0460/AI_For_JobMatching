import numpy as np
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Generate synthetic training data
def generate_training_data(n=10000):
    X = []
    y = []
    for _ in range(n):
        skill = random.choice([np.random.uniform(0.7, 1.0), np.random.uniform(0.4, 0.7), np.random.uniform(0.0, 0.4)])
        exp = random.choice([np.random.uniform(0.7, 1.0), np.random.uniform(0.3, 0.7), np.random.uniform(0.0, 0.3)])
        qual = random.choice([1.0, 0.7, 0.3])
        
        # Scoring logic
        score = (0.5 * skill) + (0.3 * exp) + (0.2 * qual)
        
        # Add noise
        noise = np.random.normal(0, 0.03)
        score = max(0, min(1, score + noise))
        
        X.append([skill, exp, qual])
        y.append(score)
    return np.array(X), np.array(y)

# 2. Prepare Data
X_all, y_all = generate_training_data()

X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)

# 3. Train Model
model_ml = RandomForestRegressor(n_estimators=100, random_state=42)
model_ml.fit(X_train, y_train)


y_pred = model_ml.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"--- Model Performance ---")
print(f"R-squared Score (Accuracy): {r2 * 100:.2f}%")
print(f"Mean Absolute Error: {mae:.4f}")

#Final Prediction function
def predict_score(skill_score, exp_score, qual_score):
    return float(model_ml.predict([[skill_score, exp_score, qual_score]])[0])

# Test run
print(f"\nTest Prediction (High Skills/Exp): {predict_score(0.9, 0.8, 1.0):.4f}")
