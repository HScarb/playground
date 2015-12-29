#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  movie2015
# @author   dectinc@icloud.com
# @date     2015-12-29 13:12

import re


class Movie(object):
    def __init__(self, name, url, rate):
        self.name = name
        self.url = url
        self.rate = rate

    def __str__(self):
        return '[%s](%s) - %.1f' % (self.name, self.url, self.rate)


def load_source(_url='http://movie.douban.com/annual2015'):
    import requests
    response = requests.get(_url)
    print response.status_code
    if response.status_code == 200:
        return response.content
    else:
        f = open('source', 'rb')
        content = ''.join(f.readlines())
        f.close()
        return content


def get_section():
    p_section = re.compile(
            r'<div class="section .*?<div class="barrage-form-section">')
    sections = p_section.findall(page_content)
    print len(sections)
    for section in sections:
        section_type = get_section_type(section)
        if section_type == 'top-10-widget':
            parse_top_10_widget(section)
        elif section_type == 'dialogue-widget':
            parse_dialog_widget(section_type)
        else:
            pass


def get_section_type(section):
    p_section_type = re.compile(r'(?<=<div class="section )[a-z0-9-]+')
    section_type = p_section_type.search(section)
    return section_type.group()


def parse_top_10_widget(_content):
    pass


def parse_dialog_widget(_content):
    pass


def print_list(_file='douban_movie_annual_2015'):
    f = open(_file, 'wb')
    f.close()


if __name__ == '__main__':
    page_content = load_source()
    page_content = page_content.replace('\r\n', ' ')
    page_content = page_content.replace('\n', ' ')
    list_ = get_section()
    print_list()
