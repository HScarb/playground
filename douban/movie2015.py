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
        s = '[%s](%s)' % (self.name, self.url)
        if self.rate:
            s += ' - %s' % self.rate
        return s


class Dialogue(object):
    def __init__(self, name, url, dialogue):
        self.name = name
        self.url = url
        self.dialogue = dialogue

    def __str__(self):
        return '[%s](%s) : %s' % (self.name, self.url, self.dialogue)


def search(_content, _pattern):
    p = re.compile(_pattern)
    m = p.search(_content)
    return m.group() if m else ''


def load_source(_url='http://movie.douban.com/annual2015'):
    import requests
    response = requests.get(_url)
    print 'Response code: %d' % response.status_code
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
    print 'Number sections: %d' % len(sections)
    movie_sections = []
    movie_map = {}
    dialogues = []
    for section in sections:
        section_type = get_section_type(section)
        if section_type == 'top-10-widget':
            title, movies = parse_top_10_widget(section)
            if title not in movie_map:
                movie_sections.append(title)
                movie_map[title] = movies
            else:
                movie_map[title] = movie_map[title] + movies
        elif section_type == 'dialogue-widget':
            dialogue = parse_dialog_widget(section)
            dialogues.append(dialogue)
        else:
            pass
    return movie_sections, movie_map, dialogues


def get_section_type(section):
    p_section_type = re.compile(r'(?<=<div class="section )[a-z0-9-]+')
    section_type = p_section_type.search(section)
    return section_type.group()


def parse_top_10_widget(_content):
    top_title = search(_content, r'(?<=<div class="top-title">).*?(?=</div>)')
    bottom_title = search(_content,
                          r'(?<=<div class="bottom-title">).*?(?=</div>)')
    print top_title + bottom_title
    p_subject_wrapper = re.compile(
            r'<div class="subjects-wrapper clearfix">.*?<div class="barrage')
    subject_wrapper = p_subject_wrapper.search(_content).group()
    p_item = re.compile(r'<a target="_blank".*?</div></div>')
    items = p_item.findall(subject_wrapper)

    def parse_item(_src):
        url_ = search(_src, r'(?<=<a target="_blank" href=").*?(?=")')
        name_ = search(_src, r'(?<=data-title=").*?(?=">)')
        rate_ = search(_src, r'(?<=<p>)[\d\.]+?(?=</p>)')
        return Movie(name_, url_, rate_)

    movies = []
    for item in items:
        movie_ = parse_item(item)
        movies.append(movie_)
        print str(movie_)
    print ''
    return top_title + bottom_title, movies


def parse_dialog_widget(_content):
    url_ = search(_content,
                  r'(?<=class="subject-meta"><a target="_blank" href=").*?(?=" class="title">)')
    name_ = search(_content, r'(?<=" class="title">).*?(?=[</a>|\\(])')
    dialogue_ = search(_content, r'(?<=<div class="text ">).*?(?=</div>)')
    if not dialogue_:
        dialogue_ = search(_content, r'(?<=<div class="text min">).*?(?=</div>)')
    return Dialogue(name_, url_, dialogue_)


def save_annual_list(_movie_file='douban_movie_annual_2015',
                     _dialogue_file='douban_movie_annual_2015_dialogues'):
    mf = open(_movie_file, 'wb')
    print movie_sections
    for title in movie_sections:
        mf.write(title)
        mf.write('\n')
        count = 1
        for movie_ in movie_map[title]:
            mf.write('%2d. ' % count)
            count += 1
            mf.write(str(movie_))
            mf.write('\n')
        mf.write('\n')
    mf.close()
    df = open(_dialogue_file, 'wb')
    count = 1
    for dialogue_ in dialogues:
        df.write('%2d. ' % count)
        count += 1
        df.write(str(dialogue_))
        df.write('\n')
    df.write('\n')
    df.close()


if __name__ == '__main__':
    page_content = load_source()
    page_content = page_content.replace('\r\n', ' ')
    page_content = page_content.replace('\n', ' ')
    page_content = re.sub(r'>\s+<', '><', page_content)
    movie_sections, movie_map, dialogues = get_section()
    save_annual_list()
