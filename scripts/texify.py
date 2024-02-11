"""
Texify CLI Interface.
"""
import click
from db import Quarter
from config import ROOT
from _texify import (new_quarter, new_course, new_lecture,new_pset,
                     view_quarters_in_db, view_courses_in_db,
                     view_courses_in_quarter, view_lectures_in_course,
                     course_include_recent)

@click.group()
def cli():
    """
    texify cli wrapper.
    """
    return
# Quarter


@click.option('-q', '--quarter', 'q_id',
              help="Quarter ID to create, view all quarters in database")
@click.option('-a', '--all', 'view',
              is_flag=True,
              show_default=True,
              default=False,
              help="View flag")
@cli.command()
def quarter(q_id, view):
    """
    Create new quarter, view all quarters
    """
    if view:
        print(view_quarters_in_db())
        return
    if q_id is not None:
        print(new_quarter(q_id))
    else:
        print("Failed: No id provided")
    return

# Course


@click.option('-c', '--course', 'c_id',
              help="Course ID to create, view, render")
@click.option('-q', '--quarter', 'q_id',
              help="Quarter ID to create, view courses in quarter")
@click.option('-a', '--all', 'view',
              is_flag=True,
              show_default=True,
              default=False,
              help="View flag")
@click.option('-n', '--n', 'n',
              help="Number of most recent lectures to be included in the render")
@cli.command()
def course(c_id, q_id, view, n):
    """
    Create new course in quarter, view all courses, render most recent lectures.
    """
    if n:
        if c_id is not None:
            print(course_include_recent(c_id, n))
        else:
            print("Failed: No id provided to compile")
        return
    if view:
        if q_id is not None:
            print(view_courses_in_quarter(q_id))
        else:
            print(view_courses_in_db())
        return
    if c_id is not None:
        if q_id is not None:
            print(new_course(c_id, q_id))
        else:
            print("Failed: No quarter provided")
    else:
        print("Failed: No id provided")

# Lecture


@click.option('-c', '--course', 'c_id',
              help="Course ID to create, view all lectures in course")
@click.option('-a', '--all', 'view',
              is_flag=True,
              show_default=True,
              default=False,
              help="View flag")
@cli.command()
def lecture(c_id, view):
    """
    Create new lecture in course, view all lectures in course
    """
    if view:
        if c_id is None:
            print("Failed: No course provided!")
        else:
            print(view_lectures_in_course(c_id))
        return
    if c_id is not None:
        print(new_lecture(c_id))
    else:
        print("Failed: No course provided!")

@click.option('-c', '--course', 'c_id',
              help="Course ID to create pset in course")
@cli.command()
def pset(c_id):
    """
    Create new pset in course
    """
    if c_id is not None:
        print(new_pset(c_id))
    else:
        print("Failed: No course provided!")
