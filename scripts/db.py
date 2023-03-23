"""
Module for Lecture and Lecutres
"""
from datetime import datetime
from pathlib import Path
from typing import List
import locale
import re
import subprocess
import yaml
from config import ROOT, DATE_FORMAT, PSET_TEMPLATE
from utils import get_week, un_template
locale.setlocale(locale.LC_ALL, "en_US")


def lecnumber_to_filename(lecnumber: int):
    """
    Converts lecture number to corresponding tex file name.
    """
    return f'lec_{lecnumber:02}.tex'


def psetnumber_to_filename(psetnumber: int):
    """
    Converts pset number to corresponding tex file name.
    """
    return f'pset_{psetnumber:02}.tex'


def filename_to_number(filename: str):
    """
    Converts tex file name to lecture number.
    """
    return int(str(filename).replace('.tex', '').replace('lec_', '').replace('pset_', ''))


class Lecture:
    """
    Represents data of 1 Lecture
    """

    def __init__(self, l_path: Path):
        """
        Initializes the Lecture instance.
        Extracts meta-data from file at l_path.
        """
        with l_path.open() as f:
            for line in f:
                lecture_match = re.search(
                    r'lecture\{(.*?)\}\{(.*?)\}\{(.*)\}', line)
                if lecture_match:
                    break

        # number = int(lecture_match.group(1))
        date_str = lecture_match.group(2)
        self.l_path = l_path
        self.date = datetime.strptime(date_str, DATE_FORMAT)
        self.week = get_week(self.date)
        self.number = filename_to_number(l_path.stem)
        self.l_title = lecture_match.group(3)

    def __str__(self):
        return f"Lecture {self.number} (Week {self.week}, {self.date}): {self.l_title}"


class Course:
    """
    Represent a course in the folder

    c_path (Path): path of course folder
    c_id (str): id of course
    info ('title': str, 'id': str): Title and short name of course
    _lectures (Optional(Lectures)): Lectures object of course
    """

    def __init__(self, c_path: Path):
        self.c_path = c_path
        self.info = yaml.safe_load((c_path / 'course.yaml').open())
        self.c_title = self.info['title']
        self.c_id = self.info['id']
        self.lectures = self._init_lectures()
        self.psets = self._init_psets()
        self.master_file_path = self.c_path / f'master_{self.c_id}.tex'

    def _init_lectures(self):
        """
        Read in lectures under course path.
        """
        l_paths = self.c_path.glob('lec_*.tex')
        return sorted((Lecture(l_path) for l_path in l_paths), key=lambda l: l.number)

    def _init_psets(self):
        """
        Read in psets under course path
        """
        p_paths = self.c_path.glob('pset_*.tex')
        return sorted([filename_to_number(p_path.stem) for p_path in p_paths])

    def __str__(self):
        return f"Course {self.c_title} ({self.c_id}): {len(self.lectures)} lecture(s)\n"+"\t".join([str(l) for l in self.lectures])

    def add_lecture(self) -> Lecture:
        """
        Creates a new lecture
        """
        if len(self.lectures) != 0:
            new_l_number = self.lectures[-1].number + 1
        else:
            new_l_number = 1

        new_l_path = self.c_path / \
            lecnumber_to_filename(new_l_number)

        today = datetime.today()
        date = today.strftime(DATE_FORMAT)

        new_l_path.touch()
        new_l_path.write_text(
            f'\\lecture{{{new_l_number}}}{{{date}}}{{}}\n')

        self.lectures = self._init_lectures()

        if new_l_number == 1:
            self.include_recent(1)
        else:
            # only include the last 2 lectures in master file
            self.include_recent(2)

    def add_pset(self):
        """
        Creates a new pset
        """
        if len(self.psets) != 0:
            new_p_number = self.psets[-1] + 1
        else:
            new_p_number = 1
        new_p_path = self.c_path / psetnumber_to_filename(new_p_number)

        today = datetime.today()
        date = today.strftime(DATE_FORMAT)

        new_p_path.touch()
        new_p_path.write_text(un_template(PSET_TEMPLATE, [(
            'PSET_NUMBER', str(new_p_number)), ('COURSE_TITLE', self.c_title), ("DATE", str(date))]))

    def _parse_range(self, n):
        """
        Parse numerical range
        """
        all_lec_numbers = [lecture.number for lecture in self.lectures]
        if n == -1 or n == 0:
            return all_lec_numbers
        n = min(len(all_lec_numbers), max(n, 1))
        return range(len(all_lec_numbers) - n + 1, len(all_lec_numbers)+1)

    def _update_master(self, inclued_l_numbers: List[int]) -> None:
        """
        Updates master file to only contain lectures
        in a list of specified lecture numbers.
        Attaches existing header and footer.
        """
        header, footer = self.get_header_footer(self.master_file_path)
        body = ''.join(
            [(' ' * 4
             + r'\input{'
             + lecnumber_to_filename(number)
             + '}\n')
             for number in inclued_l_numbers])
        self.master_file_path.write_text(header + body + footer)

    def include_recent(self, n):
        """
        Updates master to only include last n lectures
        """
        r = self._parse_range(n)
        self._update_master(r)

    @staticmethod
    def get_header_footer(filepath):
        """
        Retrieve the header and footer at filepath, as separated by
        [header]
        start lectures
        [body]
        end lectures
        [footer]
        """
        part = 0
        header = ''
        footer = ''
        with filepath.open() as f:
            for line in f:
                # order of if-statements is important here!
                if 'end lectures' in line:
                    part = 2

                if part == 0:
                    header += line
                if part == 2:
                    footer += line

                if 'start lectures' in line:
                    part = 1
        return (header, footer)

    # def compile_master(self):
    #     """
    #     Runs script to compile the master file.
    #     """

    #     result = subprocess.run(
    #         ['pdflatex', str(self.master_file_path)],
    #         stdout=subprocess.DEVNULL,
    #         stderr=subprocess.DEVNULL,
    #         cwd=str(self.c_path),
    #         check=True
    #     )
    #     return result.returncode


