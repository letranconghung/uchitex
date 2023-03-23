# Set up
- Virtual environment and set up necessary packages
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
- If needed, deactivate the virtual environment
```
deactivate
```
- Install the `texify` command
```
pip install --editable .
```
<!-- https://click.palletsprojects.com/en/8.1.x/setuptools/ -->
Afterwards, the command `texify` should be available in the terminal!

# `texify`
Uses:
- `texify quarter ...`
- `texify course ...`
- `texify lecture ...`
## Quarter commands
All quarter commands are under `texify quarter`
Function | Command
--- | ---
Create a new quarter in ROOT | `texify quarter -i 03s23`
View all quarters | `texify quarter -a`
Help | `texify quarter --help`

CLI Parameter | Info
--- | ---
-a, --all | View flag
-i, --id | Quarter ID
--help | For help

## Course commands
All course commands are under `texify course`

Function | Command
--- | ---
Create new course in quarter | `texify course -i math20250 -q 03s23`
View all courses | `texify course -a`
View all courses in quarter | `texify course -a -q 03s23`
Only include recent lectures | `texify course -i math20250 -n 3`
Help | `texify course --help`

CLI Parameter | Info
--- | ---
-a, --all | View flag
-i, --id | Course ID
-q, --quarter | Quarter ID
-n, --n | Number of most recent lectures to be compiled
--help | For help

## Lecture commands
All lecture commands are under `texify lecture`

Function | Command
--- | ---
Create new lecture in course | `texify lecture -c math20250`
View all lectures in course | `texify lecture -a -c math20250`
Help | `texify lecture --help`

CLI Parameter | Info
--- | ---
-a, --all | View flag
-c, --course | Course ID
--help | For help

