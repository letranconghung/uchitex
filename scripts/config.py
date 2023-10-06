"""
User config
"""
from pathlib import Path

DATE_FORMAT = '%d %b %Y'
TEX_WORKSPACE = Path('/Users/hung/Desktop/macmaindata/tex/uchitex/')
ROOT =  TEX_WORKSPACE / 'quarters'
TEMPLATES_PATH = TEX_WORKSPACE / 'scripts' / 'templates'
MASTER_TEMPLATE = TEMPLATES_PATH / 'master.tex'
PREAMBLE_TEMPLATE = TEMPLATES_PATH / 'preamble.tex'
INTRO_TEMPLATE = TEMPLATES_PATH / 'intro.tex'
PSET_TEMPLATE = TEMPLATES_PATH / 'pset.tex'
COURSE_YAML_TEMPLATE = TEMPLATES_PATH / 'course.yaml'
QUARTER_YAML_TEMPLATE = TEMPLATES_PATH / 'quarter.yaml'
