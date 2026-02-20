from setuptools import setup

APP = ['src/virtual_lab_fisika_dasar.py', 'src/virtual_lab_fisika_modern.py']
DATA_FILES = [
    ('', ['config/db_config.json']),
    ('Hasil_Praktikum/Fisika_Dasar', []),
    ('Hasil_Praktikum/Fisika_Modern', []),
    ('src/assets/icons', ['src/assets/icons/logo_dasar.png', 'src/assets/icons/logo_modern.png']),
    ('src/assets/images', [])
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas', 'requests', 'openpyxl', 'matplotlib', 'numpy', 'tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)