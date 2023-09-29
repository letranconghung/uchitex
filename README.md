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
pip install --editable scripts/
```
<!-- https://click.palletsprojects.com/en/8.1.x/setuptools/ -->
Afterwards, the command `texify` should be available in the terminal!

# Getting started on a clean slate
1. Clear all quarters and courses in `quarters/`, unless you want to keep my notes! It is crucial that you don't delete the folder, unless you want to rename `quarters` into `semesters` then that is fine too, but make sure to find other path variables that depend on that  (e.g. in `scripts/config.py`)
2. Appropriately modify the `WORKSPACE_PATH` in `scripts/config.py`
3. Appropriately modify files in `scripts/templates/` to your liking (with YOUR identifiers!)

# How to use the CLI `texify`
## Overview
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
`-a, --all` | View flag
`-i, --id` | Quarter ID
`--help` | For help

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
`-a, --all` | View flag
`-i, --id` | Course ID
`-q, --quarter` | Quarter ID
`-n, --n` | Number of most recent lectures to be compiled
`--help` | For help

## Lecture commands
All lecture commands are under `texify lecture`

Function | Command
--- | ---
Create new lecture in course | `texify lecture -c math20250`
View all lectures in course | `texify lecture -a -c math20250`
Help | `texify lecture --help`

CLI Parameter | Info
--- | ---
`-a, --all` | View flag
`-c, --course` | Course ID
`--help` | For help

## Problem set commands
All pset commands are under `texify pset`

Function | Command
--- | ---
Create new pset in course | `texify pset -c math20700`
Help | `texify pset --help`

CLI Parameter | Info
--- | ---
`-c, --course` | Course ID
`--help` | For help


