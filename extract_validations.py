from pathlib import Path

test_path = Path("tests")

for path in test_path.glob("test_*.py"):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# validate: "):
                validation = line[12:]
                print("*", validation)
