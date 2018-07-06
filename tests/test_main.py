from unittest import TestCase
from unittest.mock import Mock

from bs4 import BeautifulSoup

import main


class TestMain(TestCase):

    def test_add_page_links_to_article(self):
        soup = BeautifulSoup(
            '''<p class="text">If you think that an employer has illegally 
            discriminated against you either because of a complete ban against 
            people with criminal records or by treating your record negatively 
            because of your race, sex, religion, or national origin, etc., you 
            can report the employer to the EEOC or DFEH. (The EEOC and DFEH 
            are the government agencies responsible for enforcing certain 
            civil rights and anti-discrimination laws.)</p><p class="text">You 
            may want to talk to a legal aid lawyer or plaintiff’s-side 
            employment layer about your situation. You have to file a 
            complaint with the EEOC or DFEH before you are allowed to file a 
            lawsuit in court against the employer, and a lawyer can help you 
            with this process. IT is recommended you contact the EEOC or DFEH 
            immediately, and reach out to lawyers who can advise you. For 
            more information about finding a lawyer, see PG. 594. For more 
            information about filing a lawsuit, see PG. 590.</p>''',
            'html.parser')
        mock_content_item = Mock(contents=list(soup.contents))
        main.add_page_links_to_article(mock_content_item)
        results = '\n'.join([str(item) for item in mock_content_item.contents])
        self.assertIn(
            '<a class="page_link" href="/page-index/#page_594">PG.\xa0594</a>',
            results)
        self.assertIn(
            '<a class="page_link" href="/page-index/#page_590">PG.\xa0590</a>',
            results)

    def test_remove_trailing_footnote_text(self):
        test_strings = [
            'How do[7653] services or programs?[34]'
        ]
        for test_string in test_strings:
            with self.subTest(test_string=test_string):
                result = main.remove_trailing_footnote_text(test_string)
                self.assertEqual(
                        result, 'How do services or programs?')



