#!/bin/bash
# -*- coding: utf-8 -*-
from os import listdir, remove, chdir
from os.path import basename, join, isdir, abspath, exists

TARGET_SUFFIX = 'md'
IGNORE_PREFIX = '.'
TEMPLATE_HEAD = '''
# Spring源码阅读笔记
'''
README_PATH = "README.md"
TARGET_DIR = '.'


class Writer(object):
    def __init__(self, out=README_PATH):
        if exists(out):
            remove(out)
        self.handler = open(out, 'w', encoding='utf-8')

    def __enter__(self):
        self.handler.write(TEMPLATE_HEAD)
        self.handler.write('\n')
        return self

    def write(self, line, space="", prefix='- ', parent='.'):
        self.handler.write(f'\n{space}{prefix} [{line}]({join(parent, line)})\n')

    def writeContents(self, contents, space="", parent='.'):
        for content in contents:
            if isinstance(content, str):
                self.write(content, space=space, parent=parent)
            elif isinstance(content, dict):
                for k, v in content.items():
                    self.write(k, space=space)
                    self.writeContents(v, space=space + "    ", parent=join(parent, k))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handler.close()


def dirs(dir_path=TARGET_DIR):
    files = []
    dir_path = abspath(dir_path)
    sub_dirs = listdir(dir_path)
    # print(dir_path, sub_dirs)
    for sub_file in sub_dirs:
        if isIgnore(sub_file):
            continue
        if isdir(sub_file):
            chdir(sub_file)
            sub_dir_list = dirs(join(dir_path, sub_file))
            chdir('..')
            files.append({
                sub_file: sub_dir_list
            })
        elif isTarget(sub_file):
            files.append(sub_file)
    return files


def isIgnore(fileName: str):
    return fileName.startswith(IGNORE_PREFIX)


def isTarget(fileName: str):
    if fileName == README_PATH:
        return False
    return fileName.lower().endswith(TARGET_SUFFIX)


if __name__ == '__main__':
    with Writer() as w:
        w.writeContents(dirs())