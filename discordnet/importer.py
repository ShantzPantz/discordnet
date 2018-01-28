import importlib
import importlib.util
import ntpath
import os
from pathlib import Path



def path_leaf(path):
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)


def list_plugins():
    plugins = []
    for file in os.listdir('plugins'):
        if file.startswith("_"):
            continue
        elif not file.endswith(".py"):
            continue
        plugins.append(importlib.import_module("plugins."+file.split(".")[0]))
    return plugins

