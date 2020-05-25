from table_parser import table_parser


class TestWebTableParser:
    def test_parse_size(self, mock_simple_table):
        parser = table_parser(mock_simple_table)
        assert parser.parse().shape == (138, 8)

    def test_parse_row_content(self, mock_simple_table):
        parser = table_parser(mock_simple_table)
        third_row = parser.parse().iloc[2]
        assert third_row.name == 'Iran'
        assert third_row[2] == '514'

    def test_parse_simple_header(self, mock_simple_table):
        parser = table_parser(mock_simple_table)
        assert parser.parse().columns[1] == 'NewCases'

    def test_parse_compound_header(self, mock_compound_header_table):
        parser = table_parser(mock_compound_header_table)
        parsed_table = parser.parse()
        assert parsed_table.columns[22] == 'Confirmed-Total'
        assert parsed_table.columns[27] == 'Refs'

    def test_parse_multirow_cells_table(self, mock_multirow_cells_table):
        parser = table_parser(mock_multirow_cells_table).skip_rows(last=4)
        parsed_table = parser.parse()
        assert parsed_table.columns[4] == 'Gangwon'
        assert parsed_table.iloc[1][1] == ''

    def test_row_skipping(self, mock_table_with_legend):
        parser = table_parser(mock_table_with_legend).skip_rows(first=1)
        parsed_table = parser.parse()
        assert parsed_table.iloc[1].name == '24 janvier 2020'

    def test_custom_header(self, mock_spain_table):
        parser = table_parser(mock_spain_table).skip_rows(first=1).columns(['Date', 'Graph', 'Cases', 'Deaths'])
        parsed_table = parser.parse()
        assert parsed_table.columns[1] == 'Cases'
        assert parsed_table.iloc[6][1] == '4(+33%)'

    def test_headers_mixed_with_data(self, mock_sweden_table):
        parser = table_parser(mock_sweden_table).header_rows(first=3)
        parsed_table = parser.parse()
        assert parsed_table.iloc[2][3] == ''
        assert parsed_table.iloc[7][11] == '10'

    def test_rowspan_extending_to_skipped_rows(self, mock_sweden_table):
        parser = table_parser(mock_sweden_table).header_rows(first=3).skip_rows(last=4)
        parsed_table = parser.parse()
        assert parsed_table.iloc[-1][0] == '3'
