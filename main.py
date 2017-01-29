import data
from bs4 import BeautifulSoup

DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/index.html'

TOC_CLASSES = {'toc1', 'toc2', 'toc3', 'toc4'}


def get_element_index(soup, id):
    element = soup.find("a", id=id)
    parent_element = element
    while not parent_element.parent == soup:
        parent_element = parent_element.parent
    return soup.index(parent_element)


def is_toc_item(class_name):
    return class_name in TOC_CLASSES


def write_prettified_raw_index(soup):
    with open('output/index.html', 'w') as index_file:
        index_file.write(soup.prettify())


def parse_toc(soup):
    toc_items = soup.find_all(class_=is_toc_item)
    total = len(toc_items)
    digits = len(str(total))
    for i, toc_entry in enumerate(toc_items):
        level = int(toc_entry['class'][0][-1:])
        indent = level * '    '
        print('{}{}{}. "{}"'.format(
            str(i).rjust(digits),
            indent,
            level,
            toc_entry.text))


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
        parse_toc(soup)
        exit()
        write_prettified_raw_index(soup)
        final_index = len(data.ALL_CHAPTERS) - 1
        for i, Chapter in enumerate(data.ALL_CHAPTERS):
            if i == 0:
                next_chapter_element_index = get_element_index(
                    soup, data.ALL_CHAPTERS[i + 1].id_string)
                subsection = soup.contents[:next_chapter_element_index]
            elif i == final_index:
                element_index = get_element_index(soup, Chapter.id_string)
                subsection = soup.contents[element_index:]
            else:
                next_chapter_element_index = get_element_index(
                    soup, data.ALL_CHAPTERS[i + 1].id_string)
                element_index = get_element_index(soup, Chapter.id_string)
                subsection = soup.contents[
                    element_index:next_chapter_element_index]
            chapter = Chapter(subsection)
            # chapter.parse_table_of_contents()
            chapter.render()

if __name__ == '__main__':
    run()
