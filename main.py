import data
from bs4 import BeautifulSoup
from bs4.element import Tag

DOCX_PATH = '2016-04-12_Final_st.docx'
STYLE_MAP_PATH = 'stylemap.txt'
RAW_OUTPUT = 'output/raw_index.html'
OUTPUT_PATH = 'output/nice_index.html'

TOC_CLASSES = {'toc1', 'toc2', 'toc3', 'toc4'}

TOC_CONTENT_SIGNIFIER = "_Toc"


def idx_to_str(index):
    return "{num:06d}".format(num=index)


def get_soup_index(soup, element):
    indexes = []
    parent_element = element
    while not parent_element.parent == soup:
        indexes.append(
            parent_element.parent.index(
                parent_element))
        parent_element = parent_element.parent
    indexes.append(soup.index(parent_element))
    return '.'.join([idx_to_str(index) for index in reversed(indexes)])


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
            soup_index=entry.content_link.soup_index,
            level=entry.level
        )
        ContentClass = data.level_definitions[entry.level]
        items.append(ContentClass(**init_kwargs))
    return items


def soup_top_index(soup_index):
    return int(soup_index.split('.')[0])


def find_prev_from_index(index, items):
    # defined as prev sibling or parent
    item = items[index]
    for i in range(index - 1, -1, -1):
        possible_prev = items[i]
        if possible_prev.level <= item.level:
            return possible_prev
    return None


def link_parents_and_neighbors(content_items):
    last_index = len(content_items) - 1
    for index, item in enumerate(content_items):
        if index > 0:
            item.prev = find_prev_from_index(index, content_items)
        if index < last_index:
            item.next = content_items[index + 1]
        parent = find_parent_of_index(index, content_items)
        item.parent = parent
        if parent:
            parent.children.append(item)


def are_the_same_chapter(a, b):
    if not a or not b:
        return False
    prev_index = soup_top_index(a.soup_index)
    this_index = soup_top_index(b.soup_index)
    if (this_index - prev_index) < 4:
        return True
    elif (a.text in b.text) or (b.text in a.text):
        return True
    return False


def merge_two(a, b):
    if (a.text in b.text) or (b.text in a.text):
        text = a.text
    else:
        text = a.text + b.text
    return data.Chapter(text=text, soup_index=a.soup_index)


def merge_adjacent_chapter_items(chapters):
    merged_chapters = []
    last_chapter = None
    while chapters:
        next_chapter = chapters.pop(0)
        if last_chapter:
            if are_the_same_chapter(last_chapter, next_chapter):
                merged = merge_two(last_chapter, next_chapter)
                merged_chapters.append(merged)
                last_chapter = None
            else:
                merged_chapters.append(last_chapter)
                last_chapter = next_chapter
        else:
            last_chapter = next_chapter
    if not chapters and last_chapter:
        merged_chapters.append(last_chapter)
    return merged_chapters


def clean_chapter_text(chapters):
    for chapter in chapters:
        text = chapter.text.split('(')[0]
        text = text.split(':')[0]
        chapter.text = text.strip()


def parse_chapters(soup):
    results = soup.find_all('h1')
    raw_chapters = [
        data.Chapter(
            text=result.text,
            soup_index=get_soup_index(soup, result))
        for result in results]
    chapters = merge_adjacent_chapter_items(raw_chapters)
    clean_chapter_text(chapters)
    return chapters


def add_chapters_to_content_items(content_items, chapters):
    # turn chapters into content items
    chapter_content_items = [
        data.ChapterIndex(
            title=chapter.text,
            level=0,
            soup_index=chapter.soup_index
        )
        for chapter in chapters
    ]
    content_items.extend(chapter_content_items)
    return sorted(content_items, key=lambda e: e.soup_index)


def update_contents(soup, items):
    last_index = len(items) - 1
    for i, item in enumerate(items):
        if i < last_index:
            next_item = items[i + 1]
            item.contents = get_soup_contents_between_compound_indices(
                soup, item.soup_index, next_item.soup_index)
        else:
            item.contents = get_soup_contents_between_compound_indices(
                soup, item.soup_index)


def run():
    with open(RAW_OUTPUT, 'r') as raw_html_input:
        soup = BeautifulSoup(raw_html_input, 'html.parser')
        write_prettified_raw_index(soup)
        chapters = parse_chapters(soup)
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
        content_items = add_chapters_to_content_items(content_items, chapters)
        link_parents_and_neighbors(content_items)
        update_contents(soup, content_items)
        data.global_context.update(
            chapters=[item for item in content_items if item.level == 0])
        for item in content_items:
            item.write()
            print(item.get_path())

        splash_page = data.SplashPage(title='Home', level="splash")
        splash_page.write()
        print(splash_page.get_path())


if __name__ == '__main__':
    run()