class Quarter():
    """
    List of courses contained in ROOT
    """

    def __init__(self, q_path):
        self.q_path = q_path
        self.courses = self._init_courses()
        self.info = yaml.safe_load((q_path/'quarter.yaml').open())
        self.q_name = self.info['name']
        self.q_id = self.info['id']

    def _init_courses(self):
        """
        Goes through the course directories in quarter folder.
        Generates a sorted list of Course objects.
        """
        crs = [Course(path) for path in self.q_path.iterdir() if path.is_dir()]
        return sorted(crs, key=lambda c: c.c_id)

    def get_course(self, course_name: str):
        """
        Get course based on course name.
        """
        return next(filter(lambda c: c.c_id == course_name, self.courses), None)

    def __str__(self):
        return f"Quarter {self.q_name} ({self.q_id}):\n\t" + "\n\t".join([f"{c.c_title} ({c.c_id})" for c in self.courses])


class DataBase():
    """
    All quarters
    """

    def __init__(self, db_path: Path = ROOT):
        self.db_path = db_path
        self.quarters = self._init_quarters()

    def _init_quarters(self) -> List[Quarter]:
        """
        Goes through the quarter directories in ROOT folder.
        Generates a sorted list of Quarter objects
        """
        quarters = [Quarter(path)
                    for path in self.db_path.iterdir() if path.is_dir()]
        return sorted(quarters, key=lambda q: q.q_id)

    def __str__(self):
        return "Quarters in Database: " + ", ".join([f"{q.q_name} ({q.q_id})" for q in self.quarters])

    def get_quarter(self, q_id):
        """
        Get quarter with q_id
        """
        return next(filter(lambda q: q.q_id == q_id, self.quarters), None)

    def get_course(self, c_id):
        """
        Goes through quarters to find matching course c_id.
        Returns first match.
        """
        for q in self.quarters:
            if q.get_course(c_id) is not None:
                return q.get_course(c_id)
        return None
