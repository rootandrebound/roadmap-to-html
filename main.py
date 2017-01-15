import os
import data
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape




DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/index.html'

TEMPLATE_FOLDER = 'templates'
PAGE_BASE = 'base.html'

"""
For Jinja, I'll need an Environment instance. It's used to store
configuration and global objects.

Create on Environment on initialization and use that to load templates.
"""


env = Environment(
    loader=FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

base_template = env.get_template(PAGE_BASE)


def get_element_index(soup, id):
    element = soup.find("a", id=id)
    parent_element = element
    while not parent_element.parent == soup:
        parent_element = parent_element.parent
    return soup.index(parent_element)


def render_page_index(chapter, contents):
    return base_template.render(
        chapter=chapter,
        contents=contents
    )


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
        final_index = len(data.ALL_CHAPTERS) - 1
        for i, chapter in enumerate(data.ALL_CHAPTERS):
            folder = os.path.join('output', chapter.slug)
            if i == 0:
                next_chapter_element_index = get_element_index(
                    soup, data.ALL_CHAPTERS[i + 1].id_string)
                subsection = soup.contents[:next_chapter_element_index]
            elif i == final_index:
                element_index = get_element_index(soup, chapter.id_string)
                subsection = soup.contents[element_index:]
            else:
                next_chapter_element_index = get_element_index(
                    soup, data.ALL_CHAPTERS[i + 1].id_string)
                element_index = get_element_index(soup, chapter.id_string)
                subsection = soup.contents[
                    element_index:next_chapter_element_index]
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, 'index.html')
            with open(filepath, 'w') as chapter_index_file:
                chapter_index_file.write(
                    render_page_index(chapter, subsection)
                )

if __name__ == '__main__':
    run()
