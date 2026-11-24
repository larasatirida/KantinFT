import unittest
from unittest.mock import patch
from src.database import get_table, TABLE_NAME

class TestDatabase(unittest.TestCase):

    @patch("src.database.boto3.resource")
    def test_get_table(self, mock_resource):
        mock_dynamodb = mock_resource.return_value
        mock_table = mock_dynamodb.Table.return_value

        result = get_table()

        mock_resource.assert_called_once_with("dynamodb")
        mock_dynamodb.Table.assert_called_once_with(TABLE_NAME)

        self.assertEqual(result, mock_table)

    def test_table_name(self):
        self.assertEqual(TABLE_NAME, "KantinOrders")

if __name__ == "__main__":
    unittest.main()