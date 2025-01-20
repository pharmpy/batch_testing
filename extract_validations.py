from pathlib import Path

from rich.console import Console
from rich.table import Table

test_path = Path("tests")

table = Table(title="All validation tests")
table.add_column("Function", justify="right", style="cyan", no_wrap=True)
table.add_column("Validation", style="magenta")

validations = []
for path in test_path.glob("test_*.py"):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# validate: "):
                validation = line[12:]
                validations.append(validation)

for v in sorted(validations):
    a = v.split(maxsplit=1)
    table.add_row(a[0], a[1])

console = Console()
console.print(table)
