import data
from bs4 import BeautifulSoup
from bs4.element import Tag

DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/index.html'

TOC_CLASSES = {'toc1', 'toc2', 'toc3', 'toc4'}

TOC_CONTENT_SIGNIFIER = "_Toc"


def get_chapter_index(soup, id):
    element = soup.find("a", id=id)
    parent_element = element
    while not parent_element.parent == soup:
        parent_element = parent_element.parent
    return soup.index(parent_element)


def get_soup_index(soup, element):
    indexes = []
    parent_element = element
    while not parent_element.parent == soup:
        indexes.append(
            parent_element.parent.index(
                parent_element))
        parent_element = parent_element.parent
    indexes.append(soup.index(parent_element))
    return '.'.join([str(index) for index in reversed(indexes)])


def is_toc_content(element_id):
    if element_id:
        return TOC_CONTENT_SIGNIFIER in element_id
    else:
        return False


def is_toc_item(class_name):
    return class_name in TOC_CLASSES


def write_prettified_raw_index(soup):
    with open('output/index.html', 'w') as index_file:
        index_file.write(soup.prettify())


def get_msword_toc_number(element_id):
    return element_id[len(TOC_CONTENT_SIGNIFIER):]


def get_toc_content_text(item, soup):
    if item.parent != soup:
        return item.parent.text
    elif item.next_sibling:
        if not item.next_sibling.text:
            if item.next_sibling.next_sibling:
                return item.next_sibling.next_sibling.text
        return item.next_sibling.text
    else:
        return item.text


def is_valid_toc_content_item(prospective_item):
    """
    if this and next sibling are both toc items,
    and they both have no text content,
    then this one should be disregarded
    """
    next_sibling = prospective_item.next_sibling
    if isinstance(next_sibling, Tag):
        if is_toc_content(next_sibling.get('id')):
            if (not prospective_item.text) or (not next_sibling.text):
                return False
    return True


def parse_toc_entries(soup):
    parsed_toc_entries = []
    toc_items = soup.find_all(class_=is_toc_item)
    for toc_entry in toc_items:
        level = int(toc_entry['class'][0][-1:])
        soup_index = get_soup_index(soup, toc_entry)
        entry = data.TOCEntry(level, soup_index, toc_entry)
        parsed_toc_entries.append(entry)
    return parsed_toc_entries


def parse_toc_content(soup):
    toc_items = soup.find_all(id=is_toc_content)
    valid_items = list(filter(is_valid_toc_content_item, toc_items))
    parsed_content_links = []
    for element in valid_items:
        soup_index = get_soup_index(soup, element)
        msword_index = get_msword_toc_number(element['id'])
        text = get_toc_content_text(element, soup)
        item = data.TOCLinkItem(
            element, soup_index, msword_index, text, element.contents)
        parsed_content_links.append(item)
    return parsed_content_links


def get_soup_contents_between_compound_indices(soup, start, end=None):
    start_index_fragments = start.split('.')
    start_index = int(start_index_fragments[0])
    if end:
        end_index_fragments = end.split('.')
        end_index = int(end_index_fragments[0])
        return soup.contents[start_index:end_index]
    return soup.contents[start_index:]


def extract_toc_entry_contents(toc_items, soup):
    for i, item in enumerate(toc_items):
        this_soup_index = item.soup_index
        if i < len(toc_items) - 1:
            next_soup_index = toc_items[i + 1].soup_index
            item.contents = get_soup_contents_between_compound_indices(
                soup, this_soup_index, next_soup_index)
        else:
            item.contents = get_soup_contents_between_compound_indices(
                soup, this_soup_index)


def find_parent_of_index(index, items):
    # the next previous entry that has a lower level
    # should return a chapter if level == 1
    item = items[index]
    for i in range(index - 1, -1, -1):
        possible_parent = items[i]
        if possible_parent.level < item.level:
            return possible_parent
    return None


def build_content_items(toc_entries):
    items = []
    for i, entry in enumerate(toc_entries):
        init_kwargs = dict(
            title=entry.text,
            contents=entry.content_link.contents,
            level=entry.level
        )
        items.append(data.ContentItem(**init_kwargs))
    return items


def link_parents_and_neighbors(content_items):
    last_index = len(content_items) - 1
    for index, item in enumerate(content_items):
        if index > 0:
            item.prev = content_items[index - 1]
        if index < last_index:
            item.next = content_items[index + 1]
        parent = find_parent_of_index(index, content_items)
        item.parent = parent
        if parent:
            parent.children.append(item)


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
        # write_prettified_raw_index(soup)
        link_items = parse_toc_content(soup)
        toc_entries = parse_toc_entries(soup)
        toc_entry_lookup = {
            entry.text: entry
            for entry in toc_entries
        }
        for link in link_items:
            toc_entry = toc_entry_lookup.get(link.text, None)
            link.linked_entry = toc_entry
            if toc_entry:
                toc_entry.content_link = link
        usable_entries = [
            link for link in link_items
            if link.linked_entry]
        sorted_toc_links = sorted(
            usable_entries,
            key=lambda e: e.soup_index
        )
        extract_toc_entry_contents(sorted_toc_links, soup)
        usable_sorted_toc_entries = sorted(
            [entry for entry in toc_entries if entry.content_link],
            key=lambda e: e.soup_index
        )
        content_items = build_content_items(usable_sorted_toc_entries)
        link_parents_and_neighbors(content_items)
        import ipdb; ipdb.set_trace()

        # exit()
        # write_prettified_raw_index(soup)
        # final_index = len(data.ALL_CHAPTERS) - 1
        # for i, Chapter in enumerate(data.ALL_CHAPTERS):
        #     if i == 0:
        #         next_chapter_element_index = get_element_index(
        #             soup, data.ALL_CHAPTERS[i + 1].id_string)
        #         subsection = soup.contents[:next_chapter_element_index]
        #     elif i == final_index:
        #         element_index = get_element_index(soup, Chapter.id_string)
        #         subsection = soup.contents[element_index:]
        #     else:
        #         next_chapter_element_index = get_element_index(
        #             soup, data.ALL_CHAPTERS[i + 1].id_string)
        #         element_index = get_element_index(soup, Chapter.id_string)
        #         subsection = soup.contents[
        #             element_index:next_chapter_element_index]
        #     chapter = Chapter(subsection)
        #     # chapter.parse_table_of_contents()
        #     chapter.render()

if __name__ == '__main__':
    run()
