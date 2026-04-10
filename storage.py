import json
import os

def load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    f = open(filepath, "r")
    try:
        info = json.load(f)
        f.close()
        return info
    except:
        f.close()
        return default

def save_json(filepath, data):
    folder = os.path.dirname(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)
    f = open(filepath, "w")
    json.dump(data, f, indent=4)
    f.close()
