import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_FOLDER = 'templates'
PAGE_BASE = 'base.html'


env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

base_template = env.get_template(PAGE_BASE)


level_definitions = {
    0: "ChapterIndex",
    1: "ChapterSection",
    2: "ChapterSubsection",
    3: "CompoundArticle",
    4: "SingleArticle"
}


class Chapter:

    def __init__(self, text, soup_index):
        self.text = text
        self.soup_index = soup_index


class TOCEntry:

    def __init__(self, level, soup_index, element):
        self.level = level
        self.soup_index = soup_index
        self.element = element
        self.raw_text = element.text
        self.text = element.text.split("\t")[0]
        self.content_link = None


class TOCLinkItem:

    def __init__(
            self, element, soup_index, ms_word_index, text, contents=None):
        self.element = element
        self.soup_index = soup_index
        self.ms_word_index = ms_word_index
        self.text = text
        self.contents = contents
        self.linked_entry = None


class ContentItem:

    def __init__(
            self, title, level, soup_index=None, parent=None, contents=None,
            next_item=None, prev_item=None):
        self.level = level
        self.title = title
        self.soup_index = soup_index
        self.parent = parent
        self.contents = contents
        self.next = next_item
        self.prev = prev_item
        self.children = []

    def __repr__(self):
        return 'ContentItem("{title}")'.format(**vars(self))
