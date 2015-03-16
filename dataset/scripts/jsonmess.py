import json

def load(file):
    with open(file) as f:
        for line in f:
            while True:
                try:
                    yield json.loads(line)
                    break
                except ValueError:
                    # Not yet a complete JSON value
                    line += next(f)

