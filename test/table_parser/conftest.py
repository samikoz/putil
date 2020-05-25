import pytest

from tests.mocks.table import get_cached_daily_table, get_cached_italy_table, get_cached_south_korea_table, \
    get_cached_france_table, get_cached_spain_table, get_cached_sweden_table


@pytest.fixture
def mock_simple_table():
    return get_cached_daily_table()


@pytest.fixture
def mock_compound_header_table():
    return get_cached_italy_table()


@pytest.fixture
def mock_multirow_cells_table():
    return get_cached_south_korea_table()


@pytest.fixture
def mock_table_with_legend():
    return get_cached_france_table()


@pytest.fixture
def mock_spain_table():
    return get_cached_spain_table()


@pytest.fixture
def mock_sweden_table():
    return get_cached_sweden_table()
