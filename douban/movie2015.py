#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @filename  movie2015
# @author   dectinc@icloud.com
# @date     2015-12-29 13:12

import re
import lxml.etree as le
import cStringIO


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
    if response.status_code == 200:
        return response.content
    else:
        return ''


def get_section():
    doc = le.parse(page_content)
    section_path = '//*[@id="main"]/div[contains(@class, "section")]'
    sections = doc.xpath(section_path)
    print(map(le.tostring, sections))


def parse_top_10_widget(_content):
    pass


def parse_dialog_widget(_content):
    pass


def print_list(_file='douban_movie_annual_2015'):
    f = open(_file, 'wb')
    f.close()


if __name__ == '__main__':
    page_content = load_source()
    list_ = get_section()
    print_list()
