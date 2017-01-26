import data
from bs4 import BeautifulSoup


DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/index.html'


def get_element_index(soup, id):
    element = soup.find("a", id=id)
    parent_element = element
    while not parent_element.parent == soup:
        parent_element = parent_element.parent
    return soup.index(parent_element)


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
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
            chapter.parse_table_of_contents()
            chapter.render()

if __name__ == '__main__':
    run()
