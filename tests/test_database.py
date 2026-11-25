import unittest
from unittest.mock import patch
from src.database import (
    BUCKET_NAME,
    get_s3_client,
    get_order_key
)


class TestDatabase(unittest.TestCase):

    @patch("src.database.boto3.client")
    def test_get_s3_client(self, mock_client):
        result = get_s3_client()

        mock_client.assert_called_once_with("s3")
        self.assertEqual(result, mock_client.return_value)

    def test_bucket_name(self):
        self.assertTrue(BUCKET_NAME)

    def test_get_order_key(self):
        result = get_order_key("abc123")

        self.assertEqual(result, "orders/abc123.json")


if __name__ == "__main__":
    unittest.main()