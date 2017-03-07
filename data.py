import os
from slugify import slugify
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_FOLDER = 'templates'
PAGE_BASE = 'base.jinja'
OUTPUT_DIR = 'output'

env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

base_template = env.get_template(PAGE_BASE)

global_context = dict()


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
    template = "base.jinja"

    def __init__(
            self, title, level, soup_index=None, parent=None, contents=None,
            next_item=None, prev_item=None):
        self.level = level
        self.title = title
        self.soup_index = soup_index
        self.parent = parent
        self.next = next_item
        self.prev = prev_item
        self.children = []
        self.contents = contents

    def __repr__(self):
        return '{class_}("{title}")'.format(
            class_=self.__class__.__name__, **vars(self))

    def get_slug(self):
        return slugify(self.title)[:50]

    def get_path(self):
        fragments = [self.get_slug()]
        parent = self.parent
        while parent:
            fragments.insert(0, parent.get_slug())
            parent = parent.parent
        return os.path.join(*fragments)

    def get_context(self):
        global_context.update(
            page=self)
        return global_context

    def render(self):
        template = env.get_template(self.template)
        return template.render(self.get_context())

    def write(self):
        output_directory = os.path.join(OUTPUT_DIR, self.get_path())
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, 'index.html')
        with open(output_path, 'w') as output_file:
            output_file.write(self.render())


class ContentPage(ContentItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContentIndex(ContentItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SingleArticle(ContentPage):
    pass


class CompoundArticle(ContentPage):
    pass


class ChapterSubsection(ContentIndex):
    pass


class ChapterSection(ContentIndex):
    pass


class ChapterIndex(ContentIndex):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = self.title.title()

    def remove_toc_items_from_contents(self):
        self.contents = [
            item for item in self.contents
            if 'toc' not in item.attrs.get('class', [''])[0]]

    def post_process_contents(self):
        self.remove_toc_items_from_contents()


class SplashPage(ContentPage):
    template = "splash_page.jinja"

    def get_path(self):
        return ''


level_definitions = {
    0: ChapterIndex,
    1: ChapterSection,
    2: ChapterSubsection,
    3: CompoundArticle,
    4: SingleArticle,
}
