## Required libraries

### Python Standard Library

- os
- sqlite3
- datetime

### Additional

- flask
- werkzeug
- pytz

## Setup

1. Clone this repo
1. Copy `todo - default.db` from the `default` folder to the root directory and rename it as `todo.db`
1. Create a folder `images` in the root directory

### Optional settings

| Setting    | File                    | Location           | Default values       |
| ---------- | ----------------------- | ------------------ | -------------------- |
| Categories | `todo.db`               | `Category`>`Name`  | `School`, `Personal` |
| Time zone  | `timezone_converter.py` | `END = timezone()` | `"Asia/Singapore"`   |

## Usage

1. Run `todo.py`
1. Open your browser and go to the address shown in the terminal, e.g. `http://127.0.0.1:5000/`
