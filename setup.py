from setuptools import setup


APP = ['virtual_lab_fisika_dasar.py', 'virtual_lab_fisika_modern.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'matplotlib', 'numpy', 'requests', 'pandas', 'openpyxl'],
    'iconfile': None,
}



setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
