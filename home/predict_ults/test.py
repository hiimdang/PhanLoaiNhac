import pickle

with open('history.pkl', 'rb') as f:
    history = pickle.load(f)

print(history)
