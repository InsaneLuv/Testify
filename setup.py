import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['gallery.pro', 'app/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI"
)

# SETUP CX FREEZE
setup(
    name="Testify",
    version="1.1",
    description="Курсовая работа",
    author="Молитвин данила",
    options={'build_exe': {'include_files': files}},
    executables=[target]

)
