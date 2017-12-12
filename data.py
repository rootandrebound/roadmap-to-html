import os
from slugify import slugify
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_FOLDER = 'templates'
PAGE_BASE = 'base.jinja'
OUTPUT_DIR = 'roadmap-to-html'

env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

base_template = env.get_template(PAGE_BASE)

global_context = dict(
    links=dict(
        donate=['Donate', 'http://www.rootandrebound.org/donate'],
        about_rnr=[
            'About Root & Rebound', str('http://www.rootandrebound.org/'
                                        'mission-and-vision')],
        rnr_home=['Root & Rebound', 'http://www.rootandrebound.org/'],
        take_action=[
            'Take action', 'http://www.rootandrebound.org/get-involved'],
        model_for_change=[
            'What We Do', 'http://www.rootandrebound.org/model-for-change'],
        training_hub=['Online Training Hub', 'http://reentrytraininghub.org/'],
        about_roadmap=[
            'About the Roadmap to Reentry', str('http://www.rootandrebound.org'
                                                '/roadmap-to-reentry-guide')],
        hotline_number=['510-279-4662', '5102794662'],
        email_contact=['roadmap@rootandrebound.org', 'roadmap@rootandrebound.org'],
    ),
    disclaimer="""This site, and any downloads or external sites to which it connects, are not intended to provide legal advice, but rather general legal information. No attorney-client relationship is created by using any information on this site, or any downloads or external links on the site. You should consult you own attorney if you need legal advice specific to your situation. Root & Rebound offers this site "as-is" and makes no representations or warranties of any kind concerning content, express, implied, statutory, or otherwise, including without limitation, warranties of accuracy, completeness, title, marketability, merchantability, fitness for a particular purpose, noninfringement, or the presence or absence of errors, whether or not discoverable. In particular, Root & Rebound does not make any representations of warranties that this site, or any information within it or any downloads or external links, is accurate, complete, or up-to-date, or that it will apply to your circumstances. If you or your company or agency uses information from this site, it is you responsibility to make sure that the law has not changed and applies to your particular situation."""
)


class Chapter:

    def __init__(self, text, soup_index):
        self.text = text
        self.soup_index = soup_index

    def __repr__(self):
        return "Chapter({})".format(self.text)


ROMAN_NUMERALS = {
    "I.", "II.", "III.", "IV.", "V.",
    "VI.", "VII.", "VIII.", "IX.", "X.",
    "XI.", "XII.", "XIII.", "XIV.", "XV.",
    "XI.", "XII.", "XIII.", "XIV.", "XV.",
    "XVI.", "XVII.", "XVIII.", "XIX.", "XX.",
}



def remove_leading_roman_numerals(toc_entry_text):
    return " ".join([
        chunk for chunk in toc_entry_text.split()
        if chunk not in ROMAN_NUMERALS])


class TOCEntry:

    def __init__(self, level, soup_index, element):
        self.level = level
        self.soup_index = soup_index
        self.element = element
        self.raw_text = element.text
        self.text = remove_leading_roman_numerals(element.text.split("\t")[0])
        self.content_link = None

    def __repr__(self):
        return "TOCEntry({}, {})".format(self.level, self.text)


class TOCLinkItem:

    def __init__(
            self, element, soup_index, ms_word_index, text, contents=None):
        self.element = element
        self.soup_index = soup_index
        self.ms_word_index = ms_word_index
        self.text = text
        self.contents = contents
        self.linked_entry = None

    def __repr__(self):
        return "TOCLinkItem({})".format(self.text)


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
        global_context.update(page=self)
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

    def heading_text(self):
        return '\n'.join([
            tag.text
            for tag in self.contents
            if tag.name in ('h1', 'h2', 'h3', 'h4', 'h5')
        ])

    def text(self):
        return '\n'.join([tag.text for tag in self.contents])

    def as_dict(self):
        return dict(
            title=self.title,
            level=self.level,
            heading_text=self.heading_text(),
            path=self.get_path())


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

class SearchPage(ContentPage):
    template = "search_page.jinja"

    def get_path(self):
        return 'search'

level_definitions = {
    0: ChapterIndex,
    1: ChapterSection,
    2: ChapterSubsection,
    3: CompoundArticle,
    4: SingleArticle,
}
