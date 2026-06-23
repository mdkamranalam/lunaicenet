import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_and_predict_ice(cpr, dop, slope):
    """
    Train a simple RF on synthetic heuristic labels and predict.
    For the MVP, we create a proxy rule to train the model on the fly.
    """
    # Flatten arrays
    X = np.column_stack([cpr.ravel(), dop.ravel(), slope.ravel()])
    
    # Proxy Rules to generate pseudo-labels for training
    # Rule: Ice is CPR > 1.2, DOP < 0.4, Slope < 10
    labels = np.zeros(len(X))
    
    is_ice = (X[:, 0] > 1.2) & (X[:, 1] < 0.4) & (X[:, 2] < 10)
    labels[is_ice] = 1
    
    # Add some noise to labels so the RF actually has to learn
    flip_mask = np.random.choice([True, False], size=len(labels), p=[0.05, 0.95])
    labels[flip_mask] = 1 - labels[flip_mask]
    
    # Train
    clf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    clf.fit(X, labels)
    
    # Predict probability
    prob = clf.predict_proba(X)[:, 1]
    return prob.reshape(cpr.shape)
