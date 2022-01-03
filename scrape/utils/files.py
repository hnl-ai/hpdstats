# -*- coding: utf-8 -*-
"""The files utility module."""

import shutil


def copy_file(src, dst):
    """Copies a file from src to dst."""
    shutil.copyfile(src, dst)


def zip_directory(zip_name, dir_name):
    """Zips up an archive given a directory."""
    shutil.make_archive(zip_name, 'zip', dir_name)
