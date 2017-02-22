import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_FOLDER = 'templates'
PAGE_BASE = 'base.html'


env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

base_template = env.get_template(PAGE_BASE)


class TOCEntry:

    def __init__(self, level, soup_index, element):
        self.level = level
        self.soup_index = soup_index
        self.element = element
        self.raw_text = element.text
        self.text = element.text.split("\t")[0]


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
            self, title, parent, contents=None, next_item=None,
            prev_item=None):
        self.title = title
        self.parent = parent
        self.contents = contents
        self.next = next_item
        self.prev = prev_item



class Chapter:

    def __init__(self, contents):
        self.contents = contents
        self.folder_path = os.path.join('output', self.slug)
        self.template = base_template

    def create_folder(self):
        os.makedirs(self.folder_path, exist_ok=True)

    def write_index(self):
        filepath = os.path.join(self.folder_path, 'index.html')
        with open(filepath, 'w') as chapter_index_file:
            chapter_index_file.write(
                self.template.render(
                    chapter=self,
                    contents=self.contents))

    def render(self):
        self.create_folder()
        self.write_index()


class Introduction(Chapter):
    slug = 'introduction'
    name = 'Introduction'
    id_string = None


class Chapter1(Chapter):
    slug = 'building-blocks-of-reentry'
    name_prefix = "Chapter 1"
    name = 'Building Blocks of Reentry'
    id_string = "CHAPTER1_ID"


class Chapter2(Chapter):
    slug = 'parole-and-probation'
    name_prefix = "Chapter 2"
    name = 'Parole & Probation'
    id_string = "CHAPTER2_PP"


class Chapter3(Chapter):
    slug = 'housing'
    name_prefix = "Chapter 3"
    name = 'Housing'
    id_string = "CHAPTER4_HS"


class Chapter4(Chapter):
    slug = 'public-benefits'
    name_prefix = "Chapter 4"
    name = 'Public Benefits'
    id_string = "CHAPTER5_PB"


class Chapter5(Chapter):
    slug = 'employment'
    name_prefix = "Chapter 5"
    name = 'Employment'
    id_string = "CHAPTER6_EM"


class Chapter6(Chapter):
    slug = 'court-ordered-debt'
    name_prefix = "Chapter 6"
    name = 'Court-ordered Debt'
    id_string = "CHAPTER7_COD"


class Chapter7(Chapter):
    slug = 'family-and-children'
    name_prefix = "Chapter 7"
    name = 'Family & Children'
    id_string = "CHAPTER8_FC"


class Chapter8(Chapter):
    slug = 'education'
    name_prefix = "Chapter 8"
    name = 'Education'
    id_string = "CHAPTER9_ED"


class Chapter9(Chapter):
    slug = 'your-criminal-record'
    name_prefix = "Chapter 9"
    name = 'Understanding & Cleaning Up Your Criminal Record'
    id_string = "CHAPTER3_EX"


class Appendix(Chapter):
    slug = 'legal-aid-providers'
    name_prefix = "Appendix A"
    name = 'Legal Aid Providers'
    id_string = "App_LegalAidProvidersList"


class Appendix2(Chapter):
    slug = 'ca-social-services'
    name_prefix = "Appendix B"
    name = 'California Social Services'
    id_string = "App_CommunityResourceList"


ALL_CHAPTERS = [
    Introduction,
    Chapter1,
    Chapter2,
    Chapter3,
    Chapter4,
    Chapter5,
    Chapter6,
    Chapter7,
    Chapter8,
    Chapter9,
    Appendix,
    Appendix2,
]
