import xml.sax

from sax_handlers import SingleTagChildrenHandler


class TestSingleTagChildrenHandler:

    sample_xml = '/home/sami/dev/putil/test/samplefile.xml'

    def test_correct_extracting(self):
        parent = 'prg-ad:PRG_PunktAdresowy'
        children_tags = {
            'prg-ad:miejscowosc': 'city',
            'prg-ad:ulica': 'street',
            'prg-ad:numerPorzadkowy': 'street_number',
            'prg-ad:kodPocztowy': 'post_code',
            'prg-ad:status': 'status'
        }

        current_parent_content = {}
        accumulated_results = []

        def translate_tag(handler, tagname):
            current_parent_content[children_tags[tagname]] = handler.get_parsed_child(tagname)

        def append_children(handler, tagname):
            nonlocal current_parent_content
            nonlocal accumulated_results
            accumulated_results.append(current_parent_content)
            current_parent_content = {}
            handler.clear_content()

        handler = SingleTagChildrenHandler(parent, set(children_tags.keys()), {
            'child_end': translate_tag, 'parent_end': append_children
        })

        expected = [
            {
                'city': 'Borzytuchom',
                'street': 'Juliusza Słowackiego',
                'street_number': '13',
                'post_code': '77-141',
                'status': 'istniejacy'
            },
            {
                'city': 'Borzytuchom',
                'street': 'Juliusza Słowackiego',
                'street_number': '10',
                'post_code': '77-141',
                'status': 'istniejacy'
            }
        ]

        xml.sax.parse(self.sample_xml, handler)
        assert accumulated_results == expected
