import numpy as np
import random
from sklearn.ensemble import RandomForestRegressor

# Generate synthetic training data
def generate_training_data(n=500):
    X = []
    y = []

    for _ in range(n):

        # realistic skill similarity
        skill = random.choice([
            np.random.uniform(0.7, 1.0),   # strong match
            np.random.uniform(0.4, 0.7),   # medium
            np.random.uniform(0.0, 0.4)    # weak
        ])

        # realistic experience match
        exp = random.choice([
            np.random.uniform(0.7, 1.0),   # meets/exceeds
            np.random.uniform(0.3, 0.7),   # slightly less
            np.random.uniform(0.0, 0.3)    # poor
        ])

        # realistic qualification match
        qual = random.choice([
            1.0,    # exact match
            0.7,    # related degree
            0.3     # mismatch
        ])

        # 🎯 REALISTIC SCORING LOGIC
        score = (0.5 * skill) + (0.3 * exp) + (0.2 * qual)

        # add slight noise (real-world uncertainty)
        noise = np.random.normal(0, 0.03)
        score = max(0, min(1, score + noise))

        X.append([skill, exp, qual])
        y.append(score)

    return np.array(X), np.array(y)


# Train model
X, y = generate_training_data()

model_ml = RandomForestRegressor()
model_ml.fit(X, y)


# Prediction function (IMPORTANT)
def predict_score(skill_score, exp_score, qual_score):
    return float(model_ml.predict([[skill_score, exp_score, qual_score]])[0])