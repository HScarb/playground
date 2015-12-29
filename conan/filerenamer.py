#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  conan
# @author   dectinc@icloud.com
# @date     2015-12-29 00:13

import os
import re
from os import rename
from os.path import splitext, join

SUPPORT_EXTS = ('mp4', 'mkv', 'rmvb')


def load_episode_list():
    f = open('episode_list', 'rb')
    _lines = f.readlines()

    def clean_line(_l):
        if not _l:
            return ''
        assert isinstance(_l, str)
        _l = _l.strip()
        # rough replacement, decode/encode is preferred
        _l = _l.replace('　', '')
        return _l

    _lines = [clean_line(_line) for _line in _lines]
    episodes = {}
    for _line in _lines:
        _idx = _line.find(' ')
        if _idx < 0:
            continue
        _pre = _line[:_idx]
        if str.isdigit(_pre):
            _pre = int(_pre)
            if _pre < 1000 and _pre > 0:
                episodes[_pre] = _line
    f.close()
    return episodes


def handle_directory(_dir):
    _files = os.listdir(_dir)
    for _file in _files:
        _filename, _ext = splitext(_file)
        if _ext[1:] not in SUPPORT_EXTS:
            continue
        p = re.compile('(?<=[^0-9])\d{3}(?=[^0-9])')
        m = p.search(_filename)
        if not m:
            continue
        _new_file = emap[int(m.group())] + _ext
        print 'renaming %s to %s' % (_file, _new_file)
        rename(join(_dir, _file), join(_dir, _new_file))


if __name__ == '__main__':
    emap = load_episode_list()
    handle_directory('/Users/Dectinc/Movies/series/CONAN/2014年（724-762）')
    handle_directory('/Users/Dectinc/Movies/series/CONAN/2015年（763-803）')
