import os
from bs4 import BeautifulSoup

DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/index.html'


CHAPTERS = [
    {"slug": "introduction"},
    {"slug": "building-blocks-of-reentry", "id": "CHAPTER1_ID"},
    {"slug": "parole-and-probation", "id": "CHAPTER2_PP"},
    {"slug": "housing", "id": "CHAPTER4_HS"},
    {"slug": "public-benefits", "id": "CHAPTER5_PB"},
    {"slug": "employment", "id": "CHAPTER6_EM"},
    {"slug": "court-ordered-debt", "id": "CHAPTER7_COD"},
    {"slug": "family-and-children", "id": "CHAPTER8_FC"},
    {"slug": "education", "id": "CHAPTER9_ED"},
    {"slug": "your-criminal-record", "id": "CHAPTER3_EX"},
    {"slug": "legal-aid-providers", "id": "App_LegalAidProvidersList"},
    {"slug": "ca-social-services", "id": "App_CommunityResourceList"},
]


def get_element_index(soup, id):
    element = soup.find("a", id=id)
    parent_element = element
    while not parent_element.parent == soup:
        parent_element = parent_element.parent
    return soup.index(parent_element)


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
        final_index = len(CHAPTERS) - 1
        for i, chapter in enumerate(CHAPTERS):
            folder = os.path.join('output', chapter['slug'])
            if i == 0:
                next_chapter_element_index = get_element_index(
                    soup, CHAPTERS[i + 1]['id'])
                subsection = soup.contents[:next_chapter_element_index]
            elif i == final_index:
                element_index = get_element_index(soup, chapter['id'])
                subsection = soup.contents[element_index:]
            else:
                next_chapter_element_index = get_element_index(
                    soup, CHAPTERS[i + 1]['id'])
                element_index = get_element_index(soup, chapter['id'])
                subsection = soup.contents[
                    element_index:next_chapter_element_index]
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, 'index.html')
            with open(filepath, 'w') as chapter_index_file:
                chapter_index_file.write(
                    '\n'.join([str(tag) for tag in subsection])
                )

if __name__ == '__main__':
    run()
