"""
Utils module.
"""
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
def get_week(d=datetime.today()):
    """
    Returns week of date.
    """
    return int(d.strftime("%W"))

def un_template(f: Path, rplc: List[Tuple[str, str]], dlmtr: str = "\n"):
    """
    Replace placeholders in template file with specifics.
    """
    lines = f.read_text(encoding='utf-8').split('\n')
    res = []
    for line in lines:
        for (a, b) in rplc:
            line = line.replace(a, b)
        res.append(line)
    return dlmtr.join(res)
            
    