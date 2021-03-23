# Install (PowerShell/Bash)

```bash
git clone https://github.com/keyansheng/todo-app
cd todo-app
echo '#!/bin/bash
prettier --check .
black --check .' > .git/hooks/pre-commit
pip install -r requirements.txt
cp db-default.sqlite3 db.sqlite3
mkdir images
```

# Run

1. Run `todo.py`
1. Open your browser and go to the address shown in the terminal, e.g. `http://127.0.0.1:5000/`

# Optional settings

| Setting    | File                    | Location        | Default values       |
| ---------- | ----------------------- | --------------- | -------------------- |
| Categories | `db.sqlite3`            | `Category.Name` | `School`, `Personal` |
| Time zone  | `timezone_converter.py` | line 6          | `"Asia/Singapore"`   |
