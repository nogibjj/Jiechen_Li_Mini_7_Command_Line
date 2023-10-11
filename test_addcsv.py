import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import azure_addcsv

# Assuming your main code is named azure_addcsv.py


class TestAzureCosmos(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame for testing
        self.sample_df = pd.DataFrame(
            {
                "rownames": ["Location1", "Location2"],
                "rights": ["Rights1", "Rights2"],
                "network": ["Network1", "Network2"],
            }
        )

    @patch("azure_addcsv.container")
    def test_clear_container(self, mock_container):
        mock_query_items = MagicMock()
        mock_query_items.query_items.return_value = [{"id": "1"}, {"id": "2"}]
        mock_container.query_items = mock_query_items.query_items

        azure_addcsv.clear_container()

        # Ensure the delete_item function was called twice
        # (because we have two mock items)
        self.assertEqual(mock_container.delete_item.call_count, 2)

    @patch("azure_addcsv.add_item")
    def test_add_dataframe_to_cosmos(self, mock_add_item):
        azure_addcsv.add_dataframe_to_cosmos(self.sample_df)

        # Check that add_item was called twice
        # (because our sample dataframe has two rows)
        self.assertEqual(mock_add_item.call_count, 2)

    @patch("azure_addcsv.container")
    def test_get_item(self, mock_container):
        mock_query_items = MagicMock()
        mock_query_items.query_items.return_value = [
            {
                "id": "0",
                "location": "Location1",
                "rights": "Rights1",
                "network": "Network1",
            }
        ]
        mock_container.query_items = mock_query_items.query_items

        item = azure_addcsv.get_item("0")
        self.assertEqual(item["location"], "Location1")


if __name__ == "__main__":
    unittest.main()
