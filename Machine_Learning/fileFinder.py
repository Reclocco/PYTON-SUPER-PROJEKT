import os
from pathlib import Path


def findFile(name, ext):
    src = os.getcwd()
    file = ''
    for path in Path(src).parent.rglob("*." + ext):
        if name in str(path):
            file = path
    return file
