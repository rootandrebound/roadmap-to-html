from unittest import TestCase
from unittest.mock import MagicMock

import data


class TestAppendixTOCEntry(TestCase):

    def test_parse_text_and_page(self):
        mock_self = MagicMock()
        listing_examples = [
            'Fee Waiver—California – PG.\xa078',
            'Fee Waiver—California – PG. 78',
            'Fee Waiver—California –PG. 78.',
            'Fee Waiver—California - PG.\xa078'
            'Fee Waiver—California - PG.\xa078'
        ]
        for text in listing_examples:
            with self.subTest(text=text):
                data.AppendixTOCEntry.parse_text_and_page(mock_self, text)
                self.assertEqual(mock_self.text, 'Fee Waiver—California')
                self.assertEqual(mock_self.page_number, 78)

