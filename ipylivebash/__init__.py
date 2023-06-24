#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Ben lau.
# Distributed under the terms of the Modified BSD License.

from .logview import LogView  # noqa
from ._version import __version__  # noqa
from IPython.core.magic import register_cell_magic
from .session_manager import run_script  # noqa
from .runner import Runner


def _jupyter_labextension_paths():
    """Called by Jupyter Lab Server to detect if it is a valid labextension and
    to install the widget
    Returns
    =======
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Lab copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Lab copies
        from `src` directory into <jupyter path>/labextensions/<dest> directory
        during widget installation
    """
    return [
        {
            "src": "labextension",
            "dest": "ipylivebash",
        }
    ]


def _jupyter_nbextension_paths():
    """Called by Jupyter Notebook Server to detect if it is a valid nbextension and
    to install the widget
    Returns
    =======
    section: The section of the Jupyter Notebook Server to change.
        Must be 'notebook' for widget extensions
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Notebook copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Notebook copies
        from `src` directory into <jupyter path>/nbextensions/<dest> directory
        during widget installation
    require: Path to importable AMD Javascript module inside the
        <jupyter path>/nbextensions/<dest> directory
    """
    return [
        {
            "section": "notebook",
            "src": "nbextension",
            "dest": "ipylivebash",
            "require": "ipylivebash/extension",
        }
    ]


def in_notebook():
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True


if in_notebook():

    @register_cell_magic
    def livebash(line, cell):
        runner = Runner(line.split() if line else "")
        if runner.args.print_help:
            runner.parser.print_help()
            return
        runner.run(cell)
