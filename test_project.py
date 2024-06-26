import pytest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import project

@pytest.fixture
def mock_input():
    """Mock input() to simulate input."""
    with patch('builtins.input', return_value=''):
        yield

@pytest.fixture
def mock_csv_data():
    """Mock the CSV data for random_store() function."""
    csv_content = "storename\nTest Store\nAnother Store"
    return StringIO(csv_content)

def test_owner_action():
    owner_class_mock = MagicMock()

    # Test case for adding item
    project.owner_action('add', owner_class_mock)
    owner_class_mock.add_item.assert_called_once()

    # Test case for deleting item
    owner_class_mock.reset_mock()
    project.owner_action('delete', owner_class_mock)
    owner_class_mock.delete_item.assert_called_once()

    # Test case for changing price
    owner_class_mock.reset_mock()
    project.owner_action('change-price', owner_class_mock)
    owner_class_mock.change_price.assert_called_once()

    # Test case for restocking
    owner_class_mock.reset_mock()
    project.owner_action('restock', owner_class_mock)
    owner_class_mock.restock.assert_called_once()

    # Test case for viewing items
    owner_class_mock.reset_mock()
    project.owner_action('view', owner_class_mock)
    owner_class_mock.view_items.assert_called_once()

def test_customer_action():
    customer_class_mock = MagicMock()

    # Test case for customer help
    project.customer_action('help', customer_class_mock)
    customer_class_mock.customer_help.assert_called_once()

    # Test case for exiting
    customer_class_mock.reset_mock()
    project.customer_action('exit', customer_class_mock)
    customer_class_mock.exit.assert_called_once()

    # Test case for viewing items
    customer_class_mock.reset_mock()
    project.customer_action('view', customer_class_mock)
    customer_class_mock.view_items.assert_called_once()

    # Test case for buying items
    customer_class_mock.reset_mock()
    project.customer_action('buy', customer_class_mock)
    customer_class_mock.buy_items.assert_called_once()

    # Test case for reviewing
    customer_class_mock.reset_mock()
    project.customer_action('review', customer_class_mock)
    customer_class_mock.review.assert_called_once()

def test_random_store(monkeypatch, mock_csv_data):
    monkeypatch.setattr('builtins.open', lambda _: mock_csv_data)
    storename = project.random_store()
    assert storename in ['Test Store', 'Another Store']