import dependency_injector.providers as diProviders
import pandas as pd
import itertools
from typing import Iterable, List, Any


class WebTableParser:
    def __init__(self, table) -> None:
        self.table = table
        self.header: List = []
        self.header_rows_limit: int = 0
        self.first_rows_to_skip: int = 0
        self.last_rows_to_skip: int = 0

    def skip_rows(self, first: int = 0, last: int = 0):
        self.first_rows_to_skip = first
        self.last_rows_to_skip = last
        return self

    def header_rows(self, first: int = 0):
        self.header_rows_limit = first
        return self

    def columns(self, column_names: List[str]):
        self.header = column_names
        return self

    def parse(self) -> pd.DataFrame:
        rows: List = self.table.find_all('tr')
        header_rows: List = rows if not self.header_rows_limit else rows[:self.header_rows_limit]
        header_cells: List[List] = self._select_header_cells(header_rows)
        header: List[str] = self.header if bool(self.header) else self._parse_headers(header_cells)
        data_rows: List = rows[len(header_cells):]
        parsed_rows: List[List[str]] = self._parse_data(self._select_data_cells(data_rows))
        parsed_rows_without_index: List[List[str]] = [[parsed_rows[i][j] for j in range(1, len(parsed_rows[i]))] for i in range(len(parsed_rows))]
        return pd.DataFrame(parsed_rows_without_index, columns=header[1:], index=[parsed_rows[n][0] for n in range(len(parsed_rows))])

    @staticmethod
    def _select_header_cells(rows: Iterable) -> List[List]:
        header_cells: Iterable[List] = map(lambda row: row.find_all('th'), rows)
        return list(itertools.takewhile(lambda cells: len(cells) > 0, header_cells))

    def _parse_headers(self, cells_list: List[List]) -> List[str]:
        parsed_table: List[List] = [[] for n in range(len(cells_list))]
        for row_index in range(len(cells_list)):
            # copies row with DummyCells all with colspan 1
            copied_row = []
            for a_cell in cells_list[row_index]:
                copied_row.extend([self.DummyCell(a_cell)] * int(a_cell.attrs.get('colspan', 1)))

            # inserts here what is thrown from above by rowspan
            copied_row: List = self._adjust(copied_row, parsed_table[row_index])

            parsed_table[row_index] = [None] * len(copied_row)
            for cell_index in range(len(copied_row)):
                a_cell = copied_row[cell_index]
                parsed_table[row_index][cell_index] = a_cell.text

                # handle rowspans
                if rowspan := int(a_cell.attrs.get('rowspan', 0)):
                    a_cell.attrs['rowspan'] = 0
                    row_below_indices: List[int] = list(range(rowspan-2, 0, -1))
                    self._insert(parsed_table[row_index + rowspan-1], cell_index, a_cell)
                    a_cell.text = ''
                    for row_below_index in row_below_indices:
                        self._insert(parsed_table[row_index + row_below_index], cell_index, a_cell)

        header_columns: Iterable[Iterable[str]] = map(lambda column_index: (parsed_table[row_index][column_index] for row_index in range(len(parsed_table))), range(len(parsed_table[0])))

        return list(map(lambda header_column: '-'.join(filter(None, header_column)), header_columns))

    class DummyCell:
        def __init__(self, cell) -> None:
            self.text = cell.text.strip()
            self.attrs = {'rowspan': cell.attrs.get('rowspan', 0)}

    def _select_data_cells(self, rows: Iterable) -> List[List]:
        data_cells: List[List] = list(itertools.dropwhile(lambda cells: len(cells) == 0, map(lambda row: row.find_all(['td', 'th']), rows)))
        return data_cells[self.first_rows_to_skip:len(data_cells)-self.last_rows_to_skip]

    def _parse_data(self, cells_list: List[List]) -> List[List[str]]:
        # return map(lambda cells: [cell.text.strip() for cell in cells], cells_list)

        parsed_table: List[List] = [[] for n in range(len(cells_list))]
        for row_index in range(len(cells_list)):
            # copies row with DummyCells all with colspan 1
            copied_row = [self.DummyCell(a_cell) for a_cell in cells_list[row_index]]

            # inserts here what is thrown from above by rowspan
            copied_row: List = self._adjust(copied_row, parsed_table[row_index])

            parsed_table[row_index] = [None] * len(copied_row)
            for cell_index in range(len(copied_row)):
                a_cell = copied_row[cell_index]
                parsed_table[row_index][cell_index] = a_cell.text.strip()

                # handle rowspans
                if rowspan := int(a_cell.attrs.get('rowspan', 0)):
                    a_cell.attrs['rowspan'] = 0
                    row_below_indices: List[int] = list(range(rowspan - 2, 0, -1))
                    # not to extend onto the skipped rows
                    if row_index + rowspan - 1 < len(parsed_table):
                        self._insert(parsed_table[row_index + rowspan - 1], cell_index, a_cell)
                    for row_below_index in filter(lambda below_index: row_index + below_index < len(parsed_table), row_below_indices):
                        self._insert(parsed_table[row_index + row_below_index], cell_index, a_cell)

        return parsed_table

    @staticmethod
    def _insert(array: List, index: int, item: Any) -> None:
        length: int = len(array)
        if length > index:
            array[index] = item
        else:
            array.extend([None] * (index - length))
            array.append(item)

    @staticmethod
    def _adjust(adjusted: List, adjustee: List) -> List:
        glued = adjusted.copy()
        for i in range(len(adjustee)):
            if adjustee[i] is not None:
                glued.insert(i, adjustee[i])
        return glued


table_parser = diProviders.Factory(
    WebTableParser
)
