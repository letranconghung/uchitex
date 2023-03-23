"""
Executes script that initializes all courses in root directorys.
"""
from db import Quarter, DataBase
from config import PREAMBLE_TEMPLATE, MASTER_TEMPLATE, ROOT, COURSE_YAML_TEMPLATE, QUARTER_YAML_TEMPLATE, INTRO_TEMPLATE
from utils import un_template


def new_quarter(q_id):
    """
    Create a new quarter
    """
    if (ROOT / q_id).is_dir():
        return f"Failed: Quarter {q_id} already exists!"

    q_path = ROOT / q_id
    q_path.mkdir()

    (q_path / 'quarter.yaml').touch()
    (ROOT / q_id / 'quarter.yaml').write_text(un_template(QUARTER_YAML_TEMPLATE,
                                                          [('QUARTER_ID', q_id)]))

    (q_path / 'preamble.tex').touch()
    (q_path / 'preamble.tex').write_text(un_template(PREAMBLE_TEMPLATE, []))

    return f"Quarter {q_id} created successfully!"


def new_course(c_id, q_id):
    """
    Create new course in quarter
    """
    if not (ROOT / q_id).is_dir():
        return f"Failed: Quarter {q_id} doesn't exist!"
    if (ROOT / q_id / c_id).is_dir():
        return f"Failed: Course {c_id} already exists in quarter {q_id}!"

    c_path = ROOT / q_id / c_id
    c_path.mkdir()

    (c_path / 'figures').mkdir()
    (c_path / 'figures' / '.gitkeep').touch()

    (c_path / 'course.yaml').touch()
    (c_path / 'course.yaml').write_text(un_template(COURSE_YAML_TEMPLATE,
                                                    [('COURSE_ID', c_id)]))

    (c_path / 'intro.tex').touch()
    (c_path / 'intro.tex').write_text(un_template(INTRO_TEMPLATE, []))

    (c_path / f"master_{c_id}.tex").touch()
    (c_path / f"master_{c_id}.tex").write_text(un_template(MASTER_TEMPLATE, []))

    return f"Success: Course {c_id} created in quarter {q_id}!"


def new_lecture(c_id):
    """
    Add new lecture to course c_id
    """
    db = DataBase()
    if db.get_course(c_id) is None:
        return f"Failed: No course {c_id} found!"

    db.get_course(c_id).add_lecture()
    return f"Success: New lecture added to course {c_id}!"


def new_pset(c_id):
    """
    Add new pset to course c_id
    """
    db = DataBase()
    if db.get_course(c_id) is None:
        return f"Failed: No course {c_id} found!"
    db.get_course(c_id).add_pset()
    return f"Success: New pset added to course {c_id}"


def view_quarters_in_db():
    """
    View quarters in db
    """
    db = DataBase()
    return str(db)


def view_courses_in_db():
    """
    View courses in db
    """
    db = DataBase()
    return '\n'.join(str(q) for q in db.quarters)


def view_courses_in_quarter(q_id):
    """
    View courses in quarter
    """
    db = DataBase()
    if db.get_quarter(q_id) is None:
        return f"Failed: Quarter {q_id} doesn't exist!"

    return str(db.get_quarter(q_id))


def view_lectures_in_course(c_id):
    """
    View lectures in course
    """
    db = DataBase()
    if db.get_course(c_id) is None:
        return f"Failed: Course {c_id} doesn't exist!"

    return str(db.get_course(c_id))


def course_include_recent(c_id, n: str):
    """
    Only include last n lectures in the master file of c_id
    """
    if not n.isdigit():
        return "Failed: Argument n is not an int!"
    db = DataBase()
    if db.get_course(c_id) is None:
        return f"Failed: Course {c_id} doesn't exist!"

    db.get_course(c_id).include_recent(int(n))
    return "Success"
