# Install

```bash
git clone https://github.com/keyansheng/todo-app
cp todo-default.db todo.db
mkdir images
```

# Run

1. Run `todo.py`
1. Open your browser and go to the address shown in the terminal, e.g. `http://127.0.0.1:5000/`

# Optional settings

| Setting    | File                    | Location        | Default values       |
| ---------- | ----------------------- | --------------- | -------------------- |
| Categories | `todo.db`               | `Category.Name` | `School`, `Personal` |
| Time zone  | `timezone_converter.py` | line 6          | `"Asia/Singapore"`   |
